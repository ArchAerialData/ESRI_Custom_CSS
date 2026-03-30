"""
OBJ (Wavefront Object) Parser Module

Handles reading and merging of OBJ geometry files.
Supports multi-file OBJ models (common in Terra exports).

Wavefront OBJ format elements supported:
- v  - Geometric vertices
- vt - Texture coordinates
- vn - Vertex normals
- f  - Face definitions
- g  - Group names
- o  - Object names
- usemtl - Material references
- mtllib - Material library references
"""

from pathlib import Path
from typing import List, Dict, Optional, Set
import re


class OBJParser:
    """Parser for Wavefront OBJ geometry files with multi-file support."""

    def __init__(self):
        self.obj_content: List[str] = []
        self.mtl_references: Set[str] = set()
        self.material_usage: Set[str] = set()
        self.stats = {
            'files_merged': 0,
            'vertices': 0,
            'normals': 0,
            'texcoords': 0,
            'faces': 0,
            'groups': 0,
            'objects': 0
        }

    def parse_file(self, obj_path: Path) -> str:
        """
        Parse single OBJ file.

        Args:
            obj_path: Path to .obj file

        Returns:
            OBJ file content as string

        Raises:
            FileNotFoundError: If OBJ file doesn't exist
        """
        if not obj_path.exists():
            raise FileNotFoundError(f"OBJ file not found: {obj_path}")

        with open(obj_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        self._analyze_obj_content(content)
        self.stats['files_merged'] = 1

        return content

    def parse_files(self, obj_paths: List[Path]) -> str:
        """
        Parse and merge multiple OBJ files into a single OBJ string.

        Terra often exports models as multiple .obj files that need to be combined.
        This method handles vertex index offsetting to merge files correctly.

        Args:
            obj_paths: List of paths to .obj files

        Returns:
            Merged OBJ file content as string

        Raises:
            FileNotFoundError: If any OBJ file doesn't exist
        """
        if not obj_paths:
            raise ValueError("No OBJ files provided")

        merged_lines = []
        v_offset = 0  # Vertex offset
        vt_offset = 0  # Texture coord offset
        vn_offset = 0  # Normal offset

        for i, obj_path in enumerate(obj_paths):
            if not obj_path.exists():
                raise FileNotFoundError(f"OBJ file not found: {obj_path}")

            with open(obj_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Count vertices/normals/texcoords in current file for offset calculation
            file_v_count = 0
            file_vt_count = 0
            file_vn_count = 0

            # First pass: count elements
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(maxsplit=1)
                if not parts:
                    continue

                command = parts[0].lower()

                if command == 'v':
                    file_v_count += 1
                elif command == 'vt':
                    file_vt_count += 1
                elif command == 'vn':
                    file_vn_count += 1

            # Second pass: process and add offset to face indices
            for line in lines:
                line = line.strip()

                # Skip empty lines and comments (but keep them for readability)
                if not line:
                    merged_lines.append('')
                    continue
                if line.startswith('#'):
                    merged_lines.append(line)
                    continue

                parts = line.split(maxsplit=1)
                if not parts:
                    continue

                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ''

                # Add comment separator between files
                if i > 0 and command in {'v', 'o', 'g'} and len(merged_lines) > 0 and merged_lines[-1]:
                    if merged_lines[-1] != f"# === File {i+1}: {obj_path.name} ===":
                        merged_lines.append(f"# === File {i+1}: {obj_path.name} ===")

                # Pass through geometric data unchanged
                if command in {'v', 'vt', 'vn'}:
                    merged_lines.append(line)

                # Adjust face indices by offsets
                elif command == 'f':
                    adjusted_face = self._adjust_face_indices(
                        args, v_offset, vt_offset, vn_offset
                    )
                    merged_lines.append(f"f {adjusted_face}")

                # Track material library references
                elif command == 'mtllib':
                    self.mtl_references.add(args.strip())
                    # Only add mtllib once (avoid duplicates)
                    if f"mtllib {args}" not in merged_lines:
                        merged_lines.append(line)

                # Track material usage
                elif command == 'usemtl':
                    self.material_usage.add(args.strip())
                    merged_lines.append(line)

                # Pass through other commands
                else:
                    merged_lines.append(line)

            # Update offsets for next file
            v_offset += file_v_count
            vt_offset += file_vt_count
            vn_offset += file_vn_count

        merged_content = '\n'.join(merged_lines)
        self._analyze_obj_content(merged_content)
        self.stats['files_merged'] = len(obj_paths)

        return merged_content

    def _adjust_face_indices(self, face_def: str,
                             v_offset: int, vt_offset: int, vn_offset: int) -> str:
        """
        Adjust face vertex indices by offsets.

        Face format: v/vt/vn or v//vn or v/vt or v
        Example: "1/1/1 2/2/2 3/3/3" with offset 10 becomes "11/11/11 12/12/12 13/13/13"

        Args:
            face_def: Face definition string (e.g., "1/1/1 2/2/2 3/3/3")
            v_offset: Vertex index offset
            vt_offset: Texture coordinate offset
            vn_offset: Normal index offset

        Returns:
            Adjusted face definition string
        """
        vertices = face_def.split()
        adjusted_vertices = []

        for vertex in vertices:
            parts = vertex.split('/')

            # Adjust vertex index (always present)
            if parts[0]:
                parts[0] = str(int(parts[0]) + v_offset)

            # Adjust texture coordinate index (if present)
            if len(parts) > 1 and parts[1]:
                parts[1] = str(int(parts[1]) + vt_offset)

            # Adjust normal index (if present)
            if len(parts) > 2 and parts[2]:
                parts[2] = str(int(parts[2]) + vn_offset)

            adjusted_vertices.append('/'.join(parts))

        return ' '.join(adjusted_vertices)

    def _analyze_obj_content(self, content: str):
        """Analyze OBJ content and update statistics."""
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(maxsplit=1)
            if not parts:
                continue

            command = parts[0].lower()

            if command == 'v':
                self.stats['vertices'] += 1
            elif command == 'vn':
                self.stats['normals'] += 1
            elif command == 'vt':
                self.stats['texcoords'] += 1
            elif command == 'f':
                self.stats['faces'] += 1
            elif command == 'g':
                self.stats['groups'] += 1
            elif command == 'o':
                self.stats['objects'] += 1
            elif command == 'mtllib':
                self.mtl_references.add(parts[1].strip() if len(parts) > 1 else '')
            elif command == 'usemtl':
                self.material_usage.add(parts[1].strip() if len(parts) > 1 else '')

    def get_mtl_references(self) -> Set[str]:
        """Get all MTL file references found in OBJ file(s)."""
        return self.mtl_references

    def get_material_usage(self) -> Set[str]:
        """Get all material names used in OBJ file(s)."""
        return self.material_usage

    def get_stats(self) -> Dict:
        """Get parsing statistics."""
        return self.stats.copy()

    @staticmethod
    def find_obj_files(directory: Path) -> List[Path]:
        """
        Find all OBJ files in a directory.

        Args:
            directory: Directory to search

        Returns:
            List of OBJ file paths, sorted alphabetically
        """
        if not directory.exists() or not directory.is_dir():
            return []

        obj_files = sorted(directory.glob('*.obj'))
        return obj_files

    @staticmethod
    def find_mtl_file(obj_path: Path) -> Optional[Path]:
        """
        Find MTL file associated with OBJ file.

        Looks for:
        1. MTL file with same name as OBJ
        2. Any MTL file in same directory

        Args:
            obj_path: Path to OBJ file

        Returns:
            Path to MTL file, or None if not found
        """
        # Check for same-named MTL
        mtl_path = obj_path.with_suffix('.mtl')
        if mtl_path.exists():
            return mtl_path

        # Check for any MTL in directory
        mtl_files = list(obj_path.parent.glob('*.mtl'))
        if mtl_files:
            return mtl_files[0]

        return None


# Example usage
if __name__ == "__main__":
    parser = OBJParser()

    # Example: Parse single file
    # content = parser.parse_file(Path("model.obj"))
    # print(f"Vertices: {parser.stats['vertices']}")

    # Example: Parse multiple files
    # files = [Path("model_part1.obj"), Path("model_part2.obj")]
    # merged = parser.parse_files(files)
    # print(f"Merged {parser.stats['files_merged']} files")
    # print(f"Total vertices: {parser.stats['vertices']}")

    print("OBJParser module loaded successfully")
    print("Supports multi-file OBJ merging with vertex index offsetting")
