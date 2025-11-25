"""Validation utilities for user inputs."""
import re
import os


def validate_domain_name(domain: str) -> bool:
    """
    Validate domain name format.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        True if valid
    """
    if not domain or len(domain) > 253:
        return False
    
    # Allow localhost and .test domains
    if domain == 'localhost':
        return True
    
    # Domain pattern
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    return bool(re.match(pattern, domain))


def validate_path(path: str, must_exist: bool = False) -> bool:
    """
    Validate file/directory path.
    
    Args:
        path: Path to validate
        must_exist: Whether path must exist
        
    Returns:
        True if valid
    """
    if not path:
        return False
    
    # Check for invalid characters
    if any(char in path for char in ['\0', '\n', '\r']):
        return False
    
    if must_exist:
        return os.path.exists(path)
    
    return True


def validate_database_name(name: str) -> bool:
    """
    Validate database name.
    
    Args:
        name: Database name to validate
        
    Returns:
        True if valid
    """
    if not name or len(name) > 64:
        return False
    
    # Database name pattern (alphanumeric, underscore, hyphen)
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, name))


def validate_username(username: str) -> bool:
    """
    Validate username.
    
    Args:
        username: Username to validate
        
    Returns:
        True if valid
    """
    if not username or len(username) > 32:
        return False
    
    # Username pattern
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, username))


def validate_port(port: int) -> bool:
    """
    Validate port number.
    
    Args:
        port: Port number to validate
        
    Returns:
        True if valid
    """
    return isinstance(port, int) and 1 <= port <= 65535


def validate_ip_address(ip: str) -> bool:
    """
    Validate IP address (IPv4).
    
    Args:
        ip: IP address to validate
        
    Returns:
        True if valid
    """
    if not ip:
        return False
    
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))


def validate_email(email: str) -> bool:
    """
    Validate email address.
    
    Args:
        email: Email to validate
        
    Returns:
        True if valid
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*\0]', '', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    return filename


def sanitize_domain(domain: str) -> str:
    """
    Sanitize domain name.
    
    Args:
        domain: Domain to sanitize
        
    Returns:
        Sanitized domain
    """
    # Convert to lowercase
    domain = domain.lower()
    # Remove invalid characters
    domain = re.sub(r'[^a-z0-9.-]', '', domain)
    # Remove leading/trailing dots and hyphens
    domain = domain.strip('.-')
    return domain
