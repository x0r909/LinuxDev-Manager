"""Virtual host manager for Apache and Nginx."""
import os
from typing import Tuple, Optional
from utils.system_utils import run_command, read_file, write_file
from utils.validators import validate_domain_name, sanitize_domain
from core.config_manager import ConfigManager


class VHostManager:
    """Manages virtual hosts for Apache and Nginx."""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize virtual host manager.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config = config_manager
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def create_virtual_host(
        self,
        project_name: str,
        document_root: str,
        web_server: str = 'apache2',
        php_version: str = '8.2',
        enable_ssl: bool = False,
        custom_domain: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create a virtual host.
        
        Args:
            project_name: Name of the project
            document_root: Document root directory
            web_server: Web server ('apache2' or 'nginx')
            php_version: PHP version
            enable_ssl: Whether to enable SSL
            custom_domain: Custom domain (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Generate domain
        if custom_domain:
            domain = sanitize_domain(custom_domain)
        else:
            domain_ext = self.config.get_domain_extension()
            domain = f"{sanitize_domain(project_name)}{domain_ext}"
        
        # Validate domain
        if not validate_domain_name(domain):
            return False, f"Invalid domain name: {domain}"
        
        # Validate document root
        if not os.path.exists(document_root):
            return False, f"Document root does not exist: {document_root}"
        
        # Create virtual host configuration
        if web_server == 'apache2':
            success, message = self._create_apache_vhost(
                domain, document_root, php_version, enable_ssl
            )
        elif web_server == 'nginx':
            success, message = self._create_nginx_vhost(
                domain, document_root, php_version, enable_ssl
            )
        else:
            return False, f"Unsupported web server: {web_server}"
        
        if not success:
            return False, message
        
        # Add to hosts file
        success, message = self._add_to_hosts(domain)
        if not success:
            return False, message
        
        return True, f"Virtual host created successfully: {domain}"
    
    def _create_apache_vhost(
        self,
        domain: str,
        document_root: str,
        php_version: str,
        enable_ssl: bool
    ) -> Tuple[bool, str]:
        """Create Apache virtual host configuration."""
        # Load template
        template_path = os.path.join(self.app_dir, 'templates', 'apache_vhost.conf')
        template = read_file(template_path, use_sudo=False)
        
        if not template:
            return False, "Failed to load Apache template"
        
        # SSL configuration
        ssl_config = ""
        if enable_ssl:
            ssl_template_path = os.path.join(self.app_dir, 'templates', 'apache_ssl.conf')
            ssl_template = read_file(ssl_template_path, use_sudo=False)
            
            if ssl_template:
                ssl_cert = f"/etc/ssl/certs/{domain}.crt"
                ssl_key = f"/etc/ssl/private/{domain}.key"
                
                ssl_config = ssl_template.format(
                    domain=domain,
                    document_root=document_root,
                    php_version=php_version,
                    ssl_cert=ssl_cert,
                    ssl_key=ssl_key
                )
        
        # Generate configuration
        config = template.format(
            domain=domain,
            document_root=document_root,
            php_version=php_version,
            ssl_config=ssl_config
        )
        
        # Write configuration file
        sites_available = self.config.get_path('apache_sites')
        config_file = os.path.join(sites_available, f"{domain}.conf")
        
        if not write_file(config_file, config, use_sudo=True):
            return False, "Failed to write Apache configuration"
        
        # Enable site
        returncode, _, stderr = run_command(f'a2ensite {domain}.conf', use_sudo=True)
        if returncode != 0:
            return False, f"Failed to enable site: {stderr}"
        
        # Enable required modules
        run_command('a2enmod rewrite', use_sudo=True)
        run_command('a2enmod ssl', use_sudo=True)
        run_command('a2enmod proxy_fcgi', use_sudo=True)
        
        # Reload Apache
        returncode, _, stderr = run_command('systemctl reload apache2', use_sudo=True)
        if returncode != 0:
            return False, f"Failed to reload Apache: {stderr}"
        
        return True, "Apache virtual host created"
    
    def _create_nginx_vhost(
        self,
        domain: str,
        document_root: str,
        php_version: str,
        enable_ssl: bool
    ) -> Tuple[bool, str]:
        """Create Nginx virtual host configuration."""
        # Load template
        template_path = os.path.join(self.app_dir, 'templates', 'nginx_vhost.conf')
        template = read_file(template_path, use_sudo=False)
        
        if not template:
            return False, "Failed to load Nginx template"
        
        # SSL configuration
        ssl_config = ""
        if enable_ssl:
            ssl_template_path = os.path.join(self.app_dir, 'templates', 'nginx_ssl.conf')
            ssl_template = read_file(ssl_template_path, use_sudo=False)
            
            if ssl_template:
                ssl_cert = f"/etc/ssl/certs/{domain}.crt"
                ssl_key = f"/etc/ssl/private/{domain}.key"
                
                ssl_config = ssl_template.format(
                    domain=domain,
                    document_root=document_root,
                    php_version=php_version,
                    ssl_cert=ssl_cert,
                    ssl_key=ssl_key
                )
        
        # Generate configuration
        config = template.format(
            domain=domain,
            document_root=document_root,
            php_version=php_version,
            ssl_config=ssl_config
        )
        
        # Write configuration file
        sites_available = self.config.get_path('nginx_sites')
        config_file = os.path.join(sites_available, domain)
        
        if not write_file(config_file, config, use_sudo=True):
            return False, "Failed to write Nginx configuration"
        
        # Enable site (create symlink)
        sites_enabled = self.config.get_path('nginx_enabled')
        symlink_path = os.path.join(sites_enabled, domain)
        
        returncode, _, stderr = run_command(
            f'ln -sf {config_file} {symlink_path}',
            use_sudo=True
        )
        if returncode != 0:
            return False, f"Failed to enable site: {stderr}"
        
        # Test configuration
        returncode, _, stderr = run_command('nginx -t', use_sudo=True)
        if returncode != 0:
            return False, f"Nginx configuration test failed: {stderr}"
        
        # Reload Nginx
        returncode, _, stderr = run_command('systemctl reload nginx', use_sudo=True)
        if returncode != 0:
            return False, f"Failed to reload Nginx: {stderr}"
        
        return True, "Nginx virtual host created"
    
    def _add_to_hosts(self, domain: str) -> Tuple[bool, str]:
        """Add domain to /etc/hosts file."""
        hosts_file = self.config.get_path('hosts_file')
        
        # Read current hosts file
        hosts_content = read_file(hosts_file, use_sudo=True)
        if hosts_content is None:
            return False, "Failed to read hosts file"
        
        # Check if domain already exists
        entry = f"127.0.0.1 {domain}"
        if entry in hosts_content:
            return True, "Domain already in hosts file"
        
        # Add entry
        new_content = hosts_content.rstrip() + f"\n{entry}\n"
        
        if not write_file(hosts_file, new_content, use_sudo=True):
            return False, "Failed to update hosts file"
        
        return True, "Domain added to hosts file"
    
    def remove_virtual_host(self, domain: str, web_server: str = 'apache2') -> Tuple[bool, str]:
        """
        Remove a virtual host.
        
        Args:
            domain: Domain name
            web_server: Web server ('apache2' or 'nginx')
            
        Returns:
            Tuple of (success, message)
        """
        if web_server == 'apache2':
            # Disable site
            run_command(f'a2dissite {domain}.conf', use_sudo=True)
            
            # Remove configuration
            sites_available = self.config.get_path('apache_sites')
            config_file = os.path.join(sites_available, f"{domain}.conf")
            run_command(f'rm -f {config_file}', use_sudo=True)
            
            # Reload Apache
            run_command('systemctl reload apache2', use_sudo=True)
        
        elif web_server == 'nginx':
            # Remove symlink
            sites_enabled = self.config.get_path('nginx_enabled')
            symlink_path = os.path.join(sites_enabled, domain)
            run_command(f'rm -f {symlink_path}', use_sudo=True)
            
            # Remove configuration
            sites_available = self.config.get_path('nginx_sites')
            config_file = os.path.join(sites_available, domain)
            run_command(f'rm -f {config_file}', use_sudo=True)
            
            # Reload Nginx
            run_command('systemctl reload nginx', use_sudo=True)
        
        # Remove from hosts file
        self._remove_from_hosts(domain)
        
        return True, f"Virtual host removed: {domain}"
    
    def _remove_from_hosts(self, domain: str) -> Tuple[bool, str]:
        """Remove domain from /etc/hosts file."""
        hosts_file = self.config.get_path('hosts_file')
        
        # Read current hosts file
        hosts_content = read_file(hosts_file, use_sudo=True)
        if hosts_content is None:
            return False, "Failed to read hosts file"
        
        # Remove entry
        lines = hosts_content.split('\n')
        new_lines = [line for line in lines if not line.strip().endswith(domain)]
        new_content = '\n'.join(new_lines)
        
        if not write_file(hosts_file, new_content, use_sudo=True):
            return False, "Failed to update hosts file"
        
        return True, "Domain removed from hosts file"
