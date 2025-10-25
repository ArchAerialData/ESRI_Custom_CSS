# Contributing to Terra Model Viewer Generator

## Development Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Installation

1. Clone the repository:
```bash
cd _three.js-viewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application (when available):
```bash
python src/model-viewer-generator.py
```

## Project Structure

See [README.md](README.md) for complete folder structure.

## Development Workflow

### Adding a New Feature

1. Check the [Implementation Plan](.planning-to-do/embedded-viewer.md) for phase alignment
2. Create new module in `src/modules/` if needed
3. Update HTML templates in `src/templates/` if needed
4. Add tests in `tests/`
5. Update documentation in `docs/`

### Phase-by-Phase Development

Follow the phases outlined in the implementation plan:

- **Phase 1**: Prototyping in `prototypes/phase1/`
- **Phase 2**: Core viewer in `src/templates/`
- **Phase 3**: GUI and modules in `src/`
- **Phase 4**: Advanced features (future)
- **Phase 5**: Testing and documentation

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_obj_parser.py

# Run with coverage
pytest --cov=src/modules
```

## Building the Executable

```bash
# Run build script
./build-exe.bat

# Output will be in dist/
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints
- Write docstrings for all functions and classes
- Keep functions focused and modular

## File Locations Reference

All code should be placed according to the folder structure:

- **Prototypes**: `prototypes/phase1/`
- **Source code**: `src/`
- **Modules**: `src/modules/`
- **Templates**: `src/templates/`
- **Tests**: `tests/`
- **Documentation**: `docs/`
- **Examples**: `examples/`
- **Resources**: `resources/`

See the implementation plan for detailed file locations per phase.

## Questions?

Refer to the [Implementation Plan](.planning-to-do/embedded-viewer.md) for detailed guidance on each development phase.
