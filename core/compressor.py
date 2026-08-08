from PIL import Image
from pathlib import Path

def compress_jpeg(input_path, output_path, quality=85):
    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True, subsampling=0)

def compress_png(input_path, output_path, quality=85):
    img = Image.open(input_path)
    img.save(output_path, 'PNG', optimize=True, compress_level=9)

def compress_webp(input_path, output_path, quality=85):
    img = Image.open(input_path)
    img.save(output_path, 'WEBP', quality=quality, method=6)

def compress_image(input_path, output_path, fmt, quality=85):
    if fmt == 'JPEG':
        compress_jpeg(input_path, output_path, quality)
    elif fmt == 'PNG':
        compress_png(input_path, output_path, quality)
    elif fmt == 'WEBP':
        compress_webp(input_path, output_path, quality)
    else:
        # fallback – определяем по расширению
        ext = Path(input_path).suffix.lower()
        if ext in ('.jpg', '.jpeg'):
            compress_jpeg(input_path, output_path, quality)
        elif ext == '.png':
            compress_png(input_path, output_path, quality)
        elif ext == '.webp':
            compress_webp(input_path, output_path, quality)
        else:
            # на всякий случай конвертируем в JPEG
            img = Image.open(input_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=quality, optimize=True)