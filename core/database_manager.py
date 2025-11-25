"""Database manager for MySQL, MariaDB, and PostgreSQL."""
from typing import Tuple, List, Optional
from utils.system_utils import run_command


class DatabaseManager:
    """Manages databases and database users."""
    
    def __init__(self):
        """Initialize database manager."""
        pass
    
    # MySQL/MariaDB methods
    
    def create_mysql_database(
        self,
        database_name: str,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create MySQL/MariaDB database and optionally a user.
        
        Args:
            database_name: Name of the database
            username: Username (optional)
            password: Password (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Create database
        cmd = f"mysql -e \"CREATE DATABASE IF NOT EXISTS {database_name};\""
        returncode, stdout, stderr = run_command(cmd, use_sudo=True)
        
        if returncode != 0:
            return False, f"Failed to create database: {stderr}"
        
        # Create user if specified
        if username and password:
            cmd = f"mysql -e \"CREATE USER IF NOT EXISTS '{username}'@'localhost' IDENTIFIED BY '{password}';\""
            returncode, _, stderr = run_command(cmd, use_sudo=True)
            
            if returncode != 0:
                return False, f"Failed to create user: {stderr}"
            
            # Grant privileges
            cmd = f"mysql -e \"GRANT ALL PRIVILEGES ON {database_name}.* TO '{username}'@'localhost'; FLUSH PRIVILEGES;\""
            returncode, _, stderr = run_command(cmd, use_sudo=True)
            
            if returncode != 0:
                return False, f"Failed to grant privileges: {stderr}"
            
            return True, f"Database and user created successfully"
        
        return True, f"Database created successfully: {database_name}"
    
    def delete_mysql_database(self, database_name: str) -> Tuple[bool, str]:
        """
        Delete MySQL/MariaDB database.
        
        Args:
            database_name: Name of the database
            
        Returns:
            Tuple of (success, message)
        """
        cmd = f"mysql -e \"DROP DATABASE IF EXISTS {database_name};\""
        returncode, stdout, stderr = run_command(cmd, use_sudo=True)
        
        if returncode == 0:
            return True, f"Database deleted: {database_name}"
        else:
            return False, f"Failed to delete database: {stderr}"
    
    def list_mysql_databases(self) -> List[str]:
        """
        List all MySQL/MariaDB databases.
        
        Returns:
            List of database names
        """
        cmd = "mysql -e \"SHOW DATABASES;\""
        returncode, stdout, stderr = run_command(cmd, use_sudo=True)
        
        if returncode == 0:
            databases = []
            for line in stdout.strip().split('\n')[1:]:  # Skip header
                db_name = line.strip()
                if db_name and db_name not in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                    databases.append(db_name)
            return databases
        else:
            return []
    
    def import_mysql_database(
        self,
        database_name: str,
        sql_file: str
    ) -> Tuple[bool, str]:
        """
        Import SQL file into MySQL/MariaDB database.
        
        Args:
            database_name: Name of the database
            sql_file: Path to SQL file
            
        Returns:
            Tuple of (success, message)
        """
        cmd = f"mysql {database_name} < {sql_file}"
        returncode, stdout, stderr = run_command(cmd, use_sudo=True)
        
        if returncode == 0:
            return True, f"Database imported successfully"
        else:
            return False, f"Failed to import database: {stderr}"
    
    def export_mysql_database(
        self,
        database_name: str,
        output_file: str
    ) -> Tuple[bool, str]:
        """
        Export MySQL/MariaDB database to SQL file.
        
        Args:
            database_name: Name of the database
            output_file: Path to output SQL file
            
        Returns:
            Tuple of (success, message)
        """
        cmd = f"mysqldump {database_name} > {output_file}"
        returncode, stdout, stderr = run_command(cmd, use_sudo=True)
        
        if returncode == 0:
            return True, f"Database exported to {output_file}"
        else:
            return False, f"Failed to export database: {stderr}"
    
    # PostgreSQL methods
    
    def create_postgresql_database(
        self,
        database_name: str,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Create PostgreSQL database and optionally a user.
        
        Args:
            database_name: Name of the database
            username: Username (optional)
            password: Password (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Create user if specified
        if username and password:
            cmd = f"sudo -u postgres psql -c \"CREATE USER {username} WITH PASSWORD '{password}';\""
            returncode, _, stderr = run_command(cmd, use_sudo=False)
            
            if returncode != 0 and "already exists" not in stderr:
                return False, f"Failed to create user: {stderr}"
        
        # Create database
        owner_clause = f"OWNER {username}" if username else ""
        cmd = f"sudo -u postgres psql -c \"CREATE DATABASE {database_name} {owner_clause};\""
        returncode, stdout, stderr = run_command(cmd, use_sudo=False)
        
        if returncode == 0:
            return True, f"PostgreSQL database created successfully"
        else:
            if "already exists" in stderr:
                return True, f"Database already exists: {database_name}"
            return False, f"Failed to create database: {stderr}"
    
    def delete_postgresql_database(self, database_name: str) -> Tuple[bool, str]:
        """
        Delete PostgreSQL database.
        
        Args:
            database_name: Name of the database
            
        Returns:
            Tuple of (success, message)
        """
        cmd = f"sudo -u postgres psql -c \"DROP DATABASE IF EXISTS {database_name};\""
        returncode, stdout, stderr = run_command(cmd, use_sudo=False)
        
        if returncode == 0:
            return True, f"Database deleted: {database_name}"
        else:
            return False, f"Failed to delete database: {stderr}"
    
    def list_postgresql_databases(self) -> List[str]:
        """
        List all PostgreSQL databases.
        
        Returns:
            List of database names
        """
        cmd = "sudo -u postgres psql -c \"\\l\" -t"
        returncode, stdout, stderr = run_command(cmd, use_sudo=False)
        
        if returncode == 0:
            databases = []
            for line in stdout.strip().split('\n'):
                parts = line.split('|')
                if parts:
                    db_name = parts[0].strip()
                    if db_name and db_name not in ['postgres', 'template0', 'template1']:
                        databases.append(db_name)
            return databases
        else:
            return []
    
    def get_connection_string(
        self,
        db_type: str,
        database_name: str,
        username: str = 'root',
        password: str = '',
        host: str = 'localhost',
        port: Optional[int] = None
    ) -> str:
        """
        Generate database connection string.
        
        Args:
            db_type: Database type ('mysql', 'postgresql')
            database_name: Database name
            username: Username
            password: Password
            host: Host
            port: Port (optional)
            
        Returns:
            Connection string
        """
        if db_type == 'mysql':
            default_port = port or 3306
            return f"mysql://{username}:{password}@{host}:{default_port}/{database_name}"
        elif db_type == 'postgresql':
            default_port = port or 5432
            return f"postgresql://{username}:{password}@{host}:{default_port}/{database_name}"
        else:
            return ""
