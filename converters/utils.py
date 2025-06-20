import os
from pathlib import Path
from typing import Optional, Tuple


def validate_file(file_path: str) -> bool:
    """Validate that a file exists and is readable."""
    if not os.path.exists(file_path):
        return False
    if not os.path.isfile(file_path):
        return False
    if not os.access(file_path, os.R_OK):
        return False
    return True


def get_file_format(file_path: str) -> str:
    """Get the file format from the file extension."""
    return Path(file_path).suffix.lower().lstrip('.')


def create_output_path(input_path: str, output_format: str, output_path: Optional[str] = None) -> str:
    """Create output file path based on input path and target format."""
    if output_path:
        return output_path
    
    input_path_obj = Path(input_path)
    output_filename = f"{input_path_obj.stem}.{output_format.lower()}"
    return str(input_path_obj.parent / output_filename)


def get_supported_formats() -> Tuple[list, list]:
    """Get lists of supported image and audio formats."""
    image_formats = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif', 'webp']
    audio_formats = ['mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a']
    return image_formats, audio_formats


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"
