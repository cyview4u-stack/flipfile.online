import asyncio
from pathlib import Path
import logging
from typing import List, Dict, Any, Tuple
import tempfile

logger = logging.getLogger(__name__)

class ColorExtractor:
    """Extract color palettes from images and PDFs"""
    
    def __init__(self):
        self.color_formats = ["hex", "rgb", "hsl", "cmyk"]
        self.color_spaces = ["rgb", "hsl", "lab", "hsv"]
    
    async def extract(self, input_path: Path, color_count: int = 5, 
                     color_format: str = "hex") -> List[Dict[str, Any]]:
        """Extract color palette from file"""
        
        # Validate format
        if color_format not in self.color_formats:
            color_format = "hex"
        
        # Check file type
        if input_path.suffix.lower() in [".pdf"]:
            return await self._extract_from_pdf(input_path, color_count, color_format)
        else:
            return await self._extract_from_image(input_path, color_count, color_format)
    
    async def _extract_from_image(self, image_path: Path, color_count: int,
                                 color_format: str) -> List[Dict[str, Any]]:
        """Extract colors from image file"""
        try:
            from PIL import Image
            import numpy as np
            from sklearn.cluster import KMeans
            
            # Open and resize image for faster processing
            img = Image.open(image_path)
            img = img.convert("RGB")
            
            # Resize if image is too large
            max_size = 300
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(img)
            pixels = img_array.reshape(-1, 3)
            
            # Use K-means clustering to find dominant colors
            if len(pixels) > color_count:
                kmeans = KMeans(n_clusters=min(color_count, 8), 
                              n_init=10, random_state=42)
                kmeans.fit(pixels)
                
                # Get cluster centers (colors)
                colors = kmeans.cluster_centers_.astype(int)
                
                # Get cluster sizes for weighting
                unique, counts = np.unique(kmeans.labels_, return_counts=True)
                cluster_sizes = dict(zip(unique, counts))
                
                # Sort by cluster size (most dominant first)
                sorted_indices = sorted(range(len(colors)), 
                                      key=lambda i: cluster_sizes.get(i, 0), 
                                      reverse=True)
                colors = colors[sorted_indices]
            else:
                # For small images, just get unique colors
                colors = np.unique(pixels, axis=0)
            
            # Convert to requested format
            color_palette = []
            for color in colors[:color_count]:
                color_dict = self._format_color(color, color_format)
                color_palette.append(color_dict)
            
            return color_palette
            
        except Exception as e:
            logger.error(f"Image color extraction error: {e}")
            # Fallback: extract using PIL's getcolors
            try:
                from PIL import Image
                
                img = Image.open(image_path)
                img = img.convert("RGB")
                
                # Get color frequencies
                colors = img.getcolors(maxcolors=256*256)
                if colors:
                    colors.sort(reverse=True, key=lambda x: x[0])
                    
                    color_palette = []
                    for count, color in colors[:color_count]:
                        color_dict = self._format_color(color, color_format)
                        color_dict["count"] = count
                        color_palette.append(color_dict)
                    
                    return color_palette
                
            except Exception as e2:
                logger.error(f"Fallback extraction also failed: {e2}")
            
            # Return default colors if all else fails
            return self._get_default_colors(color_format, color_count)
    
    async def _extract_from_pdf(self, pdf_path: Path, color_count: int,
                               color_format: str) -> List[Dict[str, Any]]:
        """Extract colors from PDF file"""
        try:
            import fitz
            from PIL import Image
            import numpy as np
            from sklearn.cluster import KMeans
            import io
            
            pdf = fitz.open(pdf_path)
            all_colors = []
            
            # Extract colors from each page
            for page_num in range(min(3, len(pdf))):  # Limit to first 3 pages
                page = pdf.load_page(page_num)
                
                # Extract images from page
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list[:5]):  # Limit to 5 images per page
                    xref = img[0]
                    base_image = pdf.extract_image(xref)
                    
                    if base_image:
                        image_bytes = base_image["image"]
                        
                        # Convert to PIL Image
                        img_pil = Image.open(io.BytesIO(image_bytes))
                        img_pil = img_pil.convert("RGB")
                        
                        # Resize for processing
                        max_size = 200
                        if max(img_pil.size) > max_size:
                            ratio = max_size / max(img_pil.size)
                            new_size = tuple(int(dim * ratio) for dim in img_pil.size)
                            img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
                        
                        # Get colors
                        img_array = np.array(img_pil)
                        pixels = img_array.reshape(-1, 3)
                        
                        # Sample pixels
                        if len(pixels) > 1000:
                            indices = np.random.choice(len(pixels), 1000, replace=False)
                            pixels = pixels[indices]
                        
                        all_colors.extend(pixels)
            
            pdf.close()
            
            if not all_colors:
                return self._get_default_colors(color_format, color_count)
            
            # Convert to numpy array
            all_colors = np.array(all_colors)
            
            # Cluster colors
            if len(all_colors) > color_count:
                kmeans = KMeans(n_clusters=min(color_count, 8), 
                              n_init=10, random_state=42)
                kmeans.fit(all_colors)
                colors = kmeans.cluster_centers_.astype(int)
            else:
                colors = np.unique(all_colors, axis=0)
            
            # Format colors
            color_palette = []
            for color in colors[:color_count]:
                color_dict = self._format_color(color, color_format)
                color_palette.append(color_dict)
            
            return color_palette
            
        except Exception as e:
            logger.error(f"PDF color extraction error: {e}")
            return self._get_default_colors(color_format, color_count)
    
    def _format_color(self, color, format: str) -> Dict[str, Any]:
        """Convert color to requested format"""
        r, g, b = color[:3]
        
        color_dict = {
            "hex": self._rgb_to_hex(r, g, b),
            "rgb": {"r": r, "g": g, "b": b},
            "hsl": self._rgb_to_hsl(r, g, b),
            "cmyk": self._rgb_to_cmyk(r, g, b)
        }
        
        # Add additional formats
        if format == "hex":
            return {"hex": color_dict["hex"], "rgb": color_dict["rgb"]}
        else:
            return {format: color_dict[format], "hex": color_dict["hex"]}
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()
    
    def _rgb_to_hsl(self, r: int, g: int, b: int) -> Dict[str, float]:
        """Convert RGB to HSL"""
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        cmax = max(r_norm, g_norm, b_norm)
        cmin = min(r_norm, g_norm, b_norm)
        delta = cmax - cmin
        
        # Calculate hue
        if delta == 0:
            h = 0
        elif cmax == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif cmax == g_norm:
            h = 60 * (((b_norm - r_norm) / delta) + 2)
        else:
            h = 60 * (((r_norm - g_norm) / delta) + 4)
        
        # Calculate lightness
        l = (cmax + cmin) / 2
        
        # Calculate saturation
        if delta == 0:
            s = 0
        else:
            s = delta / (1 - abs(2 * l - 1))
        
        return {
            "h": round(h),
            "s": round(s * 100),
            "l": round(l * 100)
        }
    
    def _rgb_to_cmyk(self, r: int, g: int, b: int) -> Dict[str, float]:
        """Convert RGB to CMYK"""
        if (r, g, b) == (0, 0, 0):
            return {"c": 0, "m": 0, "y": 0, "k": 100}
        
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0
        
        k = 1 - max(r_norm, g_norm, b_norm)
        c = (1 - r_norm - k) / (1 - k) if (1 - k) != 0 else 0
        m = (1 - g_norm - k) / (1 - k) if (1 - k) != 0 else 0
        y = (1 - b_norm - k) / (1 - k) if (1 - k) != 0 else 0
        
        return {
            "c": round(c * 100, 1),
            "m": round(m * 100, 1),
            "y": round(y * 100, 1),
            "k": round(k * 100, 1)
        }
    
    def _get_default_colors(self, format: str, count: int) -> List[Dict[str, Any]]:
        """Get default color palette"""
        default_colors = [
            (255, 0, 0),      # Red
            (0, 255, 0),      # Green
            (0, 0, 255),      # Blue
            (255, 255, 0),    # Yellow
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (128, 0, 128),    # Purple
            (255, 165, 0),    # Orange
            (0, 128, 0),      # Dark Green
            (75, 0, 130)      # Indigo
        ]
        
        colors = []
        for i in range(min(count, len(default_colors))):
            color = default_colors[i]
            colors.append(self._format_color(color, format))
        
        return colors
    
    async def create_palette_image(self, colors: List[Dict[str, Any]], 
                                  output_dir: Path, filename: str) -> Path:
        """Create an image showing the color palette"""
        try:
            from PIL import Image, ImageDraw
            
            # Create image
            width = 800
            height = 200
            img = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(img)
            
            # Calculate color swatch dimensions
            num_colors = len(colors)
            swatch_width = width // num_colors
            
            # Draw color swatches
            for i, color_info in enumerate(colors):
                # Get RGB values
                if "rgb" in color_info:
                    rgb = color_info["rgb"]
                    color = (rgb["r"], rgb["g"], rgb["b"])
                elif "hex" in color_info:
                    hex_color = color_info["hex"].lstrip("#")
                    color = tuple(int(hex_color[j:j+2], 16) for j in (0, 2, 4))
                else:
                    color = (255, 255, 255)  # Default white
                
                # Draw swatch
                x0 = i * swatch_width
                x1 = x0 + swatch_width
                draw.rectangle([x0, 0, x1, height], fill=color, outline="black")
                
                # Add hex code
                hex_code = color_info.get("hex", "#FFFFFF")
                draw.text((x0 + 10, height - 30), hex_code, fill="black")
                
                # Add RGB values
                if "rgb" in color_info:
                    rgb_text = f"RGB: {color_info['rgb']['r']},{color_info['rgb']['g']},{color_info['rgb']['b']}"
                    draw.text((x0 + 10, height - 50), rgb_text, fill="black")
            
            # Save image
            output_path = output_dir / filename
            img.save(output_path, "PNG")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Palette image creation error: {e}")
            # Create simple palette image as fallback
            return await self._create_simple_palette(colors, output_dir, filename)
    
    async def _create_simple_palette(self, colors: List[Dict[str, Any]],
                                    output_dir: Path, filename: str) -> Path:
        """Create simple palette image (fallback)"""
        from PIL import Image, ImageDraw
        
        width = 400
        height = 100
        img = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(img)
        
        num_colors = len(colors)
        swatch_width = width // num_colors
        
        for i, color_info in enumerate(colors):
            # Get color
            if "hex" in color_info:
                hex_color = color_info["hex"].lstrip("#")
                color = tuple(int(hex_color[j:j+2], 16) for j in (0, 2, 4))
            else:
                color = (255, 255, 255)
            
            # Draw swatch
            x0 = i * swatch_width
            x1 = x0 + swatch_width
            draw.rectangle([x0, 0, x1, height], fill=color)
        
        output_path = output_dir / filename
        img.save(output_path, "PNG")
        
        return output_path
    
    async def generate_color_scheme(self, base_color: str, 
                                   scheme_type: str = "monochromatic") -> List[Dict[str, Any]]:
        """Generate color scheme from base color"""
        try:
            # Parse base color
            if base_color.startswith("#"):
                hex_color = base_color.lstrip("#")
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
            else:
                # Assume RGB tuple
                r, g, b = base_color
            
            # Generate scheme based on type
            if scheme_type == "monochromatic":
                colors = self._generate_monochromatic(r, g, b)
            elif scheme_type == "analogous":
                colors = self._generate_analogous(r, g, b)
            elif scheme_type == "complementary":
                colors = self._generate_complementary(r, g, b)
            elif scheme_type == "triadic":
                colors = self._generate_triadic(r, g, b)
            elif scheme_type == "tetradic":
                colors = self._generate_tetradic(r, g, b)
            else:
                colors = self._generate_monochromatic(r, g, b)
            
            # Convert to requested format
            formatted_colors = []
            for color in colors:
                color_dict = self._format_color(color, "hex")
                formatted_colors.append(color_dict)
            
            return formatted_colors
            
        except Exception as e:
            logger.error(f"Color scheme generation error: {e}")
            return []
    
    def _generate_monochromatic(self, r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Generate monochromatic color scheme"""
        colors = [(r, g, b)]
        
        # Generate lighter shades
        for i in range(1, 3):
            light_r = min(255, r + 30 * i)
            light_g = min(255, g + 30 * i)
            light_b = min(255, b + 30 * i)
            colors.append((light_r, light_g, light_b))
        
        # Generate darker shades
        for i in range(1, 3):
            dark_r = max(0, r - 30 * i)
            dark_g = max(0, g - 30 * i)
            dark_b = max(0, b - 30 * i)
            colors.append((dark_r, dark_g, dark_b))
        
        return colors[:5]  # Return 5 colors
    
    def _generate_analogous(self, r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Generate analogous color scheme"""
        # Convert to HSL for easier manipulation
        hsl = self._rgb_to_hsl(r, g, b)
        h = hsl["h"]
        
        colors = [(r, g, b)]
        
        # Generate analogous colors (±30 degrees)
        for angle in [-30, -15, 15, 30]:
            new_h = (h + angle) % 360
            new_rgb = self._hsl_to_rgb(new_h, hsl["s"], hsl["l"])
            colors.append(new_rgb)
        
        return colors[:5]
    
    def _generate_complementary(self, r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Generate complementary color scheme"""
        hsl = self._rgb_to_hsl(r, g, b)
        h = hsl["h"]
        
        # Complementary color (180 degrees opposite)
        comp_h = (h + 180) % 360
        comp_rgb = self._hsl_to_rgb(comp_h, hsl["s"], hsl["l"])
        
        # Return base, complementary, and some variations
        return [
            (r, g, b),
            comp_rgb,
            self._adjust_lightness(r, g, b, 1.2),
            self._adjust_lightness(comp_rgb[0], comp_rgb[1], comp_rgb[2], 1.2),
            self._adjust_lightness(r, g, b, 0.8)
        ]
    
    def _generate_triadic(self, r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Generate triadic color scheme"""
        hsl = self._rgb_to_hsl(r, g, b)
        h = hsl["h"]
        
        # Triadic colors (120 degrees apart)
        triad1_h = (h + 120) % 360
        triad2_h = (h + 240) % 360
        
        triad1_rgb = self._hsl_to_rgb(triad1_h, hsl["s"], hsl["l"])
        triad2_rgb = self._hsl_to_rgb(triad2_h, hsl["s"], hsl["l"])
        
        return [
            (r, g, b),
            triad1_rgb,
            triad2_rgb,
            self._adjust_lightness(r, g, b, 1.3),
            self._adjust_lightness(triad1_rgb[0], triad1_rgb[1], triad1_rgb[2], 0.7)
        ]
    
    def _generate_tetradic(self, r: int, g: int, b: int) -> List[Tuple[int, int, int]]:
        """Generate tetradic (rectangle) color scheme"""
        hsl = self._rgb_to_hsl(r, g, b)
        h = hsl["h"]
        
        # Tetradic colors (90, 180, 270 degrees)
        colors = [(r, g, b)]
        
        for angle in [90, 180, 270]:
            new_h = (h + angle) % 360
            new_rgb = self._hsl_to_rgb(new_h, hsl["s"], hsl["l"])
            colors.append(new_rgb)
        
        # Add a lighter version of base color
        colors.append(self._adjust_lightness(r, g, b, 1.2))
        
        return colors
    
    def _hsl_to_rgb(self, h: float, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL to RGB"""
        s /= 100.0
        l /= 100.0
        
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = l - c / 2
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)
        
        return (r, g, b)
    
    def _adjust_lightness(self, r: int, g: int, b: int, factor: float) -> Tuple[int, int, int]:
        """Adjust color lightness"""
        hsl = self._rgb_to_hsl(r, g, b)
        new_l = min(100, max(0, hsl["l"] * factor))
        
        return self._hsl_to_rgb(hsl["h"], hsl["s"], new_l)
