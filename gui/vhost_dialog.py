"""Virtual host creation dialog."""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QFileDialog, QMessageBox,
    QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt
from core.vhost_manager import VHostManager
from core.ssl_manager import SSLManager
from core.config_manager import ConfigManager


class VHostDialog(QDialog):
    """Dialog for creating virtual hosts."""
    
    def __init__(self, vhost_manager: VHostManager, ssl_manager: SSLManager, 
                 config: ConfigManager, parent=None):
        """
        Initialize dialog.
        
        Args:
            vhost_manager: Virtual host manager instance
            ssl_manager: SSL manager instance
            config: Configuration manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.vhost_manager = vhost_manager
        self.ssl_manager = ssl_manager
        self.config = config
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle('Create Virtual Host')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Form
        form_group = QGroupBox("Virtual Host Configuration")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        # Project name
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("e.g., myproject")
        form_layout.addRow("Project Name:", self.project_name_input)
        
        # Document root
        doc_root_layout = QHBoxLayout()
        self.doc_root_input = QLineEdit()
        self.doc_root_input.setPlaceholderText("/path/to/project")
        doc_root_layout.addWidget(self.doc_root_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_document_root)
        doc_root_layout.addWidget(browse_btn)
        
        form_layout.addRow("Document Root:", doc_root_layout)
        
        # Web server
        self.web_server_combo = QComboBox()
        self.web_server_combo.addItems(['apache2', 'nginx'])
        self.web_server_combo.setCurrentText(self.config.get_default_web_server())
        form_layout.addRow("Web Server:", self.web_server_combo)
        
        # PHP version
        self.php_version_combo = QComboBox()
        self.php_version_combo.addItems(['8.2', '8.1', '8.0', '7.4'])
        self.php_version_combo.setCurrentText(self.config.get_default_php_version())
        form_layout.addRow("PHP Version:", self.php_version_combo)
        
        # Custom domain
        self.custom_domain_input = QLineEdit()
        self.custom_domain_input.setPlaceholderText(f"Leave empty for auto (projectname{self.config.get_domain_extension()})")
        form_layout.addRow("Custom Domain:", self.custom_domain_input)
        
        # Enable SSL
        self.ssl_checkbox = QCheckBox("Enable SSL (HTTPS)")
        form_layout.addRow("", self.ssl_checkbox)
        
        layout.addWidget(form_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        create_btn = QPushButton("Create")
        create_btn.setProperty("class", "success")
        create_btn.clicked.connect(self.create_vhost)
        buttons_layout.addWidget(create_btn)
        
        layout.addLayout(buttons_layout)
    
    def browse_document_root(self):
        """Browse for document root directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Document Root",
            self.config.get_projects_root()
        )
        
        if directory:
            self.doc_root_input.setText(directory)
    
    def create_vhost(self):
        """Create virtual host."""
        project_name = self.project_name_input.text().strip()
        document_root = self.doc_root_input.text().strip()
        web_server = self.web_server_combo.currentText()
        php_version = self.php_version_combo.currentText()
        custom_domain = self.custom_domain_input.text().strip() or None
        enable_ssl = self.ssl_checkbox.isChecked()
        
        # Validate inputs
        if not project_name:
            QMessageBox.warning(self, "Validation Error", "Please enter a project name")
            return
        
        if not document_root:
            QMessageBox.warning(self, "Validation Error", "Please select a document root")
            return
        
        # Generate SSL certificate if needed
        if enable_ssl:
            domain = custom_domain or f"{project_name}{self.config.get_domain_extension()}"
            success, message = self.ssl_manager.generate_self_signed_certificate(domain)
            
            if not success:
                QMessageBox.critical(self, "SSL Error", f"Failed to generate SSL certificate: {message}")
                return
        
        # Create virtual host
        success, message = self.vhost_manager.create_virtual_host(
            project_name,
            document_root,
            web_server,
            php_version,
            enable_ssl,
            custom_domain
        )
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", message)
