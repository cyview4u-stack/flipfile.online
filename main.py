from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
import logging
from datetime import datetime, timedelta
import tempfile
import json

# PDF processing libraries
try:
    import pikepdf
    from pdf2docx import Converter
    import ghostscript
    from PIL import Image
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: Some PDF libraries not installed. Install with: pip install pikepdf pdf2docx pymupdf pillow")

app = FastAPI(
    title="FlipFile PDF Tools API",
    description="Free, Fast, Secure & Private PDF Tools Conversions",
    version="1.0.0"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Templates
templates = Jinja2Templates(directory=".")

# Store user sessions (in production, use a database)
user_sessions = {}

class User:
    def __init__(self, user_id: str, plan: str = "free", daily_tasks: int = 0):
        self.user_id = user_id
        self.plan = plan
        self.daily_tasks = daily_tasks
        self.max_file_size = 50 * 1024 * 1024 if plan == "free" else 200 * 1024 * 1024
        self.created_at = datetime.now()
        self.files = []

class FileProcessor:
    def __init__(self):
        self.supported_formats = {
            'pdf': ['.pdf'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'],
            'documents': ['.doc', '.docx', '.txt', '.rtf'],
            'spreadsheets': ['.xls', '.xlsx', '.csv'],
            'presentations': ['.ppt', '.pptx']
        }
    
    def compress_pdf(self, input_path: str, output_path: str, quality: str = 'medium'):
        """Compress PDF file"""
        if not PDF_SUPPORT:
            raise Exception("PDF compression not available. Install required libraries.")
        
        try:
            with pikepdf.open(input_path) as pdf:
                pdf.save(output_path, compress_streams=True, stream_dict_compress=True)
            return True
        except Exception as e:
            logger.error(f"PDF compression error: {e}")
            return False
    
    def convert_pdf_to_docx(self, pdf_path: str, docx_path: str):
        """Convert PDF to DOCX"""
        if not PDF_SUPPORT:
            raise Exception("PDF conversion not available. Install required libraries.")
        
        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            return True
        except Exception as e:
            logger.error(f"PDF to DOCX conversion error: {e}")
            return False
    
    def extract_colors(self, file_path: str):
        """Extract colors from image"""
        try:
            img = Image.open(file_path)
            img = img.convert('RGB')
            
            # Simple color extraction - get dominant colors
            colors = img.getcolors(maxcolors=256*256*256)
            if colors:
                # Sort by frequency and get top 5
                colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
                hex_colors = []
                for count, color in colors:
                    hex_color = '#%02x%02x%02x' % color[:3]
                    hex_colors.append({
                        'hex': hex_color,
                        'rgb': color[:3],
                        'count': count
                    })
                return hex_colors
            return []
        except Exception as e:
            logger.error(f"Color extraction error: {e}")
            return []
    
    def merge_pdfs(self, pdf_files: List[str], output_path: str):
        """Merge multiple PDFs into one"""
        if not PDF_SUPPORT:
            raise Exception("PDF merge not available. Install required libraries.")
        
        try:
            result = pikepdf.Pdf.new()
            for pdf_file in pdf_files:
                src = pikepdf.open(pdf_file)
                result.pages.extend(src.pages)
            result.save(output_path)
            return True
        except Exception as e:
            logger.error(f"PDF merge error: {e}")
            return False

processor = FileProcessor()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page"""
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/api/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    user_id: Optional[str] = Form(None),
    operation: str = Form("compress")
):
    """Handle file uploads"""
    
    # Validate user
    if user_id and user_id in user_sessions:
        user = user_sessions[user_id]
        max_size = user.max_file_size
    else:
        # Anonymous user
        max_size = 50 * 1024 * 1024  # 50MB
    
    uploaded_files = []
    errors = []
    
    for file in files:
        try:
            # Check file size
            contents = await file.read()
            file_size = len(contents)
            
            if file_size > max_size:
                errors.append(f"File {file.filename} exceeds maximum size ({max_size/1024/1024}MB)")
                continue
            
            # Save uploaded file
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = UPLOAD_DIR / unique_filename
            
            with open(file_path, "wb") as f:
                f.write(contents)
            
            uploaded_files.append({
                "original_name": file.filename,
                "saved_name": unique_filename,
                "size": file_size,
                "path": str(file_path)
            })
            
        except Exception as e:
            errors.append(f"Error uploading {file.filename}: {str(e)}")
    
    if errors:
        return JSONResponse(
            status_code=400,
            content={"success": False, "errors": errors}
        )
    
    # Process files based on operation
    processed_files = []
    
    for file_info in uploaded_files:
        try:
            output_filename = f"processed_{uuid.uuid4()}"
            
            if operation == "compress" and file_info["original_name"].lower().endswith('.pdf'):
                output_path = PROCESSED_DIR / f"{output_filename}.pdf"
                success = processor.compress_pdf(file_info["path"], str(output_path))
                if success:
                    processed_files.append({
                        "original": file_info["original_name"],
                        "processed": f"{output_filename}.pdf",
                        "operation": "compress"
                    })
            
            elif operation == "convert_to_docx" and file_info["original_name"].lower().endswith('.pdf'):
                output_path = PROCESSED_DIR / f"{output_filename}.docx"
                success = processor.convert_pdf_to_docx(file_info["path"], str(output_path))
                if success:
                    processed_files.append({
                        "original": file_info["original_name"],
                        "processed": f"{output_filename}.docx",
                        "operation": "convert_to_docx"
                    })
            
            elif operation == "extract_colors" and any(file_info["original_name"].lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.pdf']):
                colors = processor.extract_colors(file_info["path"])
                processed_files.append({
                    "original": file_info["original_name"],
                    "colors": colors,
                    "operation": "extract_colors"
                })
            
            else:
                # For unsupported operations, just return the uploaded file
                processed_files.append({
                    "original": file_info["original_name"],
                    "processed": file_info["saved_name"],
                    "operation": "no_operation"
                })
                
        except Exception as e:
            errors.append(f"Error processing {file_info['original_name']}: {str(e)}")
    
    # Cleanup: schedule file deletion in 1 hour
    for file_info in uploaded_files:
        schedule_file_deletion(file_info["path"], hours=1)
    
    return JSONResponse(
        content={
            "success": True,
            "message": f"Processed {len(processed_files)} file(s)",
            "processed": len(processed_files),
            "files": processed_files,
            "errors": errors
        }
    )

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download processed file"""
    file_path = PROCESSED_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.post("/api/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    name: Optional[str] = Form(None)
):
    """Register a new user"""
    user_id = str(uuid.uuid4())
    user = User(user_id, plan="free", daily_tasks=0)
    user_sessions[user_id] = user
    
    return JSONResponse(
        content={
            "success": True,
            "message": "User registered successfully",
            "user_id": user_id,
            "plan": "free"
        }
    )

@app.post("/api/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...)
):
    """Login user"""
    # Simple demo login - in production, use proper authentication
    user_id = str(uuid.uuid4())
    user = User(user_id, plan="free", daily_tasks=0)
    user_sessions[user_id] = user
    
    return JSONResponse(
        content={
            "success": True,
            "message": "Login successful",
            "user_id": user_id,
            "plan": "free"
        }
    )

@app.get("/api/tools")
async def get_tools():
    """Get list of available tools"""
    tools = [
        {"id": "compress", "name": "PDF Compressor", "icon": "compress-alt", "description": "Reduce PDF file size"},
        {"id": "convert", "name": "PDF Converter", "icon": "exchange-alt", "description": "Convert PDF to other formats"},
        {"id": "merge", "name": "PDF Merger", "icon": "copy", "description": "Merge multiple PDFs"},
        {"id": "split", "name": "PDF Splitter", "icon": "cut", "description": "Split PDF into multiple files"},
        {"id": "protect", "name": "PDF Protector", "icon": "lock", "description": "Add password protection"},
        {"id": "unlock", "name": "PDF Unlocker", "icon": "unlock", "description": "Remove password protection"},
        {"id": "edit", "name": "PDF Editor", "icon": "edit", "description": "Edit PDF content"},
        {"id": "colors", "name": "Color Extractor", "icon": "palette", "description": "Extract colors from images/PDFs"}
    ]
    
    return JSONResponse(content={"tools": tools})

@app.get("/api/stats")
async def get_stats():
    """Get service statistics"""
    total_files = len(list(UPLOAD_DIR.glob("*"))) + len(list(PROCESSED_DIR.glob("*")))
    active_users = len(user_sessions)
    
    return JSONResponse(
        content={
            "total_files_processed": total_files,
            "active_users": active_users,
            "uptime": "24/7",
            "status": "operational"
        }
    )

def schedule_file_deletion(file_path: str, hours: int = 1):
    """Schedule file for deletion after specified hours"""
    import threading
    import time
    
    def delete_file():
        time.sleep(hours * 3600)  # Convert hours to seconds
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
    
    thread = threading.Thread(target=delete_file)
    thread.daemon = True
    thread.start()

@app.on_event("startup")
async def startup_event():
    """Cleanup old files on startup"""
    cleanup_old_files()

def cleanup_old_files():
    """Cleanup files older than 24 hours"""
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for dir_path in [UPLOAD_DIR, PROCESSED_DIR]:
        for file_path in dir_path.glob("*"):
            try:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up file {file_path}: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
