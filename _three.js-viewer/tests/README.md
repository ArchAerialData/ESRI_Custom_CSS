# Tests Directory

This directory contains test files, sample models, and QA testing resources.

## Structure

```
tests/
├── sample_models/               # Test 3D models from Terra
│   ├── small-obj/              # < 5MB OBJ model
│   ├── large-obj/              # 50+ MB OBJ model
│   ├── multi-file-obj/         # Split OBJ with multiple textures
│   ├── ply-binary/             # Binary PLY model
│   └── ply-ascii/              # ASCII PLY model
├── test_obj_parser.py          # Unit tests for OBJ parser
├── test_ply_parser.py          # Unit tests for PLY parser
├── test_texture_processor.py   # Unit tests for texture processing
└── test_html_embedder.py       # Unit tests for HTML generation
```

## Phase 5.1: QA Testing

**Test Cases** (from implementation plan):
1. Small OBJ model (< 5 MB)
2. Large OBJ model (50+ MB)
3. Multi-file OBJ (split geometry + multiple textures)
4. PLY binary (typical Terra export)
5. PLY ASCII (text-based)
6. High-res textures (4K images)
7. Low-res textures (512×512)
8. Missing texture files (error handling)
9. Corrupt OBJ file (error handling)
10. Very large model (170+ MB, performance test)

## Sample Models

Place Terra-exported models in the appropriate `sample_models/` subdirectories for testing.

**Note**: Sample models are not committed to the repository (see `.gitignore`).
Add your own Terra exports for testing purposes.

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_obj_parser.py

# Run with coverage
pytest --cov=src/modules
```

## Test Data Guidelines

- Use real Terra exports when possible
- Include models with various complexities
- Test edge cases (missing files, corrupt data, extreme sizes)
- Document expected behavior for each test case
