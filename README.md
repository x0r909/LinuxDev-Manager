# LinuxDev Manager 🚀

<div align="center">

![LinuxDev Manager](assets/icon.png)

**A powerful Laragon-like web development environment manager for Linux**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg)](https://www.linux.org/)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Troubleshooting](#-troubleshooting) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

LinuxDev Manager is a comprehensive GUI application that simplifies web development environment management on Linux systems. Inspired by Laragon for Windows, it provides an intuitive interface to manage services, create virtual hosts, handle databases, and much more - all from a single, elegant application.

## ✨ Features

### 🔧 Service Management
- **Start, Stop, Restart** web services with a single click
- Support for **Apache**, **Nginx**, **MySQL**, **PostgreSQL**, **Redis**, **PHP-FPM**
- Real-time service status monitoring with color indicators
- Auto-start configuration
- Port usage detection and display

### 🌐 Virtual Host Management
- Create virtual hosts with pretty URLs (e.g., `myproject.test`)
- Support for both **Apache** and **Nginx**
- Automatic `/etc/hosts` configuration
- Multi-PHP version support (8.2, 8.3, etc.)
- One-click SSL certificate generation

### 🔒 SSL Certificate Generation
- Self-signed SSL certificates for local HTTPS development
- Automatic certificate installation and configuration
- Support for both Apache and Nginx

### 🗄️ Database Management
- Create **MySQL/MariaDB** and **PostgreSQL** databases
- User and permission management
- GUI-based database creation wizard
- Automatic database user creation

### 📦 Package Installation
- Install web development packages through GUI
- Categorized package browser:
  - Web Servers (Apache, Nginx)
  - Databases (MySQL, PostgreSQL, Redis)
  - Languages & Runtimes (PHP, Node.js, Python)
  - Development Tools
- One-click install/uninstall
- Real-time installation status tracking

### 🎨 Project Management
- Quick-create projects:
  - Empty PHP/HTML projects
  - **Laravel** applications
  - **WordPress** sites
  - Custom project types
- Automatic virtual host creation
- Integrated browser and terminal access
- Project listing with easy management

### 💻 Embedded Terminal
- Built-in terminal with project context
- Environment-aware command execution
- Project-specific working directories
- Auto-configured `PATH` (includes `node_modules/.bin`, `vendor/bin`)
- Command history with arrow key navigation
- Quick command buttons for common tasks
- Color-coded output (stdout, stderr, info)

### 🎨 Modern UI/UX
- **Light** and **Dark** theme support
- Clean, intuitive interface
- Custom-drawn vector icons (no emoji dependencies)
- Responsive design
- System tray integration
- Real-time status updates

## 🛠️ Requirements

- **OS**: Linux (Ubuntu/Debian recommended, should work on other distributions)
- **Python**: 3.8 or higher
- **systemd**: For service management
- **pkexec/PolicyKit**: For GUI-based privilege escalation (automatically installed)

### Python Dependencies
- PyQt5 (5.15+)
- Pillow (for icon generation)

## 📥 Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/x0r909/webdev-mgmt.git
   cd webdev-mgmt
   ```

2. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 main.py
   ```

### Using Installation Script

```bash
chmod +x install.sh
./install.sh
```

The installation script will:
- Install PolicyKit if not present
- Install Python dependencies
- Set up necessary permissions
- Create desktop shortcuts (optional)

## 🎯 Usage

### Starting the Application

```bash
python3 main.py
```

### Dashboard

The dashboard provides an at-a-glance view of all your services:

- 🟢 **Green**: Service is running
- 🔴 **Red**: Service is stopped
- ⚪ **Gray**: Service is not installed
- ⚡ **Lightning bolt**: Auto-start enabled
- 🌐 **Port info**: Shows active ports

**Quick Actions:**
- Create Virtual Host
- Create Database
- Create Project

### Creating a Virtual Host

1. Navigate to **Dashboard** or **Projects** tab
2. Click **"Create Virtual Host"**
3. Enter project details:
   - Project name
   - Document root path
   - Web server (Apache/Nginx)
   - PHP version
4. Enable SSL (optional)
5. Click **Create**

The application will automatically:
- Generate web server configuration
- Add entry to `/etc/hosts`
- Create SSL certificate (if enabled)
- Reload web server

### Creating a Project

1. Go to **Projects** tab
2. Click **"Create Project"**
3. Select project type:
   - Empty PHP Project
   - HTML Project
   - Laravel Application
   - WordPress Site
4. Configure virtual host (optional)
5. Enable SSL (optional)
6. Click **Create**

### Managing Packages

1. Navigate to **Packages** tab
2. Browse available packages by category
3. Click **Install** (with download icon) or **Uninstall** (with trash icon)
4. Confirm the action
5. Wait for installation/removal to complete

### Using the Terminal

1. Go to **Terminal** tab
2. Select a project from the dropdown (or use System Default)
3. Type commands in the input field or use quick command buttons
4. Press Enter to execute
5. Use ↑/↓ arrow keys to navigate command history

**Quick Commands Available:**
- `pwd` - Print working directory
- `ls -la` - List all files
- `npm install` - Install npm packages
- `composer install` - Install composer packages
- `php -v` - Check PHP version
- `node -v` - Check Node.js version

**Terminal Features:**
- Automatic PATH configuration
- Environment variables per project
- Color-coded output
- Command history
- Project-specific working directory

### Database Management

1. Navigate to **Database** tab
2. Choose database type:
   - MySQL Database
   - PostgreSQL Database
3. Click the respective **"Create"** button
4. Enter:
   - Database name
   - Username
   - Password
5. Click **Create**

## ⚙️ Configuration

Configuration file: `~/.linuxdev-manager/config.json`

### Default Settings

```json
{
  "projects_root": "~/projects",
  "default_web_server": "apache2",
  "default_php_version": "8.2",
  "default_domain_extension": ".test",
  "terminal_emulator": "gnome-terminal",
  "code_editor": "code",
  "theme": "light"
}
```

### Paths Configuration

The application manages configurations in standard Linux locations:
- Apache sites: `/etc/apache2/sites-available`
- Nginx sites: `/etc/nginx/sites-available`
- Hosts file: `/etc/hosts`
- SSL certificates: `/etc/ssl/certs`
- SSL keys: `/etc/ssl/private`

## 🐛 Troubleshooting

### Permission Errors

**Problem**: "Authentication Required" dialogs appearing

**Solution**: This is normal! The application uses `pkexec` for privilege escalation. Enter your password when prompted for administrative tasks.

If `pkexec` is not installed:
```bash
sudo apt-get install policykit-1
```

### Service Not Found

**Problem**: Service shows as "Not Installed"

**Solution**: Install the required service:
```bash
# Apache
sudo apt-get install apache2

# Nginx
sudo apt-get install nginx

# MySQL
sudo apt-get install mysql-server

# PostgreSQL
sudo apt-get install postgresql

# Redis
sudo apt-get install redis-server

# PHP-FPM (multiple versions)
sudo apt-get install php8.2-fpm php8.3-fpm
```

### Virtual Host Not Working

**Checklist:**
1. ✅ Service is running (check Dashboard)
2. ✅ Entry exists in `/etc/hosts`
3. ✅ Virtual host config file created
4. ✅ Web server has been restarted

**Debug steps:**
```bash
# Check hosts file
cat /etc/hosts | grep yourproject

# Test Apache config
sudo apache2ctl -t

# Test Nginx config
sudo nginx -t

# Check if port is in use
sudo netstat -tulpn | grep :80

# Restart service
sudo systemctl restart apache2  # or nginx
```

### SSL Certificate Issues

**Problem**: Browser shows security warning

**Solution**: This is normal for self-signed certificates in development. Click "Advanced" and proceed. 

⚠️ **Warning**: Self-signed certificates are for local development only!

### Icons Not Showing

**Problem**: Icons appear as squares

**Solution**: The application now uses custom-drawn icons. If you still see issues:
```bash
# Regenerate icons
python3 create_icon.py

# Verify icons exist
python3 verify_icon.py
```

### QSocketNotifier Warning

**Problem**: `QSocketNotifier: Can only be used with threads started with QThread`

**Solution**: This is a harmless Qt internal warning and doesn't affect functionality. You can safely ignore it.

## 🗺️ Roadmap

### Planned Features
- [ ] Docker container management
- [ ] Custom project templates
- [ ] Backup/restore functionality
- [ ] Service log viewer
- [ ] Multiple terminal tabs
- [ ] Git integration
- [ ] Database browser/editor
- [ ] Performance monitoring dashboard
- [ ] REST API for automation
- [ ] Plugin system

### Recently Added ✅
- ✅ Embedded terminal with environment support
- ✅ Custom-drawn vector icons
- ✅ Light/Dark theme support
- ✅ Project-specific environment variables
- ✅ Quick command buttons

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

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

### Code Structure

```
webdev-mgmt/
├── assets/           # Application icons
├── config/          # Configuration files
├── core/            # Core functionality modules
│   ├── config_manager.py
│   ├── service_manager.py
│   ├── vhost_manager.py
│   ├── database_manager.py
│   └── ...
├── gui/             # GUI components
│   ├── main_window.py
│   ├── terminal_widget.py
│   ├── icon_helper.py
│   └── ...
├── templates/       # Configuration templates
├── utils/           # Utility functions
└── main.py          # Application entry point
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Laragon](https://laragon.org/) for Windows
- Icons created with PyQt5 QPainter
- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
- Community contributions and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/x0r909/webdev-mgmt/issues)
- **Discussions**: [GitHub Discussions](https://github.com/x0r909/webdev-mgmt/discussions)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/x0r909/webdev-mgmt?style=social)
![GitHub forks](https://img.shields.io/github/forks/x0r909/webdev-mgmt?style=social)
![GitHub issues](https://img.shields.io/github/issues/x0r909/webdev-mgmt)

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ for Linux developers**

[⬆ Back to Top](#linuxdev-manager-)

</div>
