import asyncio
from pathlib import Path
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PDFProtector:
    """Protect PDF files with passwords and permissions"""
    
    def __init__(self):
        self.encryption_levels = {
            "40bit": 40,
            "128bit": 128,
            "256bit": 256
        }
        
        self.permission_flags = {
            "print": 4,           # Print the document
            "modify": 8,          # Modify contents
            "copy": 16,           # Copy text and images
            "annotations": 32,    # Add annotations
            "fill_forms": 256,    # Fill form fields
            "extract": 512,       # Extract text and graphics
            "assemble": 1024,     # Assemble document
            "print_high": 2048    # Print high quality
        }
    
    async def protect(self, input_path: Path, password: str, 
                     encryption_level: str = "128bit", 
                     permissions: Dict[str, bool] = None) -> Path:
        """Protect PDF with password and permissions"""
        
        if permissions is None:
            permissions = {
                "print": True,
                "modify": False,
                "copy": True,
                "annotations": True
            }
        
        output_dir = Path("processed")
        output_path = output_dir / f"protected_{input_path.name}"
        
        try:
            # Try using pikepdf first
            return await self._protect_with_pikepdf(input_path, output_path, 
                                                   password, encryption_level, permissions)
        except Exception as e:
            logger.error(f"Protection error with pikepdf: {e}")
            # Fallback to PyMuPDF
            return await self._protect_with_pymupdf(input_path, output_path, 
                                                   password, encryption_level, permissions)
    
    async def _protect_with_pikepdf(self, input_path: Path, output_path: Path,
                                   password: str, encryption_level: str,
                                   permissions: Dict[str, bool]) -> Path:
        """Protect PDF using pikepdf"""
        try:
            import pikepdf
            
            # Calculate permission bits
            permission_bits = 0
            for perm_name, allowed in permissions.items():
                if allowed and perm_name in self.permission_flags:
                    permission_bits |= self.permission_flags[perm_name]
            
            # Open PDF
            pdf = pikepdf.open(input_path)
            
            # Set encryption level
            if encryption_level == "256bit":
                # AES-256 encryption
                encryption = pikepdf.Encryption(
                    user=password,
                    owner=password,  # Use same password for owner
                    aes=True,
                    allow=permission_bits
                )
            else:
                # RC4 encryption (128-bit or 40-bit)
                encryption = pikepdf.Encryption(
                    user=password,
                    owner=password,
                    aes=False,
                    allow=permission_bits
                )
            
            # Save with encryption
            pdf.save(output_path, encryption=encryption)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Pikepdf protection error: {e}")
            raise
    
    async def _protect_with_pymupdf(self, input_path: Path, output_path: Path,
                                   password: str, encryption_level: str,
                                   permissions: Dict[str, bool]) -> Path:
        """Protect PDF using PyMuPDF"""
        try:
            import fitz
            
            # Calculate permission bits for PyMuPDF
            permission_bits = 0
            perm_map = {
                "print": fitz.PDF_PERM_PRINT,
                "modify": fitz.PDF_PERM_MODIFY,
                "copy": fitz.PDF_PERM_COPY,
                "annotations": fitz.PDF_PERM_ANNOTATE
            }
            
            for perm_name, allowed in permissions.items():
                if allowed and perm_name in perm_map:
                    permission_bits |= perm_map[perm_name]
            
            # Set encryption method
            if encryption_level == "256bit":
                encrypt_meth = fitz.PDF_ENCRYPT_AES_256
            elif encryption_level == "128bit":
                encrypt_meth = fitz.PDF_ENCRYPT_AES_128
            else:  # 40bit
                encrypt_meth = fitz.PDF_ENCRYPT_RC4_40
            
            # Open and save with encryption
            pdf = fitz.open(input_path)
            pdf.save(output_path, 
                    encryption=encrypt_meth,
                    owner_pw=password,
                    user_pw=password,
                    permissions=permission_bits)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"PyMuPDF protection error: {e}")
            raise
    
    async def add_watermark(self, input_path: Path, watermark_text: str,
                          position: str = "center", opacity: float = 0.3) -> Path:
        """Add watermark to PDF"""
        output_dir = Path("processed")
        output_path = output_dir / f"watermarked_{input_path.name}"
        
        try:
            import fitz
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            import io
            
            pdf = fitz.open(input_path)
            
            # Create watermark PDF
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            # Set font and color
            can.setFont("Helvetica", 48)
            can.setFillColorRGB(0.5, 0.5, 0.5, alpha=opacity)
            
            # Position watermark
            width, height = letter
            if position == "center":
                x, y = width/2, height/2
                can.drawCentredString(x, y, watermark_text)
            elif position == "diagonal":
                # Diagonal across page
                can.rotate(45)
                for i in range(-2, 3):
                    can.drawString(100, 100 + i*200, watermark_text)
            else:
                can.drawString(100, 100, watermark_text)
            
            can.save()
            
            # Apply watermark to each page
            watermark_pdf = fitz.open("pdf", packet.getvalue())
            
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                page_rect = page.rect
                
                # Get watermark page
                wm_page = watermark_pdf[0]
                
                # Scale watermark to fit page
                wm_rect = wm_page.rect
                scale_x = page_rect.width / wm_rect.width
                scale_y = page_rect.height / wm_rect.height
                
                # Create transformation matrix
                matrix = fitz.Matrix(scale_x, scale_y)
                
                # Apply watermark
                page.show_pdf_page(page_rect, watermark_pdf, 0, matrix=matrix)
            
            pdf.save(output_path)
            pdf.close()
            watermark_pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Watermark error: {e}")
            raise
    
    async def add_digital_signature(self, input_path: Path, 
                                   certificate_path: Path, 
                                   password: str) -> Path:
        """Add digital signature to PDF"""
        # Note: This is a simplified implementation
        # In production, use proper cryptographic libraries
        
        output_dir = Path("processed")
        output_path = output_dir / f"signed_{input_path.name}"
        
        try:
            import fitz
            
            pdf = fitz.open(input_path)
            
            # Create signature appearance
            rect = fitz.Rect(50, 50, 250, 100)  # Signature position
            
            # Add signature field (visual only in this example)
            # In real implementation, you would use proper cryptographic signing
            
            page = pdf[0]
            widget = page.add_widget({
                "field_type": fitz.PDF_WIDGET_TYPE_SIGNATURE,
                "field_name": "Signature1",
                "rect": rect
            })
            
            # Add visual representation
            page.draw_rect(rect, color=(0, 0, 0), width=1)
            page.insert_text((rect.x0 + 10, rect.y0 + 20), 
                           "Digitally Signed", fontsize=10)
            page.insert_text((rect.x0 + 10, rect.y0 + 40), 
                           "FlipFile PDF Tools", fontsize=8)
            
            pdf.save(output_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Digital signature error: {e}")
            raise
    
    def get_permission_info(self, input_path: Path) -> Dict[str, Any]:
        """Get PDF permission information"""
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            
            # Check if encrypted
            is_encrypted = pdf.is_encrypted
            
            permissions = {}
            if is_encrypted:
                # Try to get permissions (requires password)
                try:
                    # This will fail if password needed
                    perm_bits = pdf._get_permissions()
                    
                    # Decode permission bits
                    permissions = {
                        "print": bool(perm_bits & 4),
                        "modify": bool(perm_bits & 8),
                        "copy": bool(perm_bits & 16),
                        "annotations": bool(perm_bits & 32)
                    }
                except:
                    pass
            
            pdf.close()
            
            return {
                "is_encrypted": is_encrypted,
                "permissions": permissions,
                "has_owner_password": is_encrypted
            }
            
        except Exception as e:
            logger.error(f"Permission info error: {e}")
            return {"is_encrypted": False, "permissions": {}}
