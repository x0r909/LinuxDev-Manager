"""Package installer for web development tools."""
import json
import os
from typing import List, Dict, Tuple, Optional
from utils.system_utils import run_command, check_command_exists


class PackageInstaller:
    """Manages installation of web development packages."""
    
    def __init__(self):
        """Initialize package installer."""
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.packages = self._load_packages()
    
    def _load_packages(self) -> dict:
        """Load package definitions from JSON file."""
        packages_file = os.path.join(self.app_dir, 'config', 'packages.json')
        
        try:
            with open(packages_file, 'r') as f:
                return json.load(f)
        except:
            return {
                'web_servers': [],
                'databases': [],
                'languages': [],
                'tools': []
            }
    
    def get_all_packages(self) -> Dict[str, List[dict]]:
        """
        Get all available packages.
        
        Returns:
            Dictionary of categorized packages
        """
        return self.packages
    
    def get_package_by_name(self, name: str) -> Optional[dict]:
        """
        Get package information by name.
        
        Args:
            name: Package name
            
        Returns:
            Package information or None
        """
        for category in self.packages.values():
            for package in category:
                if package['name'] == name or package['package'] == name:
                    return package
        return None
    
    def is_package_installed(self, package_name: str) -> bool:
        """
        Check if a package is installed.
        
        Args:
            package_name: Package name
            
        Returns:
            True if installed
        """
        # Check using dpkg
        returncode, stdout, _ = run_command(
            f'dpkg -l | grep -w {package_name}',
            use_sudo=False
        )
        
        if returncode == 0 and stdout.strip():
            return True
        
        # Check if command exists (for some packages)
        return check_command_exists(package_name)
    
    def install_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Install a package.
        
        Args:
            package_name: Package name
            
        Returns:
            Tuple of (success, message)
        """
        package_info = self.get_package_by_name(package_name)
        
        if not package_info:
            return False, f"Package not found: {package_name}"
        
        # Check if already installed
        if self.is_package_installed(package_info['package']):
            return True, f"Package already installed: {package_name}"
        
        # Check if package requires PPA
        if 'ppa' in package_info:
            # Ensure software-properties-common is installed (needed for add-apt-repository)
            returncode, _, _ = run_command(
                'dpkg -l | grep -w software-properties-common',
                use_sudo=False
            )
            
            if returncode != 0:
                # Install software-properties-common
                returncode, _, stderr = run_command(
                    'apt-get install -y software-properties-common',
                    use_sudo=True
                )
                if returncode != 0:
                    return False, f"Failed to install software-properties-common: {stderr}"
        
        # Update package list first
        returncode, _, stderr = run_command('apt-get update', use_sudo=True)
        if returncode != 0:
            return False, f"Failed to update package list: {stderr}"
        
        # Install package
        install_cmd = package_info['install_cmd']
        returncode, stdout, stderr = run_command(install_cmd, use_sudo=True)
        
        if returncode == 0:
            return True, f"Package installed successfully: {package_name}"
        else:
            return False, f"Failed to install {package_name}: {stderr}"

    
    def uninstall_package(self, package_name: str) -> Tuple[bool, str]:
        """
        Uninstall a package.
        
        Args:
            package_name: Package name
            
        Returns:
            Tuple of (success, message)
        """
        package_info = self.get_package_by_name(package_name)
        
        if not package_info:
            return False, f"Package not found: {package_name}"
        
        # Check if installed
        if not self.is_package_installed(package_info['package']):
            return True, f"Package not installed: {package_name}"
        
        # Uninstall package
        returncode, stdout, stderr = run_command(
            f"apt-get remove -y {package_info['package']}",
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Package uninstalled successfully: {package_name}"
        else:
            return False, f"Failed to uninstall {package_name}: {stderr}"
    
    def install_multiple_packages(self, package_names: List[str]) -> Dict[str, Tuple[bool, str]]:
        """
        Install multiple packages.
        
        Args:
            package_names: List of package names
            
        Returns:
            Dictionary of results for each package
        """
        results = {}
        
        # Update package list once
        run_command('apt-get update', use_sudo=True)
        
        for package_name in package_names:
            results[package_name] = self.install_package(package_name)
        
        return results
    
    def get_installed_packages(self) -> List[str]:
        """
        Get list of installed packages from our package list.
        
        Returns:
            List of installed package names
        """
        installed = []
        
        for category in self.packages.values():
            for package in category:
                if self.is_package_installed(package['package']):
                    installed.append(package['name'])
        
        return installed
    
    def search_packages(self, query: str) -> List[dict]:
        """
        Search for packages by name or description.
        
        Args:
            query: Search query
            
        Returns:
            List of matching packages
        """
        query = query.lower()
        results = []
        
        for category in self.packages.values():
            for package in category:
                if (query in package['name'].lower() or 
                    query in package['description'].lower() or
                    query in package['package'].lower()):
                    results.append(package)
        
        return results
    
    def install_php_extension(self, extension: str, php_version: str = '8.2') -> Tuple[bool, str]:
        """
        Install a PHP extension.
        
        Args:
            extension: Extension name (e.g., 'gd', 'curl')
            php_version: PHP version
            
        Returns:
            Tuple of (success, message)
        """
        package_name = f"php{php_version}-{extension}"
        
        returncode, stdout, stderr = run_command(
            f'apt-get install -y {package_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            # Restart PHP-FPM
            run_command(f'systemctl restart php{php_version}-fpm', use_sudo=True)
            return True, f"PHP extension installed: {extension}"
        else:
            return False, f"Failed to install PHP extension: {stderr}"
    
    def install_npm_package(self, package: str, global_install: bool = True) -> Tuple[bool, str]:
        """
        Install an npm package.
        
        Args:
            package: Package name
            global_install: Whether to install globally
            
        Returns:
            Tuple of (success, message)
        """
        if not check_command_exists('npm'):
            return False, "npm is not installed"
        
        cmd = f"npm install {'--global' if global_install else ''} {package}"
        returncode, stdout, stderr = run_command(cmd, use_sudo=global_install)
        
        if returncode == 0:
            return True, f"npm package installed: {package}"
        else:
            return False, f"Failed to install npm package: {stderr}"
    
    def install_composer_package(self, package: str, global_install: bool = True) -> Tuple[bool, str]:
        """
        Install a Composer package.
        
        Args:
            package: Package name
            global_install: Whether to install globally
            
        Returns:
            Tuple of (success, message)
        """
        if not check_command_exists('composer'):
            return False, "Composer is not installed"
        
        if global_install:
            cmd = f"composer global require {package}"
        else:
            cmd = f"composer require {package}"
        
        returncode, stdout, stderr = run_command(cmd, use_sudo=False)
        
        if returncode == 0:
            return True, f"Composer package installed: {package}"
        else:
            return False, f"Failed to install Composer package: {stderr}"
