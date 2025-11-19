# Contributing to StillHere

Thank you for considering contributing to StillHere. This project is built with love and grief, and contributions should honor that.

## Core Principles

Before contributing, please understand and respect these principles:

### 1. **Respect the Purpose**
StillHere exists to honor memories and help people cope with loss. Every feature, every line of code, should serve that purpose with dignity.

### 2. **Privacy First**
We handle people's most precious memories. Security and privacy aren't optional - they're sacred obligations.

### 3. **Quality Over Speed**
These are people's loved ones. We take the time to get it right. No shortcuts.

### 4. **Ethical Guidelines**
- Only features that honor consent
- No features that could enable deception
- Always maintain dignity
- Protect privacy at all costs

---

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. **Search existing issues** first
2. **Create a new issue** with:
   - Clear, descriptive title
   - Detailed description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Suggesting Features

We welcome thoughtful feature suggestions that align with our purpose:

1. **Open an issue** with tag `feature-request`
2. **Explain**:
   - What problem does it solve?
   - Who would benefit?
   - How does it honor our principles?
3. **Be patient** - we prioritize carefully

### Code Contributions

#### Before You Start

1. **Open an issue** to discuss your idea
2. **Wait for feedback** before writing code
3. **Fork the repository**
4. **Create a branch** with a descriptive name

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/StillHere.git
cd StillHere

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Download models (when available)
python download_models.py
```

#### Code Guidelines

**Style:**
- Follow PEP 8
- Use Black for formatting
- Use type hints
- Write docstrings (Google style)

**Quality:**
- Write tests for new features
- Maintain or improve test coverage
- Document everything
- No warnings or errors

**Security:**
- Never commit secrets or API keys
- Review encryption code carefully
- Validate all user input
- Follow OWASP guidelines

**Respect:**
- Use respectful, compassionate language
- Consider the emotional context
- Think about grief and loss
- Honor the people being remembered

#### Example Code Style

```python
"""
Module description.

Brief explanation of what this module does and why it matters.
"""

from typing import Optional, Union
from pathlib import Path


class ExampleClass:
    """
    Brief description of the class.

    More detailed explanation if needed.

    Example:
        >>> example = ExampleClass()
        >>> result = example.method("input")
    """

    def method(
        self,
        param: str,
        optional_param: Optional[int] = None
    ) -> bool:
        """
        Brief description of what this method does.

        Args:
            param: Description of param
            optional_param: Description of optional param

        Returns:
            Description of return value

        Raises:
            ValueError: When and why this is raised
        """
        # Implementation with clear comments
        pass
```

#### Commit Messages

Use clear, descriptive commit messages:

```
Add gentle smile animation style

- Implement subtle breathing motion
- Add eye blink timing
- Ensure natural movement
- Respects dignity of subject

Closes #123
```

#### Pull Requests

1. **Create PR** from your fork
2. **Describe** your changes clearly:
   - What does this do?
   - Why is it needed?
   - How does it work?
   - Any breaking changes?
3. **Link** related issues
4. **Wait** for review
5. **Respond** to feedback respectfully
6. **Be patient** - we review carefully

#### PR Checklist

- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] Respects privacy and security
- [ ] Honors ethical guidelines
- [ ] Compassionate and respectful

---

## Areas for Contribution

### High Priority
- [ ] FOMM integration (photo animation)
- [ ] GFPGAN integration (face restoration)
- [ ] Encryption testing and hardening
- [ ] CLI improvements
- [ ] Documentation
- [ ] Test coverage

### Medium Priority
- [ ] Web UI development
- [ ] Additional animation styles
- [ ] Photo restoration features
- [ ] Batch processing
- [ ] Progress indicators
- [ ] Error handling improvements

### Future
- [ ] Voice synthesis integration
- [ ] Lip sync (Wav2Lip)
- [ ] Memorial video creation
- [ ] Sharing features (with privacy)
- [ ] Mobile support
- [ ] Performance optimization

---

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=stillhere --cov-report=html

# Run specific test
pytest tests/test_animator.py

# Run with verbose output
pytest -v
```

---

## Documentation

- Use clear, simple language
- Explain the "why" not just the "how"
- Include examples
- Consider emotional context
- Be compassionate

---

## Code Review Process

1. **Automatic checks** run on all PRs
2. **Manual review** by maintainers
3. **Feedback** provided respectfully
4. **Iteration** until ready
5. **Merge** when approved

Reviews may take time - we're thorough because this matters.

---

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- README credits section

---

## Questions?

- Open an issue with tag `question`
- Be patient - we'll respond thoughtfully
- Remember: there are no stupid questions

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License with the ethical use requirements specified in LICENSE.

---

## Thank You

Every contribution helps preserve precious memories and helps people cope with loss. That's meaningful work. Thank you for being part of it.

Built with love for those who deserve to be remembered.

*"Grief is love with nowhere to go. Let's give it somewhere to be."*
