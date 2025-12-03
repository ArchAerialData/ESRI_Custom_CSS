#!/usr/bin/env python3
"""
Terra OBJ Viewer Generator

Command-line tool to generate standalone HTML viewers for OBJ models.

Usage:
    python generate_obj_viewer.py input_folder/ -o output.html

Features:
- Multi-file OBJ support (automatically merges multiple .obj files)
- Material library (MTL) support
- Texture embedding with Base64 encoding
- Optional texture downscaling
- Optional WebP conversion for smaller file size

Requirements:
    pip install Pillow
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from modules.obj_parser import OBJParser
from modules.mtl_parser import MTLParser
from modules.texture_processor import TextureProcessor, format_bytes
from modules.html_generator import HTMLGenerator


def find_model_files(input_path: Path) -> dict:
    """
    Find all model-related files in input path.

    Args:
        input_path: File or directory path

    Returns:
        Dict with 'obj_files', 'mtl_file', 'texture_files'
    """
    result = {
        'obj_files': [],
        'mtl_file': None,
        'texture_files': []
    }

    if input_path.is_file():
        # Single file mode
        if input_path.suffix.lower() == '.obj':
            result['obj_files'] = [input_path]
            # Look for MTL in same directory
            result['mtl_file'] = OBJParser.find_mtl_file(input_path)
        else:
            raise ValueError(f"Input file must be .obj, got: {input_path.suffix}")

    elif input_path.is_dir():
        # Directory mode - find all OBJ files
        result['obj_files'] = OBJParser.find_obj_files(input_path)

        if not result['obj_files']:
            raise FileNotFoundError(f"No .obj files found in: {input_path}")

        # Look for MTL file
        mtl_files = list(input_path.glob('*.mtl'))
        if mtl_files:
            result['mtl_file'] = mtl_files[0]

        # Find all texture files
        for ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
            result['texture_files'].extend(input_path.glob(f'*{ext}'))
            result['texture_files'].extend(input_path.glob(f'*{ext.upper()}'))

    else:
        raise FileNotFoundError(f"Input path not found: {input_path}")

    return result


def generate_viewer(input_path: Path,
                   output_path: Path,
                   max_texture_size: Optional[int] = None,
                   convert_to_webp: bool = False,
                   jpeg_quality: int = 85,
                   title: Optional[str] = None,
                   verbose: bool = False) -> Path:
    """
    Generate standalone OBJ viewer HTML file.

    Args:
        input_path: Path to .obj file or directory containing model files
        output_path: Where to save generated HTML
        max_texture_size: Maximum texture dimension (None = no downscaling)
        convert_to_webp: Convert textures to WebP
        jpeg_quality: JPEG compression quality (1-100)
        title: Custom page title
        verbose: Print detailed progress

    Returns:
        Path to generated HTML file
    """
    print(f"🔍 Scanning for model files in: {input_path}")

    # Find all model files
    files = find_model_files(input_path)

    print(f"✓ Found {len(files['obj_files'])} OBJ file(s)")
    if files['mtl_file']:
        print(f"✓ Found MTL file: {files['mtl_file'].name}")
    if files['texture_files']:
        print(f"✓ Found {len(files['texture_files'])} texture file(s)")

    # Parse OBJ files
    print(f"\n📦 Processing OBJ geometry...")
    obj_parser = OBJParser()

    if len(files['obj_files']) == 1:
        obj_data = obj_parser.parse_file(files['obj_files'][0])
    else:
        print(f"   Merging {len(files['obj_files'])} OBJ files...")
        obj_data = obj_parser.parse_files(files['obj_files'])

    stats = obj_parser.get_stats()
    print(f"✓ Vertices: {stats['vertices']:,}")
    print(f"✓ Faces: {stats['faces']:,}")
    print(f"✓ Normals: {stats['normals']:,}")
    print(f"✓ Texture Coords: {stats['texcoords']:,}")

    # Parse MTL file
    mtl_data = ""
    mtl_parser = MTLParser()
    texture_paths = set()

    if files['mtl_file']:
        print(f"\n🎨 Processing materials...")
        mtl_parser.parse_file(files['mtl_file'])
        print(f"✓ Materials: {len(mtl_parser.materials)}")

        # Get texture paths from MTL
        texture_paths = mtl_parser.get_all_texture_paths()

        if texture_paths:
            print(f"✓ Textures referenced: {len(texture_paths)}")
            if verbose:
                for tex in texture_paths:
                    print(f"    - {tex}")

    # Process textures
    texture_data = {}

    if files['texture_files'] or texture_paths:
        print(f"\n🖼️  Processing textures...")

        processor = TextureProcessor(
            max_resolution=max_texture_size,
            convert_to_webp=convert_to_webp,
            jpeg_quality=jpeg_quality
        )

        # Match texture files to MTL references
        textures_to_process = {}

        for tex_path in files['texture_files']:
            # Check if this texture is referenced in MTL
            tex_name = tex_path.name
            # Also check without directory paths
            tex_basename = Path(tex_name).name

            if tex_name in texture_paths or tex_basename in texture_paths:
                textures_to_process[tex_name] = tex_path
            elif not texture_paths:
                # If no MTL, include all textures
                textures_to_process[tex_name] = tex_path

        if not textures_to_process:
            print("⚠️  Warning: No matching textures found for MTL references")
        else:
            for tex_name, tex_path in textures_to_process.items():
                print(f"   Processing: {tex_name}...")
                result = processor.process_texture(tex_path)

                if verbose:
                    print(f"      Original: {format_bytes(result['original_size'])}")
                    print(f"      Encoded: {format_bytes(result['encoded_size'])}")
                    print(f"      Dimensions: {result['original_dimensions']}")
                    if result['downscaled']:
                        print(f"      Downscaled to: {result['dimensions']}")

                # Use basename for texture reference
                tex_key = Path(tex_name).name
                texture_data[tex_key] = result['data_uri']

            tex_stats = processor.get_stats_summary()
            print(f"✓ Textures processed: {tex_stats['files_processed']}")
            print(f"✓ Total size: {tex_stats['total_encoded_size_mb']:.2f} MB (Base64)")

    # Update MTL with texture data URIs
    if files['mtl_file'] and texture_data:
        print(f"\n🔗 Updating material texture references...")
        mtl_parser.update_texture_paths(texture_data)

    # Generate MTL string
    if files['mtl_file']:
        mtl_data = mtl_parser.to_mtl_string()

    # Generate HTML
    print(f"\n📄 Generating HTML viewer...")

    generator = HTMLGenerator()

    # Use input filename as default title if not provided
    if title is None:
        if input_path.is_file():
            title = f"Terra Viewer - {input_path.stem}"
        else:
            title = f"Terra Viewer - {input_path.name}"

    output_file = generator.generate_obj_viewer(
        obj_data=obj_data,
        mtl_data=mtl_data,
        textures=texture_data,
        output_path=output_path,
        title=title
    )

    output_size = output_file.stat().st_size
    print(f"✓ Generated: {output_file}")
    print(f"✓ File size: {format_bytes(output_size)}")

    if output_size > 50 * 1024 * 1024:  # 50 MB
        print(f"⚠️  Warning: Large file size ({format_bytes(output_size)})")
        print(f"   Consider using texture downscaling: --max-texture-size 2048")

    return output_file


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate standalone HTML viewer for OBJ models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - single file
  python generate_obj_viewer.py model.obj -o viewer.html

  # Directory with multiple OBJ files
  python generate_obj_viewer.py model_folder/ -o viewer.html

  # With texture downscaling
  python generate_obj_viewer.py model.obj -o viewer.html --max-texture-size 2048

  # Convert textures to WebP for smaller size
  python generate_obj_viewer.py model.obj -o viewer.html --webp

  # Custom title and JPEG quality
  python generate_obj_viewer.py model.obj -o viewer.html --title "My Model" --jpeg-quality 90
        """
    )

    parser.add_argument('input', type=Path,
                       help='Path to .obj file or directory containing model files')
    parser.add_argument('-o', '--output', type=Path, required=True,
                       help='Output HTML file path')
    parser.add_argument('--max-texture-size', type=int, metavar='PIXELS',
                       help='Maximum texture dimension (e.g., 2048). Downscales larger textures.')
    parser.add_argument('--webp', action='store_true',
                       help='Convert textures to WebP format for smaller file size')
    parser.add_argument('--jpeg-quality', type=int, default=85, metavar='1-100',
                       help='JPEG compression quality (default: 85)')
    parser.add_argument('--title', type=str,
                       help='Custom page title (default: auto-generated from filename)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print detailed progress information')

    args = parser.parse_args()

    # Validate arguments
    if args.jpeg_quality < 1 or args.jpeg_quality > 100:
        parser.error("JPEG quality must be between 1 and 100")

    if not args.input.exists():
        parser.error(f"Input path not found: {args.input}")

    try:
        print("=" * 60)
        print("Terra OBJ Viewer Generator")
        print("=" * 60)

        output_file = generate_viewer(
            input_path=args.input,
            output_path=args.output,
            max_texture_size=args.max_texture_size,
            convert_to_webp=args.webp,
            jpeg_quality=args.jpeg_quality,
            title=args.title,
            verbose=args.verbose
        )

        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"\nOpen in browser: {output_file.absolute()}")

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
