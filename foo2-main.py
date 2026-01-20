from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional, Dict, Any
import os
import uuid
import shutil
from pathlib import Path
import logging
from datetime import datetime, timedelta
import tempfile
import json
import asyncio
import aiofiles
from pydantic import BaseModel

# Import tool modules
from tools.converter import PDFConverter
from tools.compressor import PDFCompressor
from tools.protector import PDFProtector
from tools.unlocker import PDFUnlocker
from tools.editor import PDFEditor
from tools.color_extractor import ColorExtractor

app = FastAPI(
    title="FlipFile PDF Tools API",
    description="Free, Fast, Secure & Private PDF Tools Conversions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
TEMP_DIR = Path("temp")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize tool instances
converter = PDFConverter()
compressor = PDFCompressor()
protector = PDFProtector()
unlocker = PDFUnlocker()
editor = PDFEditor()
color_extractor = ColorExtractor()

# Models
class ConversionRequest(BaseModel):
    format: str
    quality: Optional[str] = "high"
    pages: Optional[List[int]] = None

class CompressionRequest(BaseModel):
    quality: str = "medium"
    dpi: int = 150
    remove_metadata: bool = True

class ProtectionRequest(BaseModel):
    password: str
    encryption_level: str = "128bit"
    permissions: Dict[str, bool] = {
        "print": True,
        "modify": False,
        "copy": True,
        "annotations": True
    }

class EditRequest(BaseModel):
    operation: str
    parameters: Dict[str, Any] = {}

class ColorExtractionRequest(BaseModel):
    color_count: int = 5
    format: str = "hex"

# Store processing tasks
processing_tasks = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/api/convert")
async def convert_file(
    file: UploadFile = File(...),
    format: str = Form(...),
    quality: str = Form("high"),
    pages: Optional[str] = Form(None)
):
    """Convert PDF to other formats or vice versa"""
    try:
        # Validate format
        supported_formats = ["docx", "doc", "xlsx", "xls", "pptx", "ppt", 
                           "jpg", "jpeg", "png", "tiff", "html", "txt"]
        if format not in supported_formats:
            raise HTTPException(400, f"Unsupported format: {format}")
        
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Parse pages if provided
        page_list = None
        if pages:
            page_list = [int(p) for p in pages.split(",")]
        
        # Process conversion
        output_path = await converter.convert(
            input_path=input_path,
            output_format=format,
            quality=quality,
            pages=page_list
        )
        
        # Schedule cleanup
        schedule_cleanup([input_path, output_path], hours=1)
        
        # Return download URL
        filename = f"{Path(file.filename).stem}.{format}"
        return JSONResponse({
            "success": True,
            "message": f"File converted to {format.upper()}",
            "download_url": f"/api/download/{output_path.name}",
            "filename": filename
        })
        
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        raise HTTPException(500, f"Conversion failed: {str(e)}")

@app.post("/api/compress")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: str = Form("medium"),
    dpi: int = Form(150),
    remove_metadata: bool = Form(True)
):
    """Compress PDF file"""
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Process compression
        original_size = os.path.getsize(input_path)
        output_path = await compressor.compress(
            input_path=input_path,
            quality=quality,
            dpi=dpi,
            remove_metadata=remove_metadata
        )
        compressed_size = os.path.getsize(output_path)
        
        # Calculate compression ratio
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        # Schedule cleanup
        schedule_cleanup([input_path, output_path], hours=1)
        
        return JSONResponse({
            "success": True,
            "message": f"File compressed by {compression_ratio:.1f}%",
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": compression_ratio,
            "download_url": f"/api/download/{output_path.name}",
            "filename": f"compressed_{Path(file.filename).name}"
        })
        
    except Exception as e:
        logger.error(f"Compression error: {e}")
        raise HTTPException(500, f"Compression failed: {str(e)}")

@app.post("/api/protect")
async def protect_pdf(
    file: UploadFile = File(...),
    password: str = Form(...),
    encryption_level: str = Form("128bit"),
    permissions: str = Form('{"print": true, "modify": false, "copy": true, "annotations": true}')
):
    """Protect PDF with password"""
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Parse permissions
        try:
            perm_dict = json.loads(permissions)
        except:
            perm_dict = {
                "print": True,
                "modify": False,
                "copy": True,
                "annotations": True
            }
        
        # Process protection
        output_path = await protector.protect(
            input_path=input_path,
            password=password,
            encryption_level=encryption_level,
            permissions=perm_dict
        )
        
        # Schedule cleanup
        schedule_cleanup([input_path, output_path], hours=1)
        
        return JSONResponse({
            "success": True,
            "message": "PDF protected successfully",
            "download_url": f"/api/download/{output_path.name}",
            "filename": f"protected_{Path(file.filename).name}"
        })
        
    except Exception as e:
        logger.error(f"Protection error: {e}")
        raise HTTPException(500, f"Protection failed: {str(e)}")

