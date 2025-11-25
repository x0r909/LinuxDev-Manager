"""Service manager for controlling system services."""
import psutil
from typing import List, Dict, Optional, Tuple
from utils.system_utils import run_command


class ServiceManager:
    """Manages system services using systemd."""
    
    # Common web development services
    SERVICES = {
        'apache2': 'Apache Web Server',
        'nginx': 'Nginx Web Server',
        'mysql': 'MySQL Database',
        'mariadb': 'MariaDB Database',
        'postgresql': 'PostgreSQL Database',
        'redis-server': 'Redis Cache',
        'mongodb': 'MongoDB Database',
        'php8.5-fpm': 'PHP 8.5 FPM',
        'php8.2-fpm': 'PHP 8.2 FPM',
        'php8.1-fpm': 'PHP 8.1 FPM',
        'php8.0-fpm': 'PHP 8.0 FPM',
        'php7.4-fpm': 'PHP 7.4 FPM',
    }
    
    def __init__(self):
        """Initialize service manager."""
        pass
    
    def get_service_status(self, service_name: str) -> str:
        """
        Get service status.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Status: 'running', 'stopped', 'not_installed', 'error'
        """
        returncode, stdout, stderr = run_command(
            f'systemctl is-active {service_name}',
            use_sudo=False
        )
        
        if returncode == 0:
            status = stdout.strip()
            if status == 'active':
                return 'running'
            elif status == 'inactive':
                return 'stopped'
            else:
                return 'stopped'
        else:
            # Check if service exists
            returncode, _, _ = run_command(
                f'systemctl list-unit-files {service_name}.service',
                use_sudo=False
            )
            if returncode == 0:
                return 'stopped'
            else:
                return 'not_installed'
    
    def start_service(self, service_name: str) -> Tuple[bool, str]:
        """
        Start a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = run_command(
            f'systemctl start {service_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Service {service_name} started successfully"
        else:
            return False, f"Failed to start {service_name}: {stderr}"
    
    def stop_service(self, service_name: str) -> Tuple[bool, str]:
        """
        Stop a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = run_command(
            f'systemctl stop {service_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Service {service_name} stopped successfully"
        else:
            return False, f"Failed to stop {service_name}: {stderr}"
    
    def restart_service(self, service_name: str) -> Tuple[bool, str]:
        """
        Restart a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = run_command(
            f'systemctl restart {service_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Service {service_name} restarted successfully"
        else:
            return False, f"Failed to restart {service_name}: {stderr}"
    
    def enable_service(self, service_name: str) -> Tuple[bool, str]:
        """
        Enable service to start on boot.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = run_command(
            f'systemctl enable {service_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Service {service_name} enabled for auto-start"
        else:
            return False, f"Failed to enable {service_name}: {stderr}"
    
    def disable_service(self, service_name: str) -> Tuple[bool, str]:
        """
        Disable service from starting on boot.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Tuple of (success, message)
        """
        returncode, stdout, stderr = run_command(
            f'systemctl disable {service_name}',
            use_sudo=True
        )
        
        if returncode == 0:
            return True, f"Service {service_name} disabled from auto-start"
        else:
            return False, f"Failed to disable {service_name}: {stderr}"
    
    def is_enabled(self, service_name: str) -> bool:
        """
        Check if service is enabled for auto-start.
        
        Args:
            service_name: Name of the service
            
        Returns:
            True if enabled
        """
        returncode, stdout, stderr = run_command(
            f'systemctl is-enabled {service_name}',
            use_sudo=False
        )
        
        return returncode == 0 and stdout.strip() == 'enabled'
    
    def get_service_logs(self, service_name: str, lines: int = 50) -> str:
        """
        Get service logs.
        
        Args:
            service_name: Name of the service
            lines: Number of lines to retrieve
            
        Returns:
            Log content
        """
        returncode, stdout, stderr = run_command(
            f'journalctl -u {service_name} -n {lines} --no-pager',
            use_sudo=False
        )
        
        if returncode == 0:
            return stdout
        else:
            return f"Failed to retrieve logs: {stderr}"
    
    def get_all_services_status(self) -> Dict[str, dict]:
        """
        Get status of all known services.
        
        Returns:
            Dictionary of service statuses
        """
        statuses = {}
        
        for service_name, description in self.SERVICES.items():
            status = self.get_service_status(service_name)
            enabled = self.is_enabled(service_name) if status != 'not_installed' else False
            
            statuses[service_name] = {
                'description': description,
                'status': status,
                'enabled': enabled
            }
        
        return statuses
    
    def get_service_port(self, service_name: str) -> Optional[int]:
        """
        Get the port a service is listening on.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Port number or None
        """
        # Common service ports
        ports = {
            'apache2': 80,
            'nginx': 80,
            'mysql': 3306,
            'mariadb': 3306,
            'postgresql': 5432,
            'redis-server': 6379,
            'mongodb': 27017,
        }
        
        return ports.get(service_name)
    
    def is_port_in_use(self, port: int) -> bool:
        """
        Check if a port is in use.
        
        Args:
            port: Port number
            
        Returns:
            True if port is in use
        """
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                return True
        return False
