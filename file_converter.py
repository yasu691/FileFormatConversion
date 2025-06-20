#!/usr/bin/env python3
"""
ファイル形式変換CLIツール

画像と音声ファイルの形式を変換するコマンドラインツールです。
PNG、JPEG、GIF、MP3、WAV、FLACなどの一般的な形式をサポートしています。
"""

import click
import os
import sys
from pathlib import Path
from typing import List

from converters import ImageConverter, AudioConverter
from converters.utils import get_supported_formats, validate_file


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """ファイル形式変換ツール - 画像と音声ファイルを異なる形式間で変換します。"""
    pass


@cli.command('convert-image')
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_format', type=str)
@click.option('-o', '--output', type=str, help='出力ファイルパス（オプション）')
@click.option('-q', '--quality', type=int, help='JPEG/WebPの品質（1-100）')
@click.option('--info', is_flag=True, help='変換前に画像情報を表示')
def convert_image(input_file: str, output_format: str, output: str, quality: int, info: bool):
    """画像ファイルを異なる形式に変換します。
    
    INPUT_FILE: 入力画像ファイルのパス
    OUTPUT_FORMAT: 対象形式 (png, jpg, jpeg, gif, bmp, tiff, webp)
    
    使用例:
        file-converter convert-image photo.png jpg
        file-converter convert-image image.jpg png -o converted.png
        file-converter convert-image photo.jpeg webp -q 80
    """
    try:
        converter = ImageConverter()
        
        if info:
            image_info = converter.get_image_info(input_file)
            click.echo(f"\n画像情報:")
            click.echo(f"  形式: {image_info['format']}")
            click.echo(f"  サイズ: {image_info['width']}x{image_info['height']}")
            click.echo(f"  モード: {image_info['mode']}")
            click.echo(f"  ファイルサイズ: {image_info['file_size']}")
            click.echo()
        
        converter.convert(input_file, output_format, output, quality=quality)
        click.echo("✓ 画像変換が正常に完了しました！")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command('convert-audio')
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_format', type=str)
@click.option('-o', '--output', type=str, help='出力ファイルパス（オプション）')
@click.option('-b', '--bitrate', type=str, help='ビットレート（例: 192k, 320k）')
@click.option('-r', '--sample-rate', type=int, help='サンプルレート（Hz）（例: 44100, 48000）')
@click.option('--info', is_flag=True, help='変換前に音声情報を表示')
def convert_audio(input_file: str, output_format: str, output: str, bitrate: str, sample_rate: int, info: bool):
    """音声ファイルを異なる形式に変換します。
    
    INPUT_FILE: 入力音声ファイルのパス
    OUTPUT_FORMAT: 対象形式 (mp3, wav, flac, ogg, aac, m4a)
    
    使用例:
        file-converter convert-audio song.wav mp3
        file-converter convert-audio audio.mp3 flac -o high_quality.flac
        file-converter convert-audio music.wav mp3 -b 320k -r 48000
    """
    try:
        converter = AudioConverter()
        
        if info:
            audio_info = converter.get_audio_info(input_file)
            click.echo(f"\n音声情報:")
            click.echo(f"  再生時間: {audio_info['duration_seconds']:.1f}秒")
            click.echo(f"  サンプルレート: {audio_info['frame_rate']}Hz")
            click.echo(f"  チャンネル数: {audio_info['channels']}")
            click.echo(f"  サンプル幅: {audio_info['sample_width']} バイト")
            click.echo(f"  ファイルサイズ: {audio_info['file_size']}")
            click.echo()
        
        converter.convert(input_file, output_format, output, bitrate=bitrate, sample_rate=sample_rate)
        click.echo("✓ 音声変換が正常に完了しました！")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command('batch-convert')
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('output_format', type=str)
@click.option('--type', 'file_type', type=click.Choice(['image', 'audio']), required=True,
              help='Type of files to convert')
@click.option('-o', '--output-dir', type=str, help='Output directory (default: same as input)')
@click.option('-q', '--quality', type=int, help='Quality for image formats (1-100)')
@click.option('-b', '--bitrate', type=str, help='Bitrate for audio formats (e.g., 192k)')
def batch_convert(input_dir: str, output_format: str, file_type: str, output_dir: str, quality: int, bitrate: str):
    """Batch convert all files in a directory.
    
    INPUT_DIR: Directory containing files to convert
    OUTPUT_FORMAT: Target format
    
    Examples:
        file-converter batch-convert ./images png --type image
        file-converter batch-convert ./music mp3 --type audio -b 192k
    """
    try:
        input_path = Path(input_dir)
        output_path = Path(output_dir) if output_dir else input_path
        
        if file_type == 'image':
            converter = ImageConverter()
            supported_formats = converter.SUPPORTED_FORMATS
        else:
            converter = AudioConverter()
            supported_formats = converter.SUPPORTED_FORMATS
        
        files_to_convert = []
        for file_path in input_path.iterdir():
            if file_path.is_file():
                file_ext = file_path.suffix.lower().lstrip('.')
                if file_ext in supported_formats:
                    files_to_convert.append(file_path)
        
        if not files_to_convert:
            click.echo(f"No {file_type} files found in {input_dir}")
            return
        
        click.echo(f"Found {len(files_to_convert)} {file_type} files to convert...")
        
        success_count = 0
        for file_path in files_to_convert:
            try:
                output_file = output_path / f"{file_path.stem}.{output_format}"
                
                if file_type == 'image':
                    converter.convert(str(file_path), output_format, str(output_file), quality=quality)
                else:
                    converter.convert(str(file_path), output_format, str(output_file), bitrate=bitrate)
                
                success_count += 1
            except Exception as e:
                click.echo(f"❌ Failed to convert {file_path.name}: {str(e)}", err=True)
        
        click.echo(f"\n✓ Batch conversion completed! {success_count}/{len(files_to_convert)} files converted successfully.")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command('formats')
def list_formats():
    """List all supported file formats."""
    image_formats, audio_formats = get_supported_formats()
    
    click.echo("Supported Image Formats:")
    click.echo("  " + ", ".join(image_formats))
    click.echo()
    click.echo("Supported Audio Formats:")
    click.echo("  " + ", ".join(audio_formats))


@cli.command('info')
@click.argument('file_path', type=click.Path(exists=True))
def file_info(file_path: str):
    """Get detailed information about an image or audio file."""
    try:
        file_ext = Path(file_path).suffix.lower().lstrip('.')
        image_formats, audio_formats = get_supported_formats()
        
        if file_ext in image_formats:
            converter = ImageConverter()
            info = converter.get_image_info(file_path)
            click.echo(f"\nImage File: {file_path}")
            click.echo(f"  Format: {info['format']}")
            click.echo(f"  Dimensions: {info['width']}x{info['height']}")
            click.echo(f"  Mode: {info['mode']}")
            click.echo(f"  File Size: {info['file_size']}")
            
        elif file_ext in audio_formats:
            converter = AudioConverter()
            info = converter.get_audio_info(file_path)
            click.echo(f"\nAudio File: {file_path}")
            click.echo(f"  Duration: {info['duration_seconds']:.1f}s")
            click.echo(f"  Sample Rate: {info['frame_rate']}Hz")
            click.echo(f"  Channels: {info['channels']}")
            click.echo(f"  Sample Width: {info['sample_width']} bytes")
            click.echo(f"  File Size: {info['file_size']}")
            
        else:
            click.echo(f"❌ Unsupported file format: {file_ext}")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