@app.post("/api/unlock")
async def unlock_pdf(
    file: UploadFile = File(...),
    password: Optional[str] = Form(None)
):
    """Unlock/remove password from PDF"""
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Process unlocking
        output_path = await unlocker.unlock(
            input_path=input_path,
            password=password
        )
        
        # Schedule cleanup
        schedule_cleanup([input_path, output_path], hours=1)
        
        return JSONResponse({
            "success": True,
            "message": "PDF unlocked successfully",
            "download_url": f"/api/download/{output_path.name}",
            "filename": f"unlocked_{Path(file.filename).name}"
        })
        
    except Exception as e:
        logger.error(f"Unlock error: {e}")
        raise HTTPException(500, f"Unlock failed: {str(e)}")

@app.post("/api/edit")
async def edit_pdf(
    file: UploadFile = File(...),
    operation: str = Form(...),
    parameters: str = Form("{}")
):
    """Edit PDF (merge, split, rotate, etc.)"""
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Parse parameters
        try:
            params_dict = json.loads(parameters)
        except:
            params_dict = {}
        
        # Process editing
        output_path = await editor.edit(
            input_path=input_path,
            operation=operation,
            parameters=params_dict
        )
        
        # Schedule cleanup
        schedule_cleanup([input_path], hours=1)
        
        # If output is a directory (multiple files), create zip
        if isinstance(output_path, list):
            # Create zip file
            import zipfile
            zip_filename = f"edited_{file_id}.zip"
            zip_path = PROCESSED_DIR / zip_filename
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in output_path:
                    zipf.write(file_path, file_path.name)
            
            schedule_cleanup(output_path + [zip_path], hours=1)
            
            return JSONResponse({
                "success": True,
                "message": f"PDF edited successfully ({len(output_path)} files created)",
                "download_url": f"/api/download/{zip_filename}",
                "filename": f"edited_{Path(file.filename).stem}.zip"
            })
        else:
            schedule_cleanup([output_path], hours=1)
            return JSONResponse({
                "success": True,
                "message": "PDF edited successfully",
                "download_url": f"/api/download/{output_path.name}",
                "filename": f"edited_{Path(file.filename).name}"
            })
        
    except Exception as e:
        logger.error(f"Edit error: {e}")
        raise HTTPException(500, f"Edit failed: {str(e)}")

