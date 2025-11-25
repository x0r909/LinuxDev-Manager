#!/usr/bin/env python3
"""LinuxDev Manager - Web Development Environment Manager for Linux."""
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Check if pkexec is available
    import shutil
    if not shutil.which('pkexec'):
        print("Error: pkexec is not installed.")
        print("Please install PolicyKit by running:")
        print("  sudo apt-get install policykit-1")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    app.setApplicationName('LinuxDev Manager')
    app.setOrganizationName('LinuxDev')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
