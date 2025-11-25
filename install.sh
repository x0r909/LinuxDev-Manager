#!/bin/bash
# Installation script for LinuxDev Manager

echo "======================================"
echo "LinuxDev Manager Installation"
echo "======================================"
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This application only works on Linux"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python dependencies"
    exit 1
fi

# Check and install pkexec (policykit-1)
echo ""
echo "Checking for pkexec..."
if ! command -v pkexec &> /dev/null; then
    echo "pkexec not found. Installing policykit-1..."
    sudo apt-get update
    sudo apt-get install -y policykit-1
    
    if [ $? -ne 0 ]; then
        echo "Warning: Failed to install policykit-1"
        echo "Please install it manually: sudo apt-get install policykit-1"
    else
        echo "policykit-1 installed successfully"
    fi
else
    echo "pkexec is already installed"
fi

# Install nvm and Node.js
echo ""
echo "Installing nvm (Node Version Manager)..."
if [ ! -d "$HOME/.nvm" ]; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
    
    if [ $? -eq 0 ]; then
        echo "nvm installed successfully"
        
        # Load nvm
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        
        # Install Node.js v24
        echo ""
        echo "Installing Node.js v24..."
        nvm install 24
        
        if [ $? -eq 0 ]; then
            echo "Node.js v24 installed successfully"
            node_version=$(node -v)
            npm_version=$(npm -v)
            echo "Node.js version: $node_version"
            echo "npm version: $npm_version"
        else
            echo "Warning: Failed to install Node.js v24"
        fi
    else
        echo "Warning: Failed to install nvm"
    fi
else
    echo "nvm is already installed"
fi

# Create projects directory
projects_dir="$HOME/projects"
if [ ! -d "$projects_dir" ]; then
    echo ""
    echo "Creating projects directory: $projects_dir"
    mkdir -p "$projects_dir"
fi

# Create config directory
config_dir="$HOME/.linuxdev-manager"
if [ ! -d "$config_dir" ]; then
    echo "Creating config directory: $config_dir"
    mkdir -p "$config_dir"
fi

# Make main.py executable
chmod +x main.py

# Create desktop entry
desktop_file="$HOME/.local/share/applications/linuxdev-manager.desktop"
echo ""
echo "Creating desktop entry..."

cat > "$desktop_file" << EOF
[Desktop Entry]
Name=LinuxDev Manager
Comment=Web Development Environment Manager
Exec=$(pwd)/main.py
Icon=applications-development
Terminal=false
Type=Application
Categories=Development;
EOF

chmod +x "$desktop_file"

echo ""
echo "======================================"
echo "Installation completed successfully!"
echo "======================================"
echo ""
echo "You can now run the application with:"
echo "  python3 main.py"
echo ""
echo "Or search for 'LinuxDev Manager' in your applications menu"
echo ""
echo "Note: Administrative operations will prompt for authentication using pkexec."
echo ""