@app.post("/api/extract-colors")
async def extract_colors(
    file: UploadFile = File(...),
    color_count: int = Form(5),
    format: str = Form("hex")
):
    """Extract colors from image/PDF"""
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix.lower()
        file_id = str(uuid.uuid4())
        input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
        
        async with aiofiles.open(input_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Extract colors
        colors = await color_extractor.extract(
            input_path=input_path,
            color_count=color_count,
            color_format=format
        )
        
        # Create color palette image
        palette_path = await color_extractor.create_palette_image(
            colors=colors,
            output_dir=PROCESSED_DIR,
            filename=f"palette_{file_id}.png"
        )
        
        # Schedule cleanup
        schedule_cleanup([input_path, palette_path], hours=1)
        
        return JSONResponse({
            "success": True,
            "message": f"Extracted {len(colors)} colors",
            "colors": colors,
            "palette_url": f"/api/download/{palette_path.name}",
            "filename": f"color_palette_{Path(file.filename).stem}.png"
        })
        
    except Exception as e:
        logger.error(f"Color extraction error: {e}")
        raise HTTPException(500, f"Color extraction failed: {str(e)}")

@app.post("/api/batch-process")
async def batch_process(
    files: List[UploadFile] = File(...),
    operation: str = Form(...),
    parameters: str = Form("{}")
):
    """Process multiple files at once"""
    try:
        file_paths = []
        processed_files = []
        
        # Save all uploaded files
        for file in files:
            file_ext = Path(file.filename).suffix.lower()
            file_id = str(uuid.uuid4())
            input_path = UPLOAD_DIR / f"{file_id}{file_ext}"
            
            async with aiofiles.open(input_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            
            file_paths.append(input_path)
        
        # Parse parameters
        try:
            params_dict = json.loads(parameters)
        except:
            params_dict = {}
        
        # Process based on operation
        if operation == "compress":
            for input_path in file_paths:
                output_path = await compressor.compress(input_path, **params_dict)
                processed_files.append(output_path)
                
        elif operation == "convert":
            format = params_dict.get("format", "docx")
            for input_path in file_paths:
                output_path = await converter.convert(input_path, output_format=format)
                processed_files.append(output_path)
                
        elif operation == "protect":
            password = params_dict.get("password", "protected")
            for input_path in file_paths:
                output_path = await protector.protect(input_path, password=password)
                processed_files.append(output_path)
        
        # Create zip file
        import zipfile
        zip_filename = f"batch_{uuid.uuid4()}.zip"
        zip_path = PROCESSED_DIR / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in processed_files:
                zipf.write(file_path, file_path.name)
        
        # Schedule cleanup
        schedule_cleanup(file_paths + processed_files + [zip_path], hours=1)
        
        return JSONResponse({
            "success": True,
            "message": f"Processed {len(files)} files",
            "download_url": f"/api/download/{zip_filename}",
            "filename": f"batch_processed.zip"
        })
        
    except Exception as e:
        logger.error(f"Batch processing error: {e}")
        raise HTTPException(500, f"Batch processing failed: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download processed file"""
    file_path = PROCESSED_DIR / filename
    
    if not file_path.exists():
        # Also check in uploads directory
        file_path = UPLOAD_DIR / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/api/progress/{task_id}")
async def get_progress(task_id: str):
    """Get processing progress"""
    if task_id in processing_tasks:
        return JSONResponse(processing_tasks[task_id])
    return JSONResponse({"status": "not_found"})

@app.get("/api/stats")
async def get_stats():
    """Get service statistics"""
    total_uploads = len(list(UPLOAD_DIR.glob("*")))
    total_processed = len(list(PROCESSED_DIR.glob("*")))
    
    return JSONResponse({
        "total_uploads": total_uploads,
        "total_processed": total_processed,
        "uptime": "24/7",
        "status": "operational",
        "version": "1.0.0"
    })

@app.get("/api/tools")
async def get_tools():
    """Get list of available tools with capabilities"""
    tools = [
        {
            "id": "convert",
            "name": "PDF Converter",
            "description": "Convert PDF to Word, Excel, PowerPoint, Images and vice versa",
            "supported_formats": ["pdf", "docx", "xlsx", "pptx", "jpg", "png", "html", "txt"],
            "max_file_size": "200MB"
        },
        {
            "id": "compress",
            "name": "PDF Compressor",
            "description": "Reduce PDF file size without losing quality",
            "compression_levels": ["low", "medium", "high", "extreme"],
            "max_compression": "90%"
        },
        {
            "id": "protect",
            "name": "Protect PDF",
            "description": "Add password protection and permissions to PDF",
            "encryption_levels": ["40bit", "128bit", "256bit"],
            "permissions": ["print", "copy", "modify", "annotations"]
        },
        {
            "id": "unlock",
            "name": "Unlock PDF",
            "description": "Remove password protection from PDF files",
            "methods": ["password", "brute_force", "dictionary"],
            "success_rate": "95%"
        },
        {
            "id": "edit",
            "name": "Edit PDF",
            "description": "Merge, split, rotate, reorder pages in PDF",
            "operations": ["merge", "split", "rotate", "reorder", "extract_pages", "delete_pages"],
            "batch_support": True
        },
        {
            "id": "extract-colors",
            "name": "Color Extractor",
            "description": "Extract color schemes from images and PDF documents",
            "color_formats": ["hex", "rgb", "hsl", "cmyk"],
            "max_colors": 20
        }
    ]
    
    return JSONResponse({"tools": tools})

def schedule_cleanup(file_paths: List[Path], hours: int = 1):
    """Schedule files for deletion"""
    import threading
    
    def cleanup():
        import time
        time.sleep(hours * 3600)
        for file_path in file_paths:
            try:
                if file_path.exists():
                    if file_path.is_dir():
                        shutil.rmtree(file_path)
                    else:
                        file_path.unlink()
                    logger.info(f"Cleaned up: {file_path}")
            except Exception as e:
                logger.error(f"Cleanup error for {file_path}: {e}")
    
    thread = threading.Thread(target=cleanup)
    thread.daemon = True
    thread.start()

@app.on_event("startup")
async def startup_event():
    """Cleanup old files on startup"""
    cleanup_old_files()

def cleanup_old_files():
    """Cleanup files older than 24 hours"""
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for dir_path in [UPLOAD_DIR, PROCESSED_DIR, TEMP_DIR]:
        for file_path in dir_path.glob("*"):
            try:
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        file_path.unlink()
                        logger.info(f"Cleaned up old file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
