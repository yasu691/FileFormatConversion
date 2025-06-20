# FileFormatConversion

画像と音声ファイルの形式を変換するPython CLIツールです。

## 機能

- **画像変換**: PNG, JPEG, GIF, BMP, TIFF, WebP形式をサポート
- **音声変換**: MP3, WAV, FLAC, OGG, AAC, M4A形式をサポート
- **バッチ変換**: ディレクトリ内の複数ファイルを一括変換
- **品質設定**: JPEG/WebP画像の品質調整、音声のビットレート設定
- **ファイル情報表示**: 変換前にファイルの詳細情報を確認

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yasu691/FileFormatConversion.git
cd FileFormatConversion

# 依存関係をインストール
pip install -r requirements.txt

# パッケージをインストール（オプション）
pip install -e .
```

## 使用方法

### 基本的な使用方法

```bash
# 画像変換
python file_converter.py convert-image input.png jpg
python file_converter.py convert-image photo.jpeg png -o converted.png
python file_converter.py convert-image image.jpg webp -q 80

# 音声変換
python file_converter.py convert-audio song.wav mp3
python file_converter.py convert-audio audio.mp3 flac -o high_quality.flac
python file_converter.py convert-audio music.wav mp3 -b 320k -r 48000

# ファイル情報表示
python file_converter.py info image.jpg
python file_converter.py info audio.mp3

# サポートされている形式一覧
python file_converter.py formats
```

### バッチ変換

```bash
# ディレクトリ内の全画像をPNGに変換
python file_converter.py batch-convert ./images png --type image

# ディレクトリ内の全音声をMP3に変換（192kビットレート）
python file_converter.py batch-convert ./music mp3 --type audio -b 192k
```

### オプション

#### 画像変換オプション
- `-o, --output`: 出力ファイルパス
- `-q, --quality`: JPEG/WebPの品質（1-100）
- `--info`: 変換前にファイル情報を表示

#### 音声変換オプション
- `-o, --output`: 出力ファイルパス
- `-b, --bitrate`: ビットレート（例: 192k, 320k）
- `-r, --sample-rate`: サンプルレート（例: 44100, 48000）
- `--info`: 変換前にファイル情報を表示

## サポートされている形式

### 画像形式
- PNG
- JPEG/JPG
- GIF
- BMP
- TIFF/TIF
- WebP

### 音声形式
- MP3
- WAV
- FLAC
- OGG
- AAC
- M4A

## 依存関係

- Python 3.8+
- Pillow (画像処理)
- pydub (音声処理)
- click (CLI フレームワーク)

## 例

```bash
# 高品質JPEG変換
python file_converter.py convert-image photo.png jpg -q 95

# 高音質音声変換
python file_converter.py convert-audio song.wav flac

# ファイル情報確認後に変換
python file_converter.py convert-image image.jpg png --info

# バッチ変換で出力ディレクトリ指定
python file_converter.py batch-convert ./input png --type image -o ./output
```

## ライセンス

MIT License
