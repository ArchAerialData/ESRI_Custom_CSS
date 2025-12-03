"""
Texture Processor Module

Handles image file encoding, optimization, and Base64 conversion
for embedding textures in standalone HTML files.

Supports:
- JPEG, PNG, WebP, BMP formats
- Base64 data URI encoding
- Image downscaling (resolution reduction)
- Format conversion (JPEG ↔ WebP)
- Compression optimization
"""

import base64
import io
from pathlib import Path
from typing import Optional, Tuple, Dict
from PIL import Image


class TextureProcessor:
    """Process and encode texture images for HTML embedding."""

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

    def __init__(self, max_resolution: Optional[int] = None,
                 convert_to_webp: bool = False,
                 jpeg_quality: int = 85,
                 webp_quality: int = 80):
        """
        Initialize texture processor.

        Args:
            max_resolution: Maximum texture dimension (e.g., 2048). None = no downscaling
            convert_to_webp: Convert all textures to WebP for smaller size
            jpeg_quality: JPEG compression quality (1-100)
            webp_quality: WebP compression quality (1-100)
        """
        self.max_resolution = max_resolution
        self.convert_to_webp = convert_to_webp
        self.jpeg_quality = jpeg_quality
        self.webp_quality = webp_quality

        self.stats = {
            'processed': 0,
            'total_original_size': 0,
            'total_encoded_size': 0,
            'downscaled_count': 0,
            'converted_count': 0
        }

    def process_texture(self, image_path: Path) -> Dict[str, any]:
        """
        Process a single texture file.

        Args:
            image_path: Path to image file

        Returns:
            Dict with keys:
                - 'data_uri': Base64 encoded data URI
                - 'original_size': Original file size in bytes
                - 'encoded_size': Encoded data URI size in bytes
                - 'format': Image format (jpeg, png, webp)
                - 'dimensions': (width, height) tuple
                - 'downscaled': Boolean, was image downscaled
                - 'converted': Boolean, was format converted

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format not supported
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Texture file not found: {image_path}")

        if image_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {image_path.suffix}")

        # Track original size
        original_size = image_path.stat().st_size
        self.stats['total_original_size'] += original_size

        # Open image
        img = Image.open(image_path)
        original_dimensions = img.size
        downscaled = False
        converted = False

        # Downscale if needed
        if self.max_resolution and max(img.size) > self.max_resolution:
            img = self._downscale_image(img, self.max_resolution)
            downscaled = True
            self.stats['downscaled_count'] += 1

        # Determine output format
        if self.convert_to_webp:
            output_format = 'webp'
            mime_type = 'image/webp'
            quality = self.webp_quality
            converted = True
            self.stats['converted_count'] += 1
        elif image_path.suffix.lower() in {'.jpg', '.jpeg'}:
            output_format = 'jpeg'
            mime_type = 'image/jpeg'
            quality = self.jpeg_quality
        elif image_path.suffix.lower() == '.png':
            output_format = 'png'
            mime_type = 'image/png'
            quality = None  # PNG doesn't use quality parameter
        elif image_path.suffix.lower() == '.webp':
            output_format = 'webp'
            mime_type = 'image/webp'
            quality = self.webp_quality
        else:
            # Convert unsupported formats to JPEG
            output_format = 'jpeg'
            mime_type = 'image/jpeg'
            quality = self.jpeg_quality
            converted = True

        # Encode to Base64
        data_uri = self._encode_image_to_data_uri(img, output_format, mime_type, quality)
        encoded_size = len(data_uri)
        self.stats['total_encoded_size'] += encoded_size
        self.stats['processed'] += 1

        return {
            'data_uri': data_uri,
            'original_size': original_size,
            'encoded_size': encoded_size,
            'format': output_format,
            'dimensions': img.size,
            'downscaled': downscaled,
            'converted': converted,
            'original_dimensions': original_dimensions
        }

    def process_textures_batch(self, image_paths: list[Path]) -> Dict[str, Dict]:
        """
        Process multiple texture files.

        Args:
            image_paths: List of paths to image files

        Returns:
            Dict mapping filename to processing results
        """
        results = {}

        for image_path in image_paths:
            try:
                result = self.process_texture(image_path)
                results[image_path.name] = result
            except Exception as e:
                print(f"Warning: Failed to process {image_path.name}: {e}")
                results[image_path.name] = {'error': str(e)}

        return results

    def _downscale_image(self, img: Image.Image, max_size: int) -> Image.Image:
        """
        Downscale image to fit within max_size while maintaining aspect ratio.

        Args:
            img: PIL Image object
            max_size: Maximum dimension (width or height)

        Returns:
            Downscaled PIL Image
        """
        width, height = img.size

        if max(width, height) <= max_size:
            return img

        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        # Use high-quality Lanczos resampling
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def _encode_image_to_data_uri(self, img: Image.Image,
                                   format: str, mime_type: str,
                                   quality: Optional[int]) -> str:
        """
        Encode PIL Image to Base64 data URI.

        Args:
            img: PIL Image object
            format: Output format (jpeg, png, webp)
            mime_type: MIME type for data URI
            quality: Compression quality (None for PNG)

        Returns:
            Base64 data URI string
        """
        buffer = io.BytesIO()

        # Convert RGBA to RGB for JPEG/WebP if needed
        if format in {'jpeg', 'webp'} and img.mode in {'RGBA', 'LA', 'P'}:
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in {'RGBA', 'LA'} else None)
            img = background

        # Save to buffer
        save_kwargs = {'format': format.upper()}
        if quality is not None:
            save_kwargs['quality'] = quality
        if format == 'png':
            save_kwargs['optimize'] = True

        img.save(buffer, **save_kwargs)

        # Encode to Base64
        image_data = buffer.getvalue()
        base64_data = base64.b64encode(image_data).decode('utf-8')

        return f"data:{mime_type};base64,{base64_data}"

    def get_stats_summary(self) -> Dict[str, any]:
        """
        Get processing statistics.

        Returns:
            Dict with processing stats
        """
        compression_ratio = 0
        if self.stats['total_original_size'] > 0:
            compression_ratio = (1 - (self.stats['total_encoded_size'] /
                                     (self.stats['total_original_size'] * 1.37))) * 100
            # Note: Base64 adds ~37% overhead, so we factor that out

        return {
            'files_processed': self.stats['processed'],
            'total_original_size_mb': self.stats['total_original_size'] / (1024 * 1024),
            'total_encoded_size_mb': self.stats['total_encoded_size'] / (1024 * 1024),
            'downscaled_count': self.stats['downscaled_count'],
            'converted_count': self.stats['converted_count'],
            'compression_ratio_percent': compression_ratio
        }


def format_bytes(bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"


# Example usage
if __name__ == "__main__":
    # Example: Process a texture with downscaling
    processor = TextureProcessor(
        max_resolution=2048,
        convert_to_webp=False,
        jpeg_quality=85
    )

    # Process single texture
    # result = processor.process_texture(Path("texture.jpg"))
    # print(f"Original: {format_bytes(result['original_size'])}")
    # print(f"Encoded: {format_bytes(result['encoded_size'])}")
    # print(f"Data URI length: {len(result['data_uri'])}")

    print("TextureProcessor module loaded successfully")
    print(f"Supported formats: {', '.join(TextureProcessor.SUPPORTED_FORMATS)}")
