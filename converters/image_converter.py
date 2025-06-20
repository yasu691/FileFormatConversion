import os
from PIL import Image
from typing import Optional, Dict, Any
from .utils import validate_file, get_file_format, create_output_path, format_file_size


class ImageConverter:
    """Handles image format conversion using Pillow."""
    
    SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif', 'webp']
    
    def __init__(self):
        self.format_options = {
            'jpeg': {'quality': 95, 'optimize': True},
            'jpg': {'quality': 95, 'optimize': True},
            'png': {'optimize': True},
            'webp': {'quality': 95, 'method': 6},
        }
    
    def convert(self, input_path: str, output_format: str, output_path: Optional[str] = None, 
                quality: Optional[int] = None, **kwargs) -> bool:
        """Convert an image file to the specified format."""
        
        if not validate_file(input_path):
            raise FileNotFoundError(f"Input file not found or not readable: {input_path}")
        
        input_format = get_file_format(input_path)
        if input_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported input format: {input_format}. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")
        
        if output_format.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output format: {output_format}. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")
        
        output_file = create_output_path(input_path, output_format, output_path)
        
        try:
            with Image.open(input_path) as img:
                if img.mode == 'RGBA' and output_format.lower() in ['jpg', 'jpeg']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                
                save_kwargs = self.format_options.get(output_format.lower(), {}).copy()
                
                if quality is not None:
                    if output_format.lower() in ['jpg', 'jpeg', 'webp']:
                        save_kwargs['quality'] = quality
                
                save_kwargs.update(kwargs)
                
                format_mapping = {
                    'jpg': 'JPEG',
                    'jpeg': 'JPEG',
                    'tif': 'TIFF',
                    'tiff': 'TIFF'
                }
                pillow_format = format_mapping.get(output_format.lower(), output_format.upper())
                img.save(output_file, format=pillow_format, **save_kwargs)
                
                input_size = os.path.getsize(input_path)
                output_size = os.path.getsize(output_file)
                
                print(f"✓ Converted {input_path} → {output_file}")
                print(f"  Size: {format_file_size(input_size)} → {format_file_size(output_size)}")
                
                return True
                
        except Exception as e:
            raise RuntimeError(f"Failed to convert image: {str(e)}")
    
    def get_image_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about an image file."""
        if not validate_file(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with Image.open(file_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height,
                    'file_size': format_file_size(os.path.getsize(file_path))
                }
        except Exception as e:
            raise RuntimeError(f"Failed to read image info: {str(e)}")
