"""
MTL (Material Template Library) Parser Module

Parses Wavefront .mtl files and handles texture path resolution
for embedding in HTML viewers.

Supports standard MTL properties:
- Ambient color (Ka)
- Diffuse color (Kd)
- Specular color (Ks)
- Shininess (Ns)
- Transparency (d, Tr)
- Texture maps (map_Kd, map_Ka, map_Ks, map_Bump, map_d)
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
import re


class Material:
    """Represents a single material from MTL file."""

    def __init__(self, name: str):
        self.name = name
        self.ambient = None  # Ka - ambient color (r, g, b)
        self.diffuse = None  # Kd - diffuse color (r, g, b)
        self.specular = None  # Ks - specular color (r, g, b)
        self.shininess = None  # Ns - shininess/specular exponent
        self.opacity = 1.0  # d - opacity (0.0-1.0)
        self.transparency = 0.0  # Tr - transparency (0.0-1.0)
        self.optical_density = None  # Ni - optical density
        self.illumination = None  # illum - illumination model

        # Texture maps
        self.map_diffuse = None  # map_Kd
        self.map_ambient = None  # map_Ka
        self.map_specular = None  # map_Ks
        self.map_shininess = None  # map_Ns
        self.map_bump = None  # map_Bump or bump
        self.map_displacement = None  # disp
        self.map_alpha = None  # map_d

    def get_texture_paths(self) -> Set[str]:
        """Get all texture file paths referenced by this material."""
        textures = set()
        for attr in ['map_diffuse', 'map_ambient', 'map_specular',
                     'map_shininess', 'map_bump', 'map_displacement', 'map_alpha']:
            value = getattr(self, attr)
            if value:
                textures.add(value)
        return textures

    def __repr__(self):
        textures = ', '.join(self.get_texture_paths()) if self.get_texture_paths() else 'none'
        return f"Material('{self.name}', textures=[{textures}])"


class MTLParser:
    """Parser for Wavefront MTL material library files."""

    def __init__(self):
        self.materials: Dict[str, Material] = {}
        self.mtl_path: Optional[Path] = None

    def parse_file(self, mtl_path: Path) -> Dict[str, Material]:
        """
        Parse MTL file and extract material definitions.

        Args:
            mtl_path: Path to .mtl file

        Returns:
            Dict mapping material names to Material objects

        Raises:
            FileNotFoundError: If MTL file doesn't exist
        """
        if not mtl_path.exists():
            raise FileNotFoundError(f"MTL file not found: {mtl_path}")

        self.mtl_path = mtl_path
        self.materials = {}
        current_material = None

        with open(mtl_path, 'r', encoding='utf-8', errors='replace') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse line
                try:
                    parts = line.split(maxsplit=1)
                    if not parts:
                        continue

                    command = parts[0].lower()
                    args = parts[1] if len(parts) > 1 else ''

                    # New material definition
                    if command == 'newmtl':
                        material_name = args.strip()
                        current_material = Material(material_name)
                        self.materials[material_name] = current_material

                    elif current_material is None:
                        # Ignore commands before first newmtl
                        continue

                    # Material properties
                    elif command == 'ka':  # Ambient color
                        current_material.ambient = self._parse_color(args)
                    elif command == 'kd':  # Diffuse color
                        current_material.diffuse = self._parse_color(args)
                    elif command == 'ks':  # Specular color
                        current_material.specular = self._parse_color(args)
                    elif command == 'ns':  # Shininess
                        current_material.shininess = float(args)
                    elif command == 'd':  # Opacity
                        current_material.opacity = float(args)
                    elif command == 'tr':  # Transparency
                        current_material.transparency = float(args)
                    elif command == 'ni':  # Optical density
                        current_material.optical_density = float(args)
                    elif command == 'illum':  # Illumination model
                        current_material.illumination = int(args)

                    # Texture maps
                    elif command == 'map_kd':  # Diffuse texture
                        current_material.map_diffuse = self._parse_texture_path(args)
                    elif command == 'map_ka':  # Ambient texture
                        current_material.map_ambient = self._parse_texture_path(args)
                    elif command == 'map_ks':  # Specular texture
                        current_material.map_specular = self._parse_texture_path(args)
                    elif command == 'map_ns':  # Shininess texture
                        current_material.map_shininess = self._parse_texture_path(args)
                    elif command in {'map_bump', 'bump'}:  # Bump map
                        current_material.map_bump = self._parse_texture_path(args)
                    elif command == 'disp':  # Displacement map
                        current_material.map_displacement = self._parse_texture_path(args)
                    elif command == 'map_d':  # Alpha/transparency map
                        current_material.map_alpha = self._parse_texture_path(args)

                except (ValueError, IndexError) as e:
                    print(f"Warning: Error parsing MTL line {line_num}: {line}")
                    print(f"  Error: {e}")

        return self.materials

    def parse_string(self, mtl_content: str) -> Dict[str, Material]:
        """
        Parse MTL content from string.

        Args:
            mtl_content: MTL file content as string

        Returns:
            Dict mapping material names to Material objects
        """
        self.materials = {}
        current_material = None

        for line_num, line in enumerate(mtl_content.splitlines(), 1):
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            try:
                parts = line.split(maxsplit=1)
                if not parts:
                    continue

                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ''

                if command == 'newmtl':
                    material_name = args.strip()
                    current_material = Material(material_name)
                    self.materials[material_name] = current_material

                elif current_material is None:
                    continue

                elif command == 'ka':
                    current_material.ambient = self._parse_color(args)
                elif command == 'kd':
                    current_material.diffuse = self._parse_color(args)
                elif command == 'ks':
                    current_material.specular = self._parse_color(args)
                elif command == 'ns':
                    current_material.shininess = float(args)
                elif command == 'd':
                    current_material.opacity = float(args)
                elif command == 'tr':
                    current_material.transparency = float(args)
                elif command == 'ni':
                    current_material.optical_density = float(args)
                elif command == 'illum':
                    current_material.illumination = int(args)
                elif command == 'map_kd':
                    current_material.map_diffuse = self._parse_texture_path(args)
                elif command == 'map_ka':
                    current_material.map_ambient = self._parse_texture_path(args)
                elif command == 'map_ks':
                    current_material.map_specular = self._parse_texture_path(args)
                elif command == 'map_ns':
                    current_material.map_shininess = self._parse_texture_path(args)
                elif command in {'map_bump', 'bump'}:
                    current_material.map_bump = self._parse_texture_path(args)
                elif command == 'disp':
                    current_material.map_displacement = self._parse_texture_path(args)
                elif command == 'map_d':
                    current_material.map_alpha = self._parse_texture_path(args)

            except (ValueError, IndexError) as e:
                print(f"Warning: Error parsing MTL line {line_num}: {line}")

        return self.materials

    def get_all_texture_paths(self) -> Set[str]:
        """Get all unique texture paths referenced in MTL file."""
        textures = set()
        for material in self.materials.values():
            textures.update(material.get_texture_paths())
        return textures

    def update_texture_paths(self, path_mapping: Dict[str, str]):
        """
        Update texture paths in materials (e.g., replace with data URIs).

        Args:
            path_mapping: Dict mapping original paths to new paths/URIs
        """
        for material in self.materials.values():
            for attr in ['map_diffuse', 'map_ambient', 'map_specular',
                         'map_shininess', 'map_bump', 'map_displacement', 'map_alpha']:
                value = getattr(material, attr)
                if value and value in path_mapping:
                    setattr(material, attr, path_mapping[value])

    def to_mtl_string(self) -> str:
        """
        Generate MTL file content from parsed materials.

        Returns:
            MTL file content as string
        """
        lines = []

        for material in self.materials.values():
            lines.append(f"newmtl {material.name}")

            if material.ambient:
                lines.append(f"Ka {' '.join(map(str, material.ambient))}")
            if material.diffuse:
                lines.append(f"Kd {' '.join(map(str, material.diffuse))}")
            if material.specular:
                lines.append(f"Ks {' '.join(map(str, material.specular))}")
            if material.shininess is not None:
                lines.append(f"Ns {material.shininess}")
            if material.opacity != 1.0:
                lines.append(f"d {material.opacity}")
            if material.transparency != 0.0:
                lines.append(f"Tr {material.transparency}")
            if material.optical_density is not None:
                lines.append(f"Ni {material.optical_density}")
            if material.illumination is not None:
                lines.append(f"illum {material.illumination}")

            if material.map_diffuse:
                lines.append(f"map_Kd {material.map_diffuse}")
            if material.map_ambient:
                lines.append(f"map_Ka {material.map_ambient}")
            if material.map_specular:
                lines.append(f"map_Ks {material.map_specular}")
            if material.map_shininess:
                lines.append(f"map_Ns {material.map_shininess}")
            if material.map_bump:
                lines.append(f"map_Bump {material.map_bump}")
            if material.map_displacement:
                lines.append(f"disp {material.map_displacement}")
            if material.map_alpha:
                lines.append(f"map_d {material.map_alpha}")

            lines.append("")  # Empty line between materials

        return '\n'.join(lines)

    def _parse_color(self, args: str) -> tuple:
        """Parse RGB color values (0.0-1.0)."""
        values = args.split()
        if len(values) >= 3:
            return (float(values[0]), float(values[1]), float(values[2]))
        return (0.0, 0.0, 0.0)

    def _parse_texture_path(self, args: str) -> str:
        """Parse texture map path, handling options like -blendu, -blendv."""
        # Texture maps can have options like: -blendu on -blendv on texture.jpg
        # We want to extract just the filename
        parts = args.split()

        # Skip option flags (start with -)
        for part in reversed(parts):
            if not part.startswith('-'):
                # Extract just the filename, normalize path separators
                return part.replace('\\', '/')

        return args.strip()


# Example usage
if __name__ == "__main__":
    # Example MTL parsing
    mtl_content = """
    newmtl material0
    Ka 0.2 0.2 0.2
    Kd 0.8 0.8 0.8
    Ks 1.0 1.0 1.0
    Ns 100
    map_Kd texture.jpg
    """

    parser = MTLParser()
    materials = parser.parse_string(mtl_content)

    print("MTLParser module loaded successfully")
    print(f"Parsed {len(materials)} material(s)")
    for name, material in materials.items():
        print(f"  - {material}")
