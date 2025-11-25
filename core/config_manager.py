"""Configuration manager for application settings."""
import json
import os
from typing import Any, Optional


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to config file (default: config/app_config.json)
        """
        if config_path is None:
            # Get application directory
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(app_dir, 'config', 'app_config.json')
        
        self.config_path = config_path
        self.user_config_path = os.path.expanduser('~/.linuxdev-manager/config.json')
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        # Load default config
        default_config = {}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    default_config = json.load(f)
            except:
                pass
        
        # Load user config
        user_config = {}
        if os.path.exists(self.user_config_path):
            try:
                with open(self.user_config_path, 'r') as f:
                    user_config = json.load(f)
            except:
                pass
        
        # Merge configs (user config overrides default)
        config = default_config.copy()
        self._deep_merge(config, user_config)
        
        return config
    
    def _deep_merge(self, base: dict, override: dict):
        """Deep merge two dictionaries."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'settings.theme')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def save(self) -> bool:
        """
        Save configuration to user config file.
        
        Returns:
            True if successful
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.user_config_path), exist_ok=True)
            
            # Save config
            with open(self.user_config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            return True
        except:
            return False
    
    def reset(self):
        """Reset configuration to defaults."""
        if os.path.exists(self.user_config_path):
            os.remove(self.user_config_path)
        self.config = self._load_config()
    
    def get_projects_root(self) -> str:
        """Get projects root directory."""
        path = self.get('settings.projects_root', '~/projects')
        # Always expand user home directory
        return os.path.expanduser(path)

    
    def set_projects_root(self, path: str):
        """Set projects root directory."""
        self.set('settings.projects_root', path)
    
    def get_default_web_server(self) -> str:
        """Get default web server."""
        return self.get('settings.default_web_server', 'apache2')
    
    def set_default_web_server(self, server: str):
        """Set default web server."""
        self.set('settings.default_web_server', server)
    
    def get_default_php_version(self) -> str:
        """Get default PHP version."""
        return self.get('settings.default_php_version', '8.2')
    
    def set_default_php_version(self, version: str):
        """Set default PHP version."""
        self.set('settings.default_php_version', version)
    
    def get_domain_extension(self) -> str:
        """Get default domain extension."""
        return self.get('settings.default_domain_extension', '.test')
    
    def get_auto_start_services(self) -> list:
        """Get list of services to auto-start."""
        return self.get('settings.auto_start_services', [])
    
    def add_auto_start_service(self, service: str):
        """Add service to auto-start list."""
        services = self.get_auto_start_services()
        if service not in services:
            services.append(service)
            self.set('settings.auto_start_services', services)
    
    def remove_auto_start_service(self, service: str):
        """Remove service from auto-start list."""
        services = self.get_auto_start_services()
        if service in services:
            services.remove(service)
            self.set('settings.auto_start_services', services)
    
    def get_path(self, path_key: str) -> str:
        """
        Get system path.
        
        Args:
            path_key: Path key (e.g., 'apache_sites', 'nginx_sites')
            
        Returns:
            Path value
        """
        return self.get(f'paths.{path_key}', '')
    
    def get_theme(self) -> str:
        """Get current theme (light or dark)."""
        return self.get('settings.theme', 'light')
    
    def set_theme(self, theme: str):
        """
        Set theme preference.
        
        Args:
            theme: Theme name ('light' or 'dark')
        """
        self.set('settings.theme', theme)
        self.save()
