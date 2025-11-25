# Quick Start Guide - LinuxDev Manager

## Installation

### 1. Install Dependencies

```bash
# Update package list
sudo apt-get update

# Install required system packages
sudo apt-get install -y python3 python3-pip policykit-1

# Install Python dependencies
cd /home/augie/projek-sekum/webdev-mgmt
pip3 install -r requirements.txt
```

### 2. Run the Application

```bash
# Make executable
chmod +x main.py install.sh

# Run the application
python3 main.py
```

Or use the installation script:

```bash
./install.sh
```

## First Steps

### 1. Install Web Server and Database

1. Open LinuxDev Manager
2. Go to **Packages** tab
3. Install the packages you need:
   - **Apache2** or **Nginx** (web server)
   - **MySQL Server** or **PostgreSQL** (database)
   - **PHP 8.2** (PHP with FPM)
   - **Git** (version control)
   - **Composer** (PHP package manager)

### 2. Start Services

1. Go to **Dashboard** tab
2. Click **Start** on the services you want to run:
   - Apache2 or Nginx
   - MySQL or PostgreSQL
   - PHP 8.2 FPM

### 3. Create Your First Project

#### Option A: Quick Create

1. Go to **Projects** tab
2. Click **Create Project**
3. Enter project name (e.g., "myproject")
4. Select project type (Empty PHP, HTML, Laravel, WordPress)
5. Check "Create Virtual Host" and "Enable SSL" if desired
6. Click **Create**

#### Option B: Manual Setup

1. Create project directory:
   ```bash
   mkdir -p ~/projects/myproject
   echo "<?php phpinfo(); ?>" > ~/projects/myproject/index.php
   ```

2. Create virtual host:
   - Go to **Dashboard** tab
   - Click **Create Virtual Host**
   - Enter project name: `myproject`
   - Browse to document root: `/home/augie/projects/myproject`
   - Select web server and PHP version
   - Click **Create**

3. Access your project:
   - Open browser: `http://myproject.test`
   - Or with SSL: `https://myproject.test`

### 4. Create a Database

1. Go to **Database** tab
2. Click **Create MySQL Database** or **Create PostgreSQL Database**
3. Enter database name (e.g., "myproject_db")
4. Enter username and password (optional)
5. Click **Create**
6. Copy the connection string for your application

## Common Tasks

### Create a Laravel Project

1. Make sure Composer is installed (Packages tab)
2. Go to Projects tab → Create Project
3. Enter project name
4. Select "Laravel Project"
5. Check "Create Virtual Host" and "Enable SSL"
6. Click Create (this may take a few minutes)
7. Access: `http://projectname.test`

### Create a WordPress Site

1. Go to Projects tab → Create Project
2. Enter project name
3. Select "WordPress Project"
4. Check "Create Virtual Host"
5. Click Create
6. Access: `http://projectname.test`
7. Follow WordPress installation wizard

### Switch PHP Version

1. Install desired PHP version from Packages tab
2. When creating virtual host, select the PHP version
3. For existing sites, edit the virtual host configuration manually

### Enable SSL for Existing Site

1. Go to Dashboard → Create Virtual Host
2. Enter the same project name and document root
3. Check "Enable SSL"
4. Click Create (it will update the existing configuration)

## Troubleshooting

### "Permission Denied" Errors

Make sure pkexec is installed:
```bash
sudo apt-get install policykit-1
```

### Service Won't Start

Check if the service is installed:
```bash
systemctl status apache2  # or nginx, mysql, etc.
```

Install if needed:
```bash
sudo apt-get install apache2
```

### Virtual Host Not Working

1. Check if web server is running (Dashboard tab)
2. Verify domain in /etc/hosts:
   ```bash
   cat /etc/hosts | grep myproject
   ```
3. Check web server configuration:
   ```bash
   # For Apache
   ls -la /etc/apache2/sites-enabled/
   
   # For Nginx
   ls -la /etc/nginx/sites-enabled/
   ```

### Port Already in Use

If port 80 is already in use:
```bash
# Check what's using port 80
sudo lsof -i :80

# Stop the conflicting service
sudo systemctl stop <service-name>
```

## Tips

- **System Tray**: The application runs in the system tray. Double-click to show/hide.
- **Auto-start**: Enable auto-start for services in Settings tab
- **Projects Root**: Default is `~/projects`, change in Settings if needed
- **Logs**: View service logs with: `journalctl -u apache2 -f`
- **Backup**: Always backup databases before major changes

## Next Steps

- Explore the Packages tab to install additional tools
- Create multiple projects and test virtual hosts
- Set up databases for your applications
- Configure your preferred code editor in Settings

Enjoy developing with LinuxDev Manager! 🚀
