import asyncio
import tempfile
from pathlib import Path
import logging
import subprocess
import os

logger = logging.getLogger(__name__)

class PDFCompressor:
    """Compress PDF files with various optimization techniques"""
    
    def __init__(self):
        self.compression_levels = {
            "low": {
                "dpi": 150,
                "quality": 85,
                "remove_metadata": False,
                "compress_images": True
            },
            "medium": {
                "dpi": 150,
                "quality": 75,
                "remove_metadata": True,
                "compress_images": True
            },
            "high": {
                "dpi": 96,
                "quality": 65,
                "remove_metadata": True,
                "compress_images": True,
                "downsample_images": True
            },
            "extreme": {
                "dpi": 72,
                "quality": 50,
                "remove_metadata": True,
                "compress_images": True,
                "downsample_images": True,
                "remove_embedded_fonts": True
            }
        }
    
    async def compress(self, input_path: Path, quality: str = "medium", 
                      dpi: Optional[int] = None, remove_metadata: bool = True) -> Path:
        """Compress PDF file"""
        
        # Get compression settings
        if quality in self.compression_levels:
            settings = self.compression_levels[quality].copy()
        else:
            settings = self.compression_levels["medium"].copy()
        
        # Override DPI if specified
        if dpi:
            settings["dpi"] = dpi
        
        settings["remove_metadata"] = remove_metadata
        
        output_dir = Path("processed")
        output_path = output_dir / f"compressed_{input_path.name}"
        
        try:
            # Try using Ghostscript first (most effective)
            if await self._has_ghostscript():
                return await self._compress_with_ghostscript(input_path, output_path, settings)
            else:
                # Fallback to pikepdf
                return await self._compress_with_pikepdf(input_path, output_path, settings)
                
        except Exception as e:
            logger.error(f"Compression error: {e}")
            # Final fallback: simple copy
            import shutil
            shutil.copy2(input_path, output_path)
            return output_path
    
    async def _has_ghostscript(self) -> bool:
        """Check if Ghostscript is available"""
        try:
            result = subprocess.run(["gs", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    async def _compress_with_ghostscript(self, input_path: Path, output_path: Path, 
                                        settings: dict) -> Path:
        """Compress PDF using Ghostscript"""
        
        gs_params = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{self._get_pdfsettings(settings)}",
            f"-dDownsampleColorImages={str(settings.get('downsample_images', False)).lower()}",
            f"-dDownsampleGrayImages={str(settings.get('downsample_images', False)).lower()}",
            f"-dDownsampleMonoImages={str(settings.get('downsample_images', False)).lower()}",
            f"-dColorImageResolution={settings['dpi']}",
            f"-dGrayImageResolution={settings['dpi']}",
            f"-dMonoImageResolution={settings['dpi']}",
            f"-dColorImageDownsampleType=/Bicubic",
            f"-dGrayImageDownsampleType=/Bicubic",
            f"-dMonoImageDownsampleType=/Subsample",
            "-dNOPAUSE",
            "-dBATCH",
            "-dQUIET"
        ]
        
        if settings["remove_metadata"]:
            gs_params.append("-dDetectDuplicateImages=true")
        
        gs_params.extend([
            f"-sOutputFile={output_path}",
            str(input_path)
        ])
        
        process = await asyncio.create_subprocess_exec(
            *gs_params,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Ghostscript error: {stderr.decode()}")
        
        return output_path
    
    async def _compress_with_pikepdf(self, input_path: Path, output_path: Path, 
                                   settings: dict) -> Path:
        """Compress PDF using pikepdf"""
        try:
            import pikepdf
            from PIL import Image
            import io
            
            pdf = pikepdf.open(input_path)
            
            # Remove metadata if requested
            if settings["remove_metadata"]:
                with pdf.open_metadata() as meta:
                    if meta:
                        meta.clear()
            
            # Optimize images in PDF
            if settings.get("compress_images", True):
                await self._optimize_pdf_images(pdf, settings)
            
            # Remove embedded fonts if requested
            if settings.get("remove_embedded_fonts", False):
                self._remove_embedded_fonts(pdf)
            
            # Save with compression
            pdf.save(output_path, 
                    compress_streams=True,
                    stream_dict_compress=True,
                    preserve_pdfa=False,
                    object_stream_mode=pikepdf.ObjectStreamMode.generate)
            
            pdf.close()
            return output_path
            
        except Exception as e:
            logger.error(f"Pikepdf compression error: {e}")
            raise
    
    async def _optimize_pdf_images(self, pdf, settings: dict):
        """Optimize images within PDF"""
        try:
            from PIL import Image
            import io
            
            for page in pdf.pages:
                if '/Resources' in page and '/XObject' in page.Resources:
                    xobjects = page.Resources.XObject
                    for obj_name in xobjects:
                        xobject = xobjects[obj_name]
                        if xobject.Subtype == '/Image':
                            # Get image data
                            if '/Filter' in xobject:
                                filter_name = xobject.Filter
                                if filter_name == '/DCTDecode':  # JPEG
                                    # Recompress JPEG with lower quality
                                    img_data = xobject.read_raw_bytes()
                                    img = Image.open(io.BytesIO(img_data))
                                    
                                    # Convert to RGB if needed
                                    if img.mode != 'RGB':
                                        img = img.convert('RGB')
                                    
                                    # Save with lower quality
                                    output = io.BytesIO()
                                    img.save(output, format='JPEG', 
                                           quality=settings['quality'],
                                           optimize=True)
                                    
                                    # Update PDF object
                                    xobject.write(output.getvalue(), 
                                                filter=pikepdf.Name("/DCTDecode"))
            
        except Exception as e:
            logger.warning(f"Image optimization skipped: {e}")
    
    def _remove_embedded_fonts(self, pdf):
        """Remove embedded fonts to reduce size"""
        try:
            if '/AcroForm' in pdf.Root:
                del pdf.Root.AcroForm
            
            # Remove font subsets
            for page in pdf.pages:
                if '/Resources' in page and '/Font' in page.Resources:
                    fonts = page.Resources.Font
                    for font_name in list(fonts.keys()):
                        font = fonts[font_name]
                        if '/Subtype' in font and font.Subtype == '/Type0':
                            # This is a composite font, might be embedded
                            del fonts[font_name]
                            
        except Exception as e:
            logger.warning(f"Font removal skipped: {e}")
    
    def _get_pdfsettings(self, settings: dict) -> str:
        """Get Ghostscript PDFSETTINGS value"""
        dpi = settings['dpi']
        
        if dpi >= 300:
            return "prepress"
        elif dpi >= 150:
            return "printer"
        elif dpi >= 96:
            return "ebook"
        else:
            return "screen"
    
    async def batch_compress(self, input_paths: List[Path], quality: str = "medium") -> List[Path]:
        """Compress multiple PDF files"""
        tasks = []
        for input_path in input_paths:
            task = self.compress(input_path, quality)
            tasks.append(task)
        
        return await asyncio.gather(*tasks)
    
    def estimate_compression(self, input_path: Path, quality: str = "medium") -> dict:
        """Estimate compression results"""
        import os
        
        original_size = os.path.getsize(input_path)
        
        # Estimated compression ratios based on quality
        ratios = {
            "low": 0.7,      # 30% reduction
            "medium": 0.5,   # 50% reduction
            "high": 0.3,     # 70% reduction
            "extreme": 0.1   # 90% reduction
        }
        
        ratio = ratios.get(quality, 0.5)
        estimated_size = int(original_size * ratio)
        
        return {
            "original_size": original_size,
            "estimated_size": estimated_size,
            "estimated_reduction": original_size - estimated_size,
            "estimated_ratio": ((original_size - estimated_size) / original_size) * 100
        }
