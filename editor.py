import asyncio
from pathlib import Path
import logging
from typing import List, Dict, Any, Optional, Union
import tempfile

logger = logging.getLogger(__name__)

class PDFEditor:
    """Edit PDF files - merge, split, rotate, reorder pages"""
    
    def __init__(self):
        self.supported_operations = [
            "merge", "split", "rotate", "reorder", 
            "extract_pages", "delete_pages", "insert",
            "resize", "add_blank", "extract_images"
        ]
    
    async def edit(self, input_path: Path, operation: str, 
                  parameters: Dict[str, Any] = None) -> Union[Path, List[Path]]:
        """Perform PDF editing operation"""
        
        if parameters is None:
            parameters = {}
        
        if operation not in self.supported_operations:
            raise ValueError(f"Unsupported operation: {operation}")
        
        # Route to appropriate method
        if operation == "merge":
            return await self.merge_pdfs([input_path] + parameters.get("additional_files", []), 
                                        parameters)
        elif operation == "split":
            return await self.split_pdf(input_path, parameters)
        elif operation == "rotate":
            return await self.rotate_pages(input_path, parameters)
        elif operation == "reorder":
            return await self.reorder_pages(input_path, parameters)
        elif operation == "extract_pages":
            return await self.extract_pages(input_path, parameters)
        elif operation == "delete_pages":
            return await self.delete_pages(input_path, parameters)
        elif operation == "insert":
            return await self.insert_pages(input_path, parameters)
        elif operation == "resize":
            return await self.resize_pages(input_path, parameters)
        elif operation == "add_blank":
            return await self.add_blank_pages(input_path, parameters)
        elif operation == "extract_images":
            return await self.extract_images(input_path, parameters)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def merge_pdfs(self, pdf_paths: List[Path], 
                        parameters: Dict[str, Any]) -> Path:
        """Merge multiple PDFs into one"""
        output_dir = Path("processed")
        output_path = output_dir / f"merged_{len(pdf_paths)}_files.pdf"
        
        try:
            import pikepdf
            
            merged = pikepdf.Pdf.new()
            
            for pdf_path in pdf_paths:
                if not pdf_path.exists():
                    continue
                
                src = pikepdf.open(pdf_path)
                merged.pages.extend(src.pages)
                src.close()
            
            # Apply bookmarks if requested
            if parameters.get("add_bookmarks", False):
                self._add_merge_bookmarks(merged, pdf_paths)
            
            merged.save(output_path)
            merged.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Merge error: {e}")
            raise
    
    async def split_pdf(self, input_path: Path, 
                       parameters: Dict[str, Any]) -> List[Path]:
        """Split PDF into multiple files"""
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            total_pages = len(pdf.pages)
            
            split_type = parameters.get("type", "single_pages")
            output_files = []
            
            if split_type == "single_pages":
                # Split into individual pages
                for page_num in range(total_pages):
                    output = pikepdf.Pdf.new()
                    output.pages.append(pdf.pages[page_num])
                    
                    output_path = Path("processed") / f"{input_path.stem}_page_{page_num+1}.pdf"
                    output.save(output_path)
                    output.close()
                    
                    output_files.append(output_path)
            
            elif split_type == "ranges":
                # Split by page ranges
                ranges = parameters.get("ranges", ["1-"])
                
                for range_str in ranges:
                    if "-" in range_str:
                        start_str, end_str = range_str.split("-", 1)
                        start = int(start_str) - 1 if start_str else 0
                        end = int(end_str) - 1 if end_str else total_pages - 1
                    else:
                        start = end = int(range_str) - 1
                    
                    output = pikepdf.Pdf.new()
                    for page_num in range(start, end + 1):
                        if page_num < total_pages:
                            output.pages.append(pdf.pages[page_num])
                    
                    output_path = Path("processed") / f"{input_path.stem}_pages_{start+1}-{end+1}.pdf"
                    output.save(output_path)
                    output.close()
                    
                    output_files.append(output_path)
            
            elif split_type == "every_n":
                # Split every N pages
                n = parameters.get("n", 1)
                
                for i in range(0, total_pages, n):
                    output = pikepdf.Pdf.new()
                    end = min(i + n, total_pages)
                    
                    for page_num in range(i, end):
                        output.pages.append(pdf.pages[page_num])
                    
                    output_path = Path("processed") / f"{input_path.stem}_part_{i//n + 1}.pdf"
                    output.save(output_path)
                    output.close()
                    
                    output_files.append(output_path)
            
            pdf.close()
            return output_files
            
        except Exception as e:
            logger.error(f"Split error: {e}")
            raise
    
    async def rotate_pages(self, input_path: Path, 
                          parameters: Dict[str, Any]) -> Path:
        """Rotate PDF pages"""
        output_dir = Path("processed")
        output_path = output_dir / f"rotated_{input_path.name}"
        
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            
            # Get rotation parameters
            angle = parameters.get("angle", 90)
            pages = parameters.get("pages", "all")
            
            if pages == "all":
                page_range = range(len(pdf.pages))
            elif isinstance(pages, list):
                page_range = [p - 1 for p in pages if 1 <= p <= len(pdf.pages)]
            elif isinstance(pages, str) and "-" in pages:
                start_str, end_str = pages.split("-", 1)
                start = int(start_str) - 1 if start_str else 0
                end = int(end_str) - 1 if end_str else len(pdf.pages) - 1
                page_range = range(start, end + 1)
            else:
                page_range = [int(pages) - 1]
            
            # Apply rotation
            for page_num in page_range:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    page.Rotate = (page.get('/Rotate', 0) + angle) % 360
            
            pdf.save(output_path)
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Rotate error: {e}")
            raise
    
    async def reorder_pages(self, input_path: Path, 
                           parameters: Dict[str, Any]) -> Path:
        """Reorder PDF pages"""
        output_dir = Path("processed")
        output_path = output_dir / f"reordered_{input_path.name}"
        
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            total_pages = len(pdf.pages)
            
            # Get new page order
            new_order = parameters.get("order", list(range(1, total_pages + 1)))
            
            # Validate order
            if len(new_order) != total_pages:
                raise ValueError("Page order must include all pages")
            
            if sorted(new_order) != list(range(1, total_pages + 1)):
                raise ValueError("Page order must be a permutation of page numbers")
            
            # Create new PDF with reordered pages
            output = pikepdf.Pdf.new()
            for page_num in new_order:
                output.pages.append(pdf.pages[page_num - 1])
            
            output.save(output_path)
            output.close()
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Reorder error: {e}")
            raise
    
    async def extract_pages(self, input_path: Path, 
                           parameters: Dict[str, Any]) -> Path:
        """Extract specific pages to new PDF"""
        output_dir = Path("processed")
        output_path = output_dir / f"extracted_{input_path.name}"
        
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            
            # Get pages to extract
            pages = parameters.get("pages", [1])
            if isinstance(pages, str):
                pages = [int(p) for p in pages.split(",")]
            
            # Create new PDF with extracted pages
            output = pikepdf.Pdf.new()
            for page_num in pages:
                if 1 <= page_num <= len(pdf.pages):
                    output.pages.append(pdf.pages[page_num - 1])
            
            output.save(output_path)
            output.close()
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Extract pages error: {e}")
            raise
    
    async def delete_pages(self, input_path: Path, 
                          parameters: Dict[str, Any]) -> Path:
        """Delete specific pages from PDF"""
        output_dir = Path("processed")
        output_path = output_dir / f"deleted_{input_path.name}"
        
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            total_pages = len(pdf.pages)
            
            # Get pages to delete
            pages_to_delete = parameters.get("pages", [])
            if isinstance(pages_to_delete, str):
                pages_to_delete = [int(p) for p in pages_to_delete.split(",")]
            
            # Keep all pages except those to delete
            pages_to_keep = [i for i in range(total_pages) 
                           if (i + 1) not in pages_to_delete]
            
            # Create new PDF
            output = pikepdf.Pdf.new()
            for page_num in pages_to_keep:
                output.pages.append(pdf.pages[page_num])
            
            output.save(output_path)
            output.close()
            pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Delete pages error: {e}")
            raise
    
    async def insert_pages(self, input_path: Path, 
                          parameters: Dict[str, Any]) -> Path:
        """Insert pages from another PDF"""
        output_dir = Path("processed")
        output_path = output_dir / f"inserted_{input_path.name}"
        
        try:
            import pikepdf
            
            pdf = pikepdf.open(input_path)
            
            # Get insertion parameters
            insert_file = Path(parameters.get("insert_file", ""))
            position = parameters.get("position", "end")
            pages = parameters.get("pages", "all")
            
            if not insert_file.exists():
                raise ValueError("Insert file not found")
            
            # Open PDF to insert
            insert_pdf = pikepdf.open(insert_file)
            
            # Get pages to insert
            if pages == "all":
                insert_pages = list(range(len(insert_pdf.pages)))
            else:
                insert_pages = [int(p) - 1 for p in pages.split(",")]
            
            # Create new PDF with inserted pages
            output = pikepdf.Pdf.new()
            
            if position == "start":
                # Insert at beginning
                for page_num in insert_pages:
                    output.pages.append(insert_pdf.pages[page_num])
                for page in pdf.pages:
                    output.pages.append(page)
                    
            elif position == "end":
                # Insert at end
                for page in pdf.pages:
                    output.pages.append(page)
                for page_num in insert_pages:
                    output.pages.append(insert_pdf.pages[page_num])
                    
            elif isinstance(position, int):
                # Insert at specific position
                for i, page in enumerate(pdf.pages):
                    if i == position - 1:
                        for page_num in insert_pages:
                            output.pages.append(insert_pdf.pages[page_num])
                    output.pages.append(page)
            
            output.save(output_path)
            output.close()
            pdf.close()
            insert_pdf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Insert pages error: {e}")
            raise
    
    async def resize_pages(self, input_path: Path, 
                          parameters: Dict[str, Any]) -> Path:
        """Resize PDF pages"""
        output_dir = Path("processed")
        output_path = output_dir / f"resized_{input_path.name}"
        
        try:
            import pikepdf
            import fitz
            
            pdf = pikepdf.open(input_path)
            
            # Get resize parameters
            size = parameters.get("size", "A4")
            orientation = parameters.get("orientation", "portrait")
            
            # Convert pikepdf to PyMuPDF for resizing
            # Save temporary file
            temp_path = Path("temp") / f"temp_{input_path.name}"
            pdf.save(temp_path)
            pdf.close()
            
            # Open with PyMuPDF for resizing
            doc = fitz.open(temp_path)
            
            # Page sizes in points (1/72 inch)
            page_sizes = {
                "A4": (595, 842),
                "Letter": (612, 792),
                "Legal": (612, 1008),
                "A3": (842, 1191),
                "A5": (420, 595),
                "B4": (709, 1001),
                "B5": (499, 709)
            }
            
            new_size = page_sizes.get(size, (595, 842))
            if orientation == "landscape":
                new_size = (new_size[1], new_size[0])
            
            # Create new document with resized pages
            new_doc = fitz.open()
            
            for page in doc:
                # Create new page with desired size
                new_page = new_doc.new_page(width=new_size[0], height=new_size[1])
                
                # Calculate scaling
                rect = page.rect
                scale_x = new_size[0] / rect.width
                scale_y = new_size[1] / rect.height
                scale = min(scale_x, scale_y) * 0.9  # 90% scale with margin
                
                # Calculate position (center)
                x = (new_size[0] - (rect.width * scale)) / 2
                y = (new_size[1] - (rect.height * scale)) / 2
                
                # Show original page on new page
                new_page.show_pdf_page(
                    fitz.Rect(x, y, x + rect.width * scale, y + rect.height * scale),
                    doc,
                    page.number
                )
            
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            
            # Cleanup temp file
            temp_path.unlink(missing_ok=True)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Resize error: {e}")
            raise
    
    async def add_blank_pages(self, input_path: Path, 
                             parameters: Dict[str, Any]) -> Path:
        """Add blank pages to PDF"""
        output_dir = Path("processed")
        output_path = output_dir / f"with_blanks_{input_path.name}"
        
        try:
            import pikepdf
            import fitz
            
            pdf = pikepdf.open(input_path)
            
            # Get parameters
            count = parameters.get("count", 1)
            position = parameters.get("position", "end")
            page_size = parameters.get("page_size", "same")
            
            # Save temporary file
            temp_path = Path("temp") / f"temp_{input_path.name}"
            pdf.save(temp_path)
            pdf.close()
            
            # Open with PyMuPDF
            doc = fitz.open(temp_path)
            new_doc = fitz.open()
            
            # Get page size for blank pages
            if page_size == "same" and len(doc) > 0:
                first_page = doc[0]
                blank_size = (first_page.rect.width, first_page.rect.height)
            else:
                blank_size = (595, 842)  # A4 default
            
            if position == "start":
                # Add blanks at start
                for _ in range(count):
                    new_doc.new_page(width=blank_size[0], height=blank_size[1])
                
                # Copy all original pages
                new_doc.insert_pdf(doc)
                
            elif position == "end":
                # Copy all original pages
                new_doc.insert_pdf(doc)
                
                # Add blanks at end
                for _ in range(count):
                    new_doc.new_page(width=blank_size[0], height=blank_size[1])
                    
            elif position == "between":
                # Add blank between each page
                interval = parameters.get("interval", 1)
                
                for i, page in enumerate(doc):
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    
                    if (i + 1) % interval == 0 and i < len(doc) - 1:
                        for _ in range(count):
                            new_doc.new_page(width=blank_size[0], height=blank_size[1])
            
            new_doc.save(output_path)
            new_doc.close()
            doc.close()
            
            # Cleanup temp file
            temp_path.unlink(missing_ok=True)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Add blank pages error: {e}")
            raise
    
    async def extract_images(self, input_path: Path, 
                            parameters: Dict[str, Any]) -> List[Path]:
        """Extract images from PDF"""
        try:
            import fitz
            from PIL import Image
            import io
            
            doc = fitz.open(input_path)
            image_paths = []
            
            # Get extraction parameters
            format = parameters.get("format", "png")
            dpi = parameters.get("dpi", 150)
            pages = parameters.get("pages", "all")
            
            if pages == "all":
                page_range = range(len(doc))
            elif isinstance(pages, str):
                page_range = [int(p) - 1 for p in pages.split(",")]
            else:
                page_range = pages
            
            image_count = 0
            
            for page_num in page_range:
                if not (0 <= page_num < len(doc)):
                    continue
                
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Convert to desired format if needed
                        if format.lower() != image_ext.lower():
                            img_pil = Image.open(io.BytesIO(image_bytes))
                            
                            # Resize if DPI is specified
                            if dpi:
                                current_dpi = img_pil.info.get('dpi', (72, 72))
                                if current_dpi[0] != dpi:
                                    scale = dpi / current_dpi[0]
                                    new_size = (int(img_pil.width * scale), 
                                              int(img_pil.height * scale))
                                    img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
                            
                            # Save in desired format
                            output_path = Path("processed") / \
                                        f"{input_path.stem}_page{page_num+1}_img{img_index+1}.{format}"
                            
                            if format.lower() == "jpg":
                                img_pil = img_pil.convert("RGB")  # JPG doesn't support alpha
                                img_pil.save(output_path, "JPEG", quality=95, optimize=True)
                            else:
                                img_pil.save(output_path, format.upper())
                            
                            image_paths.append(output_path)
                            image_count += 1
                        else:
                            # Save original
                            output_path = Path("processed") / \
                                        f"{input_path.stem}_page{page_num+1}_img{img_index+1}.{image_ext}"
                            
                            with open(output_path, "wb") as f:
                                f.write(image_bytes)
                            
                            image_paths.append(output_path)
                            image_count += 1
            
            doc.close()
            
            if not image_paths:
                raise Exception("No images found in PDF")
            
            return image_paths
            
        except Exception as e:
            logger.error(f"Extract images error: {e}")
            raise
    
    def _add_merge_bookmarks(self, pdf, pdf_paths: List[Path]):
        """Add bookmarks for merged PDF"""
        try:
            # This adds outline items (bookmarks) for each merged file
            if hasattr(pdf, 'Root') and '/Outlines' not in pdf.Root:
                pdf.Root.Outlines = pikepdf.Dictionary({})
            
            current_page = 0
            for file_path in pdf_paths:
                if not file_path.exists():
                    continue
                
                # Add bookmark for this file
                bookmark = pikepdf.Dictionary({
                    '/Title': file_path.name,
                    '/Parent': pdf.Root.Outlines,
                    '/First': None,
                    '/Last': None,
                    '/Count': 0
                })
                
                # Link to first page of this file
                if current_page < len(pdf.pages):
                    bookmark['/Dest'] = [pdf.pages[current_page].obj, '/Fit']
                
                # Add to outlines
                if '/First' not in pdf.Root.Outlines:
                    pdf.Root.Outlines['/First'] = bookmark
                pdf.Root.Outlines['/Last'] = bookmark
                
                # Update page count
                src_pdf = pikepdf.open(file_path)
                current_page += len(src_pdf.pages)
                src_pdf.close()
                
        except Exception as e:
            logger.warning(f"Could not add bookmarks: {e}")
