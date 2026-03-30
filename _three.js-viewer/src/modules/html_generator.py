"""
HTML Generator Module

Handles template loading and data injection for creating
standalone HTML viewers with embedded 3D models.

Supports:
- OBJ viewer template
- PLY viewer template
- Data placeholder replacement
- JavaScript string escaping
- JSON encoding for texture data
"""

from pathlib import Path
from typing import Dict, Optional
import json
import re


class HTMLGenerator:
    """Generate standalone HTML viewers from templates."""

    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize HTML generator.

        Args:
            template_dir: Directory containing viewer templates.
                         Defaults to src/templates/
        """
        if template_dir is None:
            # Default to src/templates relative to this file
            self.template_dir = Path(__file__).parent.parent / 'templates'
        else:
            self.template_dir = Path(template_dir)

        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {self.template_dir}")

    def generate_obj_viewer(self,
                           obj_data: str,
                           mtl_data: str,
                           textures: Dict[str, str],
                           output_path: Path,
                           title: str = "Terra 3D Model Viewer") -> Path:
        """
        Generate standalone OBJ viewer HTML file.

        Args:
            obj_data: OBJ geometry data as string
            mtl_data: MTL material data as string
            textures: Dict mapping texture filenames to data URIs
            output_path: Where to save generated HTML
            title: Page title

        Returns:
            Path to generated HTML file

        Raises:
            FileNotFoundError: If template not found
        """
        template_path = self.template_dir / 'viewer-obj.html'

        if not template_path.exists():
            raise FileNotFoundError(f"OBJ template not found: {template_path}")

        # Load template
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Replace placeholders
        html = html.replace('{{OBJ_DATA}}', self._escape_js_string(obj_data))
        html = html.replace('{{MTL_DATA}}', self._escape_js_string(mtl_data))
        html = html.replace('{{TEXTURE_DATA}}', json.dumps(textures, ensure_ascii=False))

        # Update title if provided
        if title:
            html = html.replace('<title>Terra 3D Model Viewer (OBJ)</title>',
                              f'<title>{self._escape_html(title)}</title>')

        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path

    def generate_ply_viewer(self,
                           ply_data: str,
                           output_path: Path,
                           title: str = "Terra Point Cloud Viewer") -> Path:
        """
        Generate standalone PLY viewer HTML file.

        Args:
            ply_data: PLY point cloud data as string
            output_path: Where to save generated HTML
            title: Page title

        Returns:
            Path to generated HTML file

        Raises:
            FileNotFoundError: If template not found
        """
        template_path = self.template_dir / 'viewer-ply.html'

        if not template_path.exists():
            raise FileNotFoundError(f"PLY template not found: {template_path}")

        # Load template
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Replace placeholders
        html = html.replace('{{PLY_DATA}}', self._escape_js_string(ply_data))

        # Update title if provided
        if title:
            html = html.replace('<title>Terra Point Cloud Viewer (PLY)</title>',
                              f'<title>{self._escape_html(title)}</title>')

        # Write output
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path

    def _escape_js_string(self, text: str) -> str:
        """
        Escape string for embedding in JavaScript template literal.

        Handles:
        - Backticks (`)
        - Backslashes (\)
        - Dollar signs with braces (${})

        Args:
            text: String to escape

        Returns:
            Escaped string safe for JavaScript template literals
        """
        # Escape backslashes first (must be first to avoid double-escaping)
        text = text.replace('\\', '\\\\')

        # Escape backticks
        text = text.replace('`', '\\`')

        # Escape ${ (template literal interpolation)
        text = text.replace('${', '\\${')

        return text

    def _escape_html(self, text: str) -> str:
        """
        Escape HTML special characters.

        Args:
            text: String to escape

        Returns:
            HTML-safe string
        """
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))

    def get_template_info(self, template_name: str) -> Dict:
        """
        Get information about a template.

        Args:
            template_name: Name of template ('obj' or 'ply')

        Returns:
            Dict with template metadata
        """
        template_path = self.template_dir / f'viewer-{template_name}.html'

        if not template_path.exists():
            return {'exists': False, 'path': str(template_path)}

        stat = template_path.stat()

        return {
            'exists': True,
            'path': str(template_path),
            'size_bytes': stat.st_size,
            'size_kb': stat.st_size / 1024,
            'placeholders': self._find_placeholders(template_path)
        }

    def _find_placeholders(self, template_path: Path) -> list:
        """Find all {{PLACEHOLDER}} markers in template."""
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all {{PLACEHOLDER}} patterns
        placeholders = re.findall(r'\{\{([A-Z_]+)\}\}', content)
        return list(set(placeholders))  # Remove duplicates

    @staticmethod
    def format_file_size(bytes: int) -> str:
        """Format bytes as human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} TB"

    @staticmethod
    def estimate_output_size(obj_size: int, mtl_size: int, texture_sizes: Dict[str, int]) -> Dict:
        """
        Estimate final HTML file size.

        Args:
            obj_size: OBJ data size in bytes
            mtl_size: MTL data size in bytes
            texture_sizes: Dict mapping texture names to sizes in bytes

        Returns:
            Dict with size estimates
        """
        # Template overhead (approximate)
        template_overhead = 62 * 1024  # ~62KB for OBJ template

        # OBJ and MTL data (no Base64 overhead, it's text)
        obj_mtl_size = obj_size + mtl_size

        # Texture data (Base64 adds ~37% overhead)
        total_texture_size = sum(texture_sizes.values())
        base64_texture_size = int(total_texture_size * 1.37)

        # Total estimate
        total_size = template_overhead + obj_mtl_size + base64_texture_size

        return {
            'template_overhead_mb': template_overhead / (1024 * 1024),
            'obj_mtl_size_mb': obj_mtl_size / (1024 * 1024),
            'textures_original_mb': total_texture_size / (1024 * 1024),
            'textures_base64_mb': base64_texture_size / (1024 * 1024),
            'total_estimated_mb': total_size / (1024 * 1024),
            'total_estimated_bytes': total_size
        }


# Example usage
if __name__ == "__main__":
    generator = HTMLGenerator()

    # Check template info
    obj_info = generator.get_template_info('obj')
    ply_info = generator.get_template_info('ply')

    print("HTMLGenerator module loaded successfully")
    print(f"\nOBJ Template:")
    print(f"  Exists: {obj_info['exists']}")
    if obj_info['exists']:
        print(f"  Size: {obj_info['size_kb']:.2f} KB")
        print(f"  Placeholders: {', '.join(obj_info['placeholders'])}")

    print(f"\nPLY Template:")
    print(f"  Exists: {ply_info['exists']}")
    if ply_info['exists']:
        print(f"  Size: {ply_info['size_kb']:.2f} KB")
        print(f"  Placeholders: {', '.join(ply_info['placeholders'])}")
