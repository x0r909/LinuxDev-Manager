"""Project manager for managing web projects."""
import os
from typing import List, Dict, Tuple, Optional
from utils.system_utils import run_command
from core.config_manager import ConfigManager


class ProjectManager:
    """Manages web development projects."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize project manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
    
    def get_projects(self) -> List[Dict[str, str]]:
        """
        Get list of projects in the projects root directory.
        
        Returns:
            List of project dictionaries
        """
        projects_root = self.config.get_projects_root()
        
        if not os.path.exists(projects_root):
            return []
        
        projects = []
        
        try:
            for item in os.listdir(projects_root):
                item_path = os.path.join(projects_root, item)
                
                if os.path.isdir(item_path):
                    project_type = self._detect_project_type(item_path)
                    
                    projects.append({
                        'name': item,
                        'path': item_path,
                        'type': project_type,
                        'url': f"http://{item}{self.config.get_domain_extension()}"
                    })
        except:
            pass
        
        return projects
    
    def _detect_project_type(self, project_path: str) -> str:
        """
        Detect project type based on files.
        
        Args:
            project_path: Path to project
            
        Returns:
            Project type
        """
        # Laravel
        if os.path.exists(os.path.join(project_path, 'artisan')):
            return 'Laravel'
        
        # WordPress
        if os.path.exists(os.path.join(project_path, 'wp-config.php')):
            return 'WordPress'
        
        # Symfony
        if os.path.exists(os.path.join(project_path, 'symfony.lock')):
            return 'Symfony'
        
        # Node.js
        if os.path.exists(os.path.join(project_path, 'package.json')):
            return 'Node.js'
        
        # Python
        if os.path.exists(os.path.join(project_path, 'requirements.txt')):
            return 'Python'
        
        # Generic PHP
        if any(f.endswith('.php') for f in os.listdir(project_path)):
            return 'PHP'
        
        # Generic HTML
        if any(f.endswith('.html') for f in os.listdir(project_path)):
            return 'HTML'
        
        return 'Unknown'
    
    def create_project(
        self,
        project_name: str,
        project_type: str = 'empty'
    ) -> Tuple[bool, str]:
        """
        Create a new project.
        
        Args:
            project_name: Name of the project
            project_type: Type of project ('empty', 'laravel', 'wordpress', etc.)
            
        Returns:
            Tuple of (success, message)
        """
        projects_root = self.config.get_projects_root()
        project_path = os.path.join(projects_root, project_name)
        
        # Check if project already exists
        if os.path.exists(project_path):
            return False, f"Project already exists: {project_name}"
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create project based on type
        if project_type == 'empty':
            # Create basic index.php
            index_content = """<?php
phpinfo();
?>"""
            with open(os.path.join(project_path, 'index.php'), 'w') as f:
                f.write(index_content)
            
            return True, f"Empty project created: {project_name}"
        
        elif project_type == 'laravel':
            # Create Laravel project using Composer
            returncode, stdout, stderr = run_command(
                f'composer create-project laravel/laravel "{project_path}"',
                use_sudo=False
            )
            
            if returncode == 0:
                return True, f"Laravel project created: {project_name}"
            else:
                return False, f"Failed to create Laravel project: {stderr}"
        
        elif project_type == 'wordpress':
            # Download WordPress
            returncode, stdout, stderr = run_command(
                f'wget -O /tmp/wordpress.tar.gz https://wordpress.org/latest.tar.gz && '
                f'tar -xzf /tmp/wordpress.tar.gz -C /tmp && '
                f'mv /tmp/wordpress/* "{project_path}/" && '
                f'rm -rf /tmp/wordpress /tmp/wordpress.tar.gz',
                use_sudo=False
            )
            
            if returncode == 0:
                return True, f"WordPress project created: {project_name}"
            else:
                return False, f"Failed to create WordPress project: {stderr}"
        
        elif project_type == 'html':
            # Create basic HTML project
            index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{}</title>
</head>
<body>
    <h1>Welcome to {}</h1>
</body>
</html>""".format(project_name, project_name)
            
            with open(os.path.join(project_path, 'index.html'), 'w') as f:
                f.write(index_content)
            
            return True, f"HTML project created: {project_name}"
        
        else:
            return False, f"Unsupported project type: {project_type}"
    
    def delete_project(self, project_name: str) -> Tuple[bool, str]:
        """
        Delete a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Tuple of (success, message)
        """
        projects_root = self.config.get_projects_root()
        project_path = os.path.join(projects_root, project_name)
        
        if not os.path.exists(project_path):
            return False, f"Project not found: {project_name}"
        
        # Delete project directory
        returncode, stdout, stderr = run_command(
            f'rm -rf "{project_path}"',
            use_sudo=False
        )
        
        if returncode == 0:
            return True, f"Project deleted: {project_name}"
        else:
            return False, f"Failed to delete project: {stderr}"
    
    def open_in_browser(self, project_name: str) -> Tuple[bool, str]:
        """
        Open project in default browser.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Tuple of (success, message)
        """
        url = f"http://{project_name}{self.config.get_domain_extension()}"
        
        returncode, stdout, stderr = run_command(
            f'xdg-open "{url}"',
            use_sudo=False
        )
        
        if returncode == 0:
            return True, f"Opened in browser: {url}"
        else:
            return False, f"Failed to open browser: {stderr}"
    
    def open_in_terminal(self, project_name: str) -> Tuple[bool, str]:
        """
        Open project directory in terminal.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Tuple of (success, message)
        """
        projects_root = self.config.get_projects_root()
        project_path = os.path.join(projects_root, project_name)
        
        if not os.path.exists(project_path):
            return False, f"Project not found: {project_name}"
        
        terminal = self.config.get('settings.terminal_emulator', 'gnome-terminal')
        
        returncode, stdout, stderr = run_command(
            f'{terminal} --working-directory="{project_path}"',
            use_sudo=False
        )
        
        if returncode == 0:
            return True, f"Opened in terminal"
        else:
            return False, f"Failed to open terminal: {stderr}"
    
    def open_in_editor(self, project_name: str) -> Tuple[bool, str]:
        """
        Open project in code editor.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Tuple of (success, message)
        """
        projects_root = self.config.get_projects_root()
        project_path = os.path.join(projects_root, project_name)
        
        if not os.path.exists(project_path):
            return False, f"Project not found: {project_name}"
        
        editor = self.config.get('settings.code_editor', 'code')
        
        returncode, stdout, stderr = run_command(
            f'{editor} "{project_path}"',
            use_sudo=False
        )
        
        if returncode == 0:
            return True, f"Opened in editor"
        else:
            return False, f"Failed to open editor: {stderr}"
