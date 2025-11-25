"""Project creation dialog."""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QMessageBox,
    QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt
from core.project_manager import ProjectManager
from core.vhost_manager import VHostManager
from core.ssl_manager import SSLManager
from core.config_manager import ConfigManager


class ProjectDialog(QDialog):
    """Dialog for creating projects."""
    
    def __init__(self, project_manager: ProjectManager, vhost_manager: VHostManager,
                 ssl_manager: SSLManager, config: ConfigManager, parent=None):
        """
        Initialize dialog.
        
        Args:
            project_manager: Project manager instance
            vhost_manager: Virtual host manager instance
            ssl_manager: SSL manager instance
            config: Configuration manager instance
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.project_manager = project_manager
        self.vhost_manager = vhost_manager
        self.ssl_manager = ssl_manager
        self.config = config
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle('Create Project')
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Form
        form_group = QGroupBox("Project Configuration")
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)
        
        # Project name
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("e.g., myproject")
        form_layout.addRow("Project Name:", self.project_name_input)
        
        # Project type
        self.project_type_combo = QComboBox()
        self.project_type_combo.addItems([
            'Empty PHP Project',
            'HTML Project',
            'Laravel Project',
            'WordPress Project'
        ])
        form_layout.addRow("Project Type:", self.project_type_combo)
        
        # Create virtual host
        self.create_vhost_checkbox = QCheckBox("Create Virtual Host")
        self.create_vhost_checkbox.setChecked(True)
        form_layout.addRow("", self.create_vhost_checkbox)
        
        # Enable SSL
        self.ssl_checkbox = QCheckBox("Enable SSL (HTTPS)")
        form_layout.addRow("", self.ssl_checkbox)
        
        layout.addWidget(form_group)
        
        # Info label
        info_label = QLabel(f"Project will be created in: {self.config.get_projects_root()}")
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
        create_btn.clicked.connect(self.create_project)
        buttons_layout.addWidget(create_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_project(self):
        """Create project."""
        project_name = self.project_name_input.text().strip()
        project_type_text = self.project_type_combo.currentText()
        create_vhost = self.create_vhost_checkbox.isChecked()
        enable_ssl = self.ssl_checkbox.isChecked()
        
        # Validate inputs
        if not project_name:
            QMessageBox.warning(self, "Validation Error", "Please enter a project name")
            return
        
        # Map project type
        type_map = {
            'Empty PHP Project': 'empty',
            'HTML Project': 'html',
            'Laravel Project': 'laravel',
            'WordPress Project': 'wordpress'
        }
        project_type = type_map.get(project_type_text, 'empty')
        
        # Create project
        success, message = self.project_manager.create_project(project_name, project_type)
        
        if not success:
            QMessageBox.critical(self, "Error", message)
            return
        
        # Create virtual host if requested
        if create_vhost:
            import os
            projects_root = self.config.get_projects_root()
            document_root = os.path.join(projects_root, project_name)
            
            # For Laravel, use public directory
            if project_type == 'laravel':
                document_root = os.path.join(document_root, 'public')
            
            # Generate SSL certificate if needed
            if enable_ssl:
                domain = f"{project_name}{self.config.get_domain_extension()}"
                ssl_success, ssl_message = self.ssl_manager.generate_self_signed_certificate(domain)
                
                if not ssl_success:
                    QMessageBox.warning(self, "SSL Warning", f"Project created but SSL failed: {ssl_message}")
            
            # Create virtual host
            vhost_success, vhost_message = self.vhost_manager.create_virtual_host(
                project_name,
                document_root,
                self.config.get_default_web_server(),
                self.config.get_default_php_version(),
                enable_ssl
            )
            
            if not vhost_success:
                QMessageBox.warning(self, "Virtual Host Warning", 
                                  f"Project created but virtual host failed: {vhost_message}")
        
        QMessageBox.information(self, "Success", 
                              f"Project created successfully!\n\n"
                              f"URL: http://{project_name}{self.config.get_domain_extension()}")
        self.accept()
