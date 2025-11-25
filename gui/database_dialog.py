"""Database creation dialog."""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt
from core.database_manager import DatabaseManager


class DatabaseDialog(QDialog):
    """Dialog for creating databases."""
    
    def __init__(self, database_manager: DatabaseManager, db_type: str = 'mysql', parent=None):
        """
        Initialize dialog.
        
        Args:
            database_manager: Database manager instance
            db_type: Database type ('mysql' or 'postgresql')
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.database_manager = database_manager
        self.db_type = db_type
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        db_name = "MySQL" if self.db_type == 'mysql' else "PostgreSQL"
        self.setWindowTitle(f'Create {db_name} Database')
        self.setMinimumWidth(450)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Form
        form_group = QGroupBox(f"{db_name} Database Configuration")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        # Database name
        self.db_name_input = QLineEdit()
        self.db_name_input.setPlaceholderText("e.g., my_database")
        form_layout.addRow("Database Name:", self.db_name_input)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("e.g., db_user (optional)")
        form_layout.addRow("Username:", self.username_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Leave empty for no user creation")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Password:", self.password_input)
        
        layout.addWidget(form_group)
        
        # Info label
        info_label = QLabel("Note: If you provide username and password, a new database user will be created with full privileges on this database.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #757575; font-size: 9pt;")
        layout.addWidget(info_label)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Create")
        create_btn.setProperty("class", "success")
        create_btn.clicked.connect(self.create_database)
        buttons_layout.addWidget(create_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_database(self):
        """Create database."""
        db_name = self.db_name_input.text().strip()
        username = self.username_input.text().strip() or None
        password = self.password_input.text().strip() or None
        
        # Validate inputs
        if not db_name:
            QMessageBox.warning(self, "Validation Error", "Please enter a database name")
            return
        
        if username and not password:
            QMessageBox.warning(self, "Validation Error", "Please enter a password for the user")
            return
        
        # Create database
        if self.db_type == 'mysql':
            success, message = self.database_manager.create_mysql_database(
                db_name, username, password
            )
        else:
            success, message = self.database_manager.create_postgresql_database(
                db_name, username, password
            )
        
        if success:
            # Show connection string
            if username and password:
                conn_str = self.database_manager.get_connection_string(
                    self.db_type, db_name, username, password
                )
                message += f"\n\nConnection String:\n{conn_str}"
            
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)
