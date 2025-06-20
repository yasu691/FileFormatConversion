import os
from pydub import AudioSegment
from typing import Optional, Dict, Any
from .utils import validate_file, get_file_format, create_output_path, format_file_size


class AudioConverter:
    """pydubを使用した音声形式変換を処理するクラス。"""
    
    SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'ogg', 'aac', 'm4a']
    
    def __init__(self):
        self.format_options = {
            'mp3': {'bitrate': '192k'},
            'ogg': {'bitrate': '192k'},
            'aac': {'bitrate': '192k'},
            'm4a': {'bitrate': '192k'},
        }
    
    def convert(self, input_path: str, output_format: str, output_path: Optional[str] = None,
                bitrate: Optional[str] = None, sample_rate: Optional[int] = None, **kwargs) -> bool:
        """音声ファイルを指定された形式に変換します。"""
        
        if not validate_file(input_path):
            raise FileNotFoundError(f"Input file not found or not readable: {input_path}")
        
        input_format = get_file_format(input_path)
        if input_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported input format: {input_format}. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")
        
        if output_format.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output format: {output_format}. Supported formats: {', '.join(self.SUPPORTED_FORMATS)}")
        
        output_file = create_output_path(input_path, output_format, output_path)
        
        try:
            audio = AudioSegment.from_file(input_path)
            
            if sample_rate:
                audio = audio.set_frame_rate(sample_rate)
            
            export_kwargs = self.format_options.get(output_format.lower(), {}).copy()
            
            if bitrate:
                export_kwargs['bitrate'] = bitrate
            
            export_kwargs.update(kwargs)
            
            if output_format.lower() == 'wav':
                export_kwargs.pop('bitrate', None)
            
            audio.export(output_file, format=output_format.lower(), **export_kwargs)
            
            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_file)
            
            print(f"✓ Converted {input_path} → {output_file}")
            print(f"  Size: {format_file_size(input_size)} → {format_file_size(output_size)}")
            print(f"  Duration: {len(audio) / 1000:.1f}s")
            
            return True
            
        except Exception as e:
            raise RuntimeError(f"Failed to convert audio: {str(e)}")
    
    def get_audio_info(self, file_path: str) -> Dict[str, Any]:
        """音声ファイルの情報を取得します。"""
        if not validate_file(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            audio = AudioSegment.from_file(file_path)
            return {
                'duration_seconds': len(audio) / 1000,
                'frame_rate': audio.frame_rate,
                'channels': audio.channels,
                'sample_width': audio.sample_width,
                'file_size': format_file_size(os.path.getsize(file_path))
            }
        except Exception as e:
            raise RuntimeError(f"Failed to read audio info: {str(e)}")
