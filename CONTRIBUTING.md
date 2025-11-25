# Contributing to LinuxDev Manager

Thank you for your interest in contributing to LinuxDev Manager! We welcome contributions from the community.

## 🤝 How to Contribute

### 1. Fork the Repository

Fork the repository to your own GitHub account by clicking the "Fork" button at the top right.

### 2. Clone Your Fork

```bash
git clone https://github.com/yourusername/webdev-mgmt.git
cd webdev-mgmt
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/AmazingFeature
```

Use descriptive branch names:
- `feature/` - for new features
- `bugfix/` - for bug fixes
- `docs/` - for documentation updates
- `refactor/` - for code refactoring

### 4. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add comments where necessary
- Test your changes thoroughly

### 5. Commit Your Changes

```bash
git add .
git commit -m 'Add some AmazingFeature'
```

**Commit Message Guidelines:**
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Examples:
```
Add dark theme support for terminal widget
Fix virtual host creation on Nginx
Update documentation for SSL configuration
```

### 6. Push to Your Fork

```bash
git push origin feature/AmazingFeature
```

### 7. Open a Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template with:
   - Description of changes
   - Related issue number (if applicable)
   - Screenshots (for UI changes)
   - Testing done

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Linux system (Ubuntu/Debian recommended)
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/yourusername/webdev-mgmt.git
cd webdev-mgmt

# Install dependencies
pip3 install -r requirements.txt

# Run in development mode
python3 main.py

# Test icons
python3 test_icons.py
```

### Testing Your Changes

Before submitting a PR, please test:

1. **Functionality**: Does your feature/fix work as expected?
2. **UI**: Does the interface look correct in both light and dark themes?
3. **Error Handling**: Does it handle errors gracefully?
4. **Compatibility**: Does it work on different Linux distributions?
5. **No Regressions**: Does it break any existing features?

## 📁 Code Structure

```
webdev-mgmt/
├── assets/           # Application icons
├── config/          # Configuration files
│   ├── app_config.json
│   └── packages.json
├── core/            # Core functionality modules
│   ├── config_manager.py      # Application configuration
│   ├── service_manager.py     # Service control
│   ├── vhost_manager.py       # Virtual host management
│   ├── database_manager.py    # Database operations
│   ├── ssl_manager.py         # SSL certificate handling
│   ├── package_installer.py   # Package management
│   └── project_manager.py     # Project creation
├── gui/             # GUI components
│   ├── main_window.py         # Main application window
│   ├── terminal_widget.py     # Embedded terminal
│   ├── icon_helper.py         # Custom icon drawing
│   ├── styles.py              # Theme and styling
│   └── *_dialog.py            # Various dialog windows
├── templates/       # Configuration templates
│   ├── apache_vhost.conf
│   ├── nginx_vhost.conf
│   └── *_ssl.conf
├── utils/           # Utility functions
│   ├── system_utils.py        # System operations
│   └── validators.py          # Input validation
└── main.py          # Application entry point
```

## 🎯 Coding Guidelines

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use 4 spaces for indentation (not tabs)

### Documentation

- Add docstrings to all functions and classes
- Update README.md if adding new features
- Comment complex logic

Example:
```python
def create_virtual_host(project_name, root_path, server_type="apache2"):
    """
    Create a virtual host configuration.
    
    Args:
        project_name (str): Name of the project
        root_path (str): Document root path
        server_type (str): Web server type ('apache2' or 'nginx')
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Implementation here
```

### GUI Components

- Use consistent widget styling
- Support both light and dark themes
- Add tooltips for user guidance
- Handle all user inputs with validation

### Error Handling

- Use try-except blocks appropriately
- Log errors for debugging
- Show user-friendly error messages
- Don't expose system paths in error dialogs

## 🐛 Reporting Bugs

### Before Submitting

- Check if the bug has already been reported
- Test on the latest version
- Gather all necessary information

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.2]
- Application version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## 💡 Suggesting Features

We love feature suggestions! Please:

1. Check if it's already been suggested
2. Explain the use case clearly
3. Describe the expected behavior
4. Consider implementation impact

## 🔍 Code Review Process

All PRs will be reviewed by maintainers. We look for:

- **Code quality**: Clean, readable, well-structured
- **Functionality**: Works as intended
- **Testing**: Adequately tested
- **Documentation**: Properly documented
- **Style**: Follows project conventions

We may request changes. Please be patient and responsive.

## 📋 Areas We Need Help With

- **Testing**: Testing on different Linux distributions
- **Documentation**: Improving guides and tutorials
- **Translations**: Multi-language support
- **Features**: Implementing roadmap items
- **Bug fixes**: Addressing open issues
- **UI/UX**: Design improvements

## 🎁 Recognition

Contributors will be:
- Listed in the project README
- Credited in release notes
- Given our eternal gratitude! 🙏

## 📞 Getting Help

Need help contributing?

- Open a [Discussion](https://github.com/x0r909/webdev-mgmt/discussions)
- Check existing [Issues](https://github.com/x0r909/webdev-mgmt/issues)
- Review the [README](README.md)

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior:**
- Being respectful and inclusive
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy

**Unacceptable behavior:**
- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to LinuxDev Manager! 🚀
