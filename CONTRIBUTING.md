# Contributing to Piano HAT

Thank you for your interest in contributing to Piano HAT! This document provides guidelines for contributing to this project.

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/piano-hat.git
   cd piano-hat
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install development dependencies:**
   ```bash
   cd library
   pip install -e ".[dev,examples]"
   ```

## Code Style

This project follows PEP 8 style guidelines with these specifics:

- **Line length:** 120 characters maximum
- **Formatter:** Black
- **Linter:** Flake8
- **Type checker:** MyPy

### Running code quality tools:

```bash
# Format code
black library/pianohat.py

# Lint code
flake8 library/pianohat.py --max-line-length=120

# Type check
mypy library/pianohat.py
```

## Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clear, concise commit messages
   - Add type hints to new functions
   - Update documentation as needed
   - Test your changes on actual hardware if possible

3. **Test your changes:**
   ```bash
   # Import test
   python3 -c "import pianohat; print(pianohat.__version__)"
   
   # Run examples (if you have hardware)
   python3 examples/buttons.py
   ```

4. **Update the CHANGELOG:**
   - Add your changes to the `[Unreleased]` section
   - Follow the existing format

## Submitting Changes

1. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request:**
   - Use a clear, descriptive title
   - Describe what changes you made and why
   - Reference any related issues
   - Ensure CI checks pass

## Pull Request Checklist

- [ ] Code follows the project's style guidelines
- [ ] Code has been formatted with Black
- [ ] Type hints added to new functions
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG updated
- [ ] Tested on actual hardware (if possible)
- [ ] CI checks pass

## Reporting Issues

When reporting issues, please include:

- **Hardware:** Raspberry Pi model and OS version
- **Python version:** Output of `python3 --version`
- **Library version:** Output of `pip3 show pianohat`
- **Steps to reproduce:** Clear, numbered steps
- **Expected behavior:** What should happen
- **Actual behavior:** What actually happens
- **Error messages:** Full error output/traceback

## Testing on Hardware

If you have a Piano HAT:

1. **Test I2C detection:**
   ```bash
   i2cdetect -y 1
   # Should show devices at 0x28 and 0x2b
   ```

2. **Test basic functionality:**
   ```bash
   python3 examples/buttons.py
   python3 examples/leds.py
   ```

3. **Test your changes:**
   - Verify all 13 piano keys work
   - Test octave up/down buttons
   - Test instrument button
   - Test LED control

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## Questions?

Feel free to open an issue for:
- Questions about development
- Suggestions for improvements
- Discussion about features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
