"""System utility functions for executing commands and system operations."""
import subprocess
import os
import shutil
from typing import Tuple, Optional, List


def run_command(command: str, use_sudo: bool = False, shell: bool = True) -> Tuple[int, str, str]:
    """
    Execute a shell command and return the result.
    
    Args:
        command: Command to execute
        use_sudo: Whether to use sudo/pkexec
        shell: Whether to use shell execution
        
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    if use_sudo and not is_root():
        # Use pkexec for GUI sudo prompt
        # Escape single quotes in the command
        escaped_command = command.replace("'", "'\"'\"'")
        command = f"pkexec bash -c '{escaped_command}'"
    
    try:
        if shell:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            process = subprocess.Popen(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        stdout, stderr = process.communicate()
        
        # Check if pkexec was cancelled
        if use_sudo and process.returncode == 126:
            return process.returncode, stdout, "Authentication cancelled by user"
        
        return process.returncode, stdout, stderr
    except Exception as e:
        return 1, "", str(e)



def run_command_async(command: str, use_sudo: bool = False) -> subprocess.Popen:
    """
    Execute a command asynchronously.
    
    Args:
        command: Command to execute
        use_sudo: Whether to use sudo
        
    Returns:
        Popen process object
    """
    if use_sudo and not is_root():
        # Escape single quotes in the command
        escaped_command = command.replace("'", "'\"'\"'")
        command = f"pkexec bash -c '{escaped_command}'"
    
    return subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def is_root() -> bool:
    """Check if running as root."""
    return os.geteuid() == 0


def check_command_exists(command: str) -> bool:
    """Check if a command exists in PATH."""
    return shutil.which(command) is not None


def get_system_info() -> dict:
    """Get system information."""
    info = {}
    
    # Get OS info
    try:
        with open('/etc/os-release', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    info[key.lower()] = value.strip('"')
    except:
        pass
    
    # Get kernel version
    returncode, stdout, _ = run_command('uname -r', use_sudo=False)
    if returncode == 0:
        info['kernel'] = stdout.strip()
    
    return info


def ensure_directory(path: str, use_sudo: bool = False) -> bool:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        use_sudo: Whether to use sudo for creation
        
    Returns:
        True if successful
    """
    if os.path.exists(path):
        return True
    
    try:
        if use_sudo:
            returncode, _, _ = run_command(f'mkdir -p "{path}"', use_sudo=True)
            return returncode == 0
        else:
            os.makedirs(path, exist_ok=True)
            return True
    except:
        return False


def read_file(path: str, use_sudo: bool = False) -> Optional[str]:
    """
    Read file contents.
    
    Args:
        path: File path
        use_sudo: Whether to use sudo
        
    Returns:
        File contents or None
    """
    try:
        if use_sudo:
            returncode, stdout, _ = run_command(f'cat "{path}"', use_sudo=True)
            return stdout if returncode == 0 else None
        else:
            with open(path, 'r') as f:
                return f.read()
    except:
        return None


def write_file(path: str, content: str, use_sudo: bool = False) -> bool:
    """
    Write content to file.
    
    Args:
        path: File path
        content: Content to write
        use_sudo: Whether to use sudo
        
    Returns:
        True if successful
    """
    try:
        if use_sudo:
            # Create temporary file and move it
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            
            returncode, _, _ = run_command(f'cp "{tmp_path}" "{path}"', use_sudo=True)
            os.unlink(tmp_path)
            return returncode == 0
        else:
            with open(path, 'w') as f:
                f.write(content)
            return True
    except:
        return False


def append_to_file(path: str, content: str, use_sudo: bool = False) -> bool:
    """
    Append content to file.
    
    Args:
        path: File path
        content: Content to append
        use_sudo: Whether to use sudo
        
    Returns:
        True if successful
    """
    existing = read_file(path, use_sudo) or ""
    return write_file(path, existing + content, use_sudo)


def get_file_owner(path: str) -> Tuple[str, str]:
    """
    Get file owner and group.
    
    Returns:
        Tuple of (owner, group)
    """
    try:
        stat_info = os.stat(path)
        import pwd
        import grp
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        group = grp.getgrgid(stat_info.st_gid).gr_name
        return owner, group
    except:
        return "", ""


def set_file_permissions(path: str, mode: int, use_sudo: bool = False) -> bool:
    """
    Set file permissions.
    
    Args:
        path: File path
        mode: Permission mode (e.g., 0o644)
        use_sudo: Whether to use sudo
        
    Returns:
        True if successful
    """
    try:
        if use_sudo:
            returncode, _, _ = run_command(f'chmod {oct(mode)[2:]} "{path}"', use_sudo=True)
            return returncode == 0
        else:
            os.chmod(path, mode)
            return True
    except:
        return False
