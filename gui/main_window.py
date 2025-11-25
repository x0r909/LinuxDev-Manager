"""Main window for LinuxDev Manager."""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QPushButton, QGroupBox, QGridLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QSystemTrayIcon,
    QMenu, QAction, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap
import sys
import os

from core.service_manager import ServiceManager
from core.config_manager import ConfigManager
from core.vhost_manager import VHostManager
from core.ssl_manager import SSLManager
from core.database_manager import DatabaseManager
from core.package_installer import PackageInstaller
from core.project_manager import ProjectManager
from gui.styles import get_light_theme, get_dark_theme, get_status_color, get_status_icon
from gui.terminal_widget import TerminalWidget
from gui.icon_helper import get_asset_icon, create_theme_icon, create_download_icon, create_trash_icon


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize managers
        self.config = ConfigManager()
        self.service_manager = ServiceManager()
        self.vhost_manager = VHostManager(self.config)
        self.ssl_manager = SSLManager(self.config)
        self.database_manager = DatabaseManager()
        self.package_installer = PackageInstaller()
        self.project_manager = ProjectManager(self.config)
        
        # Initialize theme
        self.current_theme = self.config.get_theme()
        
        # Setup UI
        self.init_ui()
        
        # Apply saved theme
        self.apply_theme(self.current_theme)
        
        # Setup system tray
        self.setup_system_tray()
        
        # Start status update timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_service_statuses)
        self.status_timer.start(5000)  # Update every 5 seconds
        
        # Initial update
        self.update_service_statuses()
        self.update_projects_list()
    
    def init_ui(self):
        """Initialize user interface."""
        self.setWindowTitle('LinuxDev Manager')
        self.setMinimumSize(1000, 700)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_dashboard_tab(), "Dashboard")
        self.tabs.addTab(self.create_projects_tab(), "Projects")
        self.tabs.addTab(self.create_packages_tab(), "Packages")
        self.tabs.addTab(self.create_database_tab(), "Database")
        self.tabs.addTab(self.create_terminal_tab(), "Terminal")
        self.tabs.addTab(self.create_settings_tab(), "Settings")
        
        main_layout.addWidget(self.tabs)
    
    def create_header(self) -> QWidget:
        """Create header widget."""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        title = QLabel("LinuxDev Manager")
        title.setProperty("class", "title")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        
        # Subtitle
        subtitle = QLabel("Web Development Environment Manager")
        subtitle.setProperty("class", "subtitle")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        
        # Title layout
        title_layout = QVBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Theme toggle button
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setObjectName("theme-toggle")
        self.theme_toggle_btn.setFixedSize(40, 40)
        self.theme_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        self.update_theme_button()
        layout.addWidget(self.theme_toggle_btn)
        
        return header
    
    def create_dashboard_tab(self) -> QWidget:
        """Create dashboard tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Services group
        services_group = QGroupBox("Services")
        services_layout = QGridLayout()
        services_group.setLayout(services_layout)
        
        # Service status labels and buttons
        self.service_widgets = {}
        
        services = [
            ('apache2', 'Apache Web Server'),
            ('nginx', 'Nginx Web Server'),
            ('mysql', 'MySQL Database'),
            ('postgresql', 'PostgreSQL Database'),
            ('redis-server', 'Redis Cache'),
            ('php8.5-fpm', 'PHP 8.5 FPM'),
            ('php8.2-fpm', 'PHP 8.2 FPM'),
        ]
        
        row = 0
        for service_name, description in services:
            # Service name and description
            name_label = QLabel(description)
            name_label.setFont(QFont('Ubuntu', 10, QFont.Bold))
            
            # Status icon
            status_icon = QLabel("●")
            status_icon.setFont(QFont('Ubuntu', 16))
            
            # Status text (running/stopped/not installed)
            status_text = QLabel("Checking...")
            status_text.setFont(QFont('Ubuntu', 9))
            status_text.setStyleSheet("color: #757575;")
            
            # Enabled/Auto-start indicator
            enabled_label = QLabel("")
            enabled_label.setFont(QFont('Ubuntu', 8))
            enabled_label.setStyleSheet("color: #9E9E9E;")
            
            # Port info
            port_label = QLabel("")
            port_label.setFont(QFont('Ubuntu', 8))
            port_label.setStyleSheet("color: #9E9E9E;")
            
            # Start button
            start_btn = QPushButton("Start")
            start_btn.setProperty("class", "success")
            start_btn.setMaximumWidth(80)
            start_btn.clicked.connect(lambda checked, s=service_name: self.start_service(s))
            
            # Stop button
            stop_btn = QPushButton("Stop")
            stop_btn.setProperty("class", "danger")
            stop_btn.setMaximumWidth(80)
            stop_btn.clicked.connect(lambda checked, s=service_name: self.stop_service(s))
            
            # Restart button
            restart_btn = QPushButton("Restart")
            restart_btn.setProperty("class", "warning")
            restart_btn.setMaximumWidth(80)
            restart_btn.clicked.connect(lambda checked, s=service_name: self.restart_service(s))
            
            # Create info layout for status text and enabled state
            info_widget = QWidget()
            info_layout = QVBoxLayout(info_widget)
            info_layout.setContentsMargins(0, 0, 0, 0)
            info_layout.setSpacing(2)
            info_layout.addWidget(status_text)
            info_layout.addWidget(enabled_label)
            info_layout.addWidget(port_label)
            
            # Add to layout
            services_layout.addWidget(status_icon, row, 0)
            services_layout.addWidget(name_label, row, 1)
            services_layout.addWidget(info_widget, row, 2)
            services_layout.addWidget(start_btn, row, 3)
            services_layout.addWidget(stop_btn, row, 4)
            services_layout.addWidget(restart_btn, row, 5)
            
            # Store widgets
            self.service_widgets[service_name] = {
                'status_icon': status_icon,
                'status_text': status_text,
                'enabled_label': enabled_label,
                'port_label': port_label,
                'name': name_label,
                'start': start_btn,
                'stop': stop_btn,
                'restart': restart_btn
            }
            
            row += 1
        
        services_layout.setColumnStretch(1, 1)
        
        layout.addWidget(services_group)
        
        # Quick actions group
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QHBoxLayout()
        actions_group.setLayout(actions_layout)
        
        # Create virtual host button
        vhost_btn = QPushButton("Create Virtual Host")
        vhost_btn.clicked.connect(self.show_create_vhost_dialog)
        actions_layout.addWidget(vhost_btn)
        
        # Create database button
        db_btn = QPushButton("Create Database")
        db_btn.clicked.connect(self.show_create_database_dialog)
        actions_layout.addWidget(db_btn)
        
        # Create project button
        project_btn = QPushButton("Create Project")
        project_btn.clicked.connect(self.show_create_project_dialog)
        actions_layout.addWidget(project_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        
        return widget
    
    def create_projects_tab(self) -> QWidget:
        """Create projects tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.update_projects_list)
        toolbar.addWidget(refresh_btn)
        
        create_btn = QPushButton("Create Project")
        create_btn.clicked.connect(self.show_create_project_dialog)
        toolbar.addWidget(create_btn)
        
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Projects table
        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(5)
        self.projects_table.setHorizontalHeaderLabels(['Name', 'Type', 'Path', 'URL', 'Actions'])
        self.projects_table.horizontalHeader().setStretchLastSection(True)
        self.projects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.projects_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.projects_table)
        
        return widget
    
    def create_packages_tab(self) -> QWidget:
        """Create packages tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Packages table
        self.packages_table = QTableWidget()
        self.packages_table.setColumnCount(5)
        self.packages_table.setHorizontalHeaderLabels(['Name', 'Category', 'Description', 'Status', 'Action'])
        self.packages_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.packages_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Set column widths
        header = self.packages_table.horizontalHeader()
        header.setStretchLastSection(False)
        self.packages_table.setColumnWidth(0, 200)  # Name
        self.packages_table.setColumnWidth(1, 120)  # Category
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Description
        self.packages_table.setColumnWidth(3, 130)  # Status
        self.packages_table.setColumnWidth(4, 130)  # Action
        
        # Set row height
        self.packages_table.verticalHeader().setDefaultSectionSize(50)
        
        # Populate packages
        self.populate_packages_table()
        
        layout.addWidget(self.packages_table)
        
        return widget
    
    def create_database_tab(self) -> QWidget:
        """Create database tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        create_mysql_btn = QPushButton("Create MySQL Database")
        create_mysql_btn.clicked.connect(lambda: self.show_create_database_dialog('mysql'))
        toolbar.addWidget(create_mysql_btn)
        
        create_pgsql_btn = QPushButton("Create PostgreSQL Database")
        create_pgsql_btn.clicked.connect(lambda: self.show_create_database_dialog('postgresql'))
        toolbar.addWidget(create_pgsql_btn)
        
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Databases info
        info_label = QLabel("Use the buttons above to create databases.\nYou can also manage databases using phpMyAdmin or command line tools.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return widget
    
    def create_terminal_tab(self) -> QWidget:
        """Create terminal tab."""
        self.terminal_widget = TerminalWidget(self.config, self.project_manager, self)
        return self.terminal_widget
    
    def create_settings_tab(self) -> QWidget:
        """Create settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Settings info
        settings_group = QGroupBox("Application Settings")
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)
        
        info_text = f"""
        <b>Projects Root:</b> {self.config.get_projects_root()}<br>
        <b>Default Web Server:</b> {self.config.get_default_web_server()}<br>
        <b>Default PHP Version:</b> {self.config.get_default_php_version()}<br>
        <b>Domain Extension:</b> {self.config.get_domain_extension()}<br>
        """
        
        info_label = QLabel(info_text)
        info_label.setTextFormat(Qt.RichText)
        settings_layout.addWidget(info_label)
        
        layout.addWidget(settings_group)
        layout.addStretch()
        
        return widget
    
    def setup_system_tray(self):
        """Setup system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set tray icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icon-32.png')
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        self.tray_icon.setToolTip('LinuxDev Manager')
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
    
    def update_service_statuses(self):
        """Update service status indicators."""
        statuses = self.service_manager.get_all_services_status()
        
        for service_name, widgets in self.service_widgets.items():
            if service_name in statuses:
                status = statuses[service_name]['status']
                enabled = statuses[service_name]['enabled']
                
                # Update status icon
                icon = get_status_icon(status)
                color = get_status_color(status)
                widgets['status_icon'].setText(icon)
                widgets['status_icon'].setStyleSheet(f"color: {color};")
                
                # Update status text
                status_text_map = {
                    'running': 'Running',
                    'stopped': 'Stopped',
                    'not_installed': 'Not Installed',
                    'error': 'Error'
                }
                widgets['status_text'].setText(status_text_map.get(status, 'Unknown'))
                widgets['status_text'].setStyleSheet(f"color: {color}; font-weight: bold;")
                
                # Update enabled/auto-start label
                if status != 'not_installed':
                    if enabled:
                        widgets['enabled_label'].setText("⚡ Auto-start enabled")
                        widgets['enabled_label'].setStyleSheet("color: #4CAF50; font-size: 8pt;")
                    else:
                        widgets['enabled_label'].setText("○ Auto-start disabled")
                        widgets['enabled_label'].setStyleSheet("color: #9E9E9E; font-size: 8pt;")
                else:
                    widgets['enabled_label'].setText("")
                
                # Update port information
                port = self.service_manager.get_service_port(service_name)
                if port and status == 'running':
                    port_in_use = self.service_manager.is_port_in_use(port)
                    if port_in_use:
                        widgets['port_label'].setText(f"🌐 Port: {port}")
                        widgets['port_label'].setStyleSheet("color: #2196F3; font-size: 8pt;")
                    else:
                        widgets['port_label'].setText(f"Port: {port}")
                        widgets['port_label'].setStyleSheet("color: #9E9E9E; font-size: 8pt;")
                else:
                    widgets['port_label'].setText("")
                
                # Enable/disable buttons
                is_running = status == 'running'
                is_installed = status != 'not_installed'
                
                widgets['start'].setEnabled(is_installed and not is_running)
                widgets['stop'].setEnabled(is_running)
                widgets['restart'].setEnabled(is_running)
    
    def start_service(self, service_name: str):
        """Start a service."""
        success, message = self.service_manager.start_service(service_name)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        
        self.update_service_statuses()
    
    def stop_service(self, service_name: str):
        """Stop a service."""
        success, message = self.service_manager.stop_service(service_name)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        
        self.update_service_statuses()
    
    def restart_service(self, service_name: str):
        """Restart a service."""
        success, message = self.service_manager.restart_service(service_name)
        
        if success:
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.critical(self, "Error", message)
        
        self.update_service_statuses()
    
    def update_projects_list(self):
        """Update projects list."""
        projects = self.project_manager.get_projects()
        
        self.projects_table.setRowCount(len(projects))
        
        for row, project in enumerate(projects):
            self.projects_table.setItem(row, 0, QTableWidgetItem(project['name']))
            self.projects_table.setItem(row, 1, QTableWidgetItem(project['type']))
            self.projects_table.setItem(row, 2, QTableWidgetItem(project['path']))
            self.projects_table.setItem(row, 3, QTableWidgetItem(project['url']))
            
            # Actions buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 4, 4, 4)
            
            browser_btn = QPushButton("Browser")
            browser_btn.clicked.connect(lambda checked, p=project['name']: self.project_manager.open_in_browser(p))
            actions_layout.addWidget(browser_btn)
            
            terminal_btn = QPushButton("Terminal")
            terminal_btn.clicked.connect(lambda checked, p=project['name']: self.project_manager.open_in_terminal(p))
            actions_layout.addWidget(terminal_btn)
            
            self.projects_table.setCellWidget(row, 4, actions_widget)
        
        # Refresh terminal widget project list if it exists
        if hasattr(self, 'terminal_widget'):
            self.terminal_widget.refresh_projects()
    
    def populate_packages_table(self):
        """Populate packages table."""
        packages = self.package_installer.get_all_packages()
        
        # Category name mapping
        category_names = {
            'web_servers': 'Web Server',
            'databases': 'Database',
            'languages': 'Language',
            'tools': 'Tool'
        }
        
        all_packages = []
        for category, pkg_list in packages.items():
            for pkg in pkg_list:
                pkg['category'] = category_names.get(category, category)
                all_packages.append(pkg)
        
        self.packages_table.setRowCount(len(all_packages))
        
        for row, package in enumerate(all_packages):
            # Name
            name_item = QTableWidgetItem(package['name'])
            name_item.setFont(QFont('Ubuntu', 10, QFont.Bold))
            self.packages_table.setItem(row, 0, name_item)
            
            # Category
            category_item = QTableWidgetItem(package['category'])
            category_item.setFont(QFont('Ubuntu', 9))
            self.packages_table.setItem(row, 1, category_item)
            
            # Description
            self.packages_table.setItem(row, 2, QTableWidgetItem(package['description']))
            
            # Check if installed
            is_installed = self.package_installer.is_package_installed(package['package'])
            
            # Status with icon
            status_icon = "✓" if is_installed else "○"
            status_text = f"{status_icon} Installed" if is_installed else f"{status_icon} Not Installed"
            status_item = QTableWidgetItem(status_text)
            status_item.setFont(QFont('Ubuntu', 10, QFont.Bold if is_installed else QFont.Normal))
            self.packages_table.setItem(row, 3, status_item)
            
            # Action button with icon and better styling
            if is_installed:
                action_btn = QPushButton("  Uninstall")
                action_btn.setIcon(create_trash_icon(20))
                action_btn.setProperty("class", "danger package-action")
                action_btn.setToolTip(f"Remove {package['name']} from your system")
                action_btn.clicked.connect(lambda checked, p=package['name']: self.uninstall_package(p))
            else:
                action_btn = QPushButton("  Install")
                action_btn.setIcon(create_download_icon(20))
                action_btn.setProperty("class", "success package-action")
                action_btn.setToolTip(f"Install {package['name']}\n{package['description']}")
                action_btn.clicked.connect(lambda checked, p=package['name']: self.install_package(p))
            
            # Set button size and styling
            action_btn.setMinimumWidth(100)
            action_btn.setMaximumWidth(120)
            action_btn.setCursor(Qt.PointingHandCursor)
            
            self.packages_table.setCellWidget(row, 4, action_btn)
    
    def install_package(self, package_name: str):
        """Install a package."""
        reply = QMessageBox.question(
            self,
            "Confirm Installation",
            f"Do you want to install {package_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.package_installer.install_package(package_name)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.populate_packages_table()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def uninstall_package(self, package_name: str):
        """Uninstall a package."""
        reply = QMessageBox.question(
            self,
            "Confirm Uninstallation",
            f"Do you want to uninstall {package_name}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.package_installer.uninstall_package(package_name)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.populate_packages_table()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def show_create_vhost_dialog(self):
        """Show create virtual host dialog."""
        from gui.vhost_dialog import VHostDialog
        dialog = VHostDialog(self.vhost_manager, self.ssl_manager, self.config, self)
        dialog.exec_()
    
    def show_create_database_dialog(self, db_type: str = 'mysql'):
        """Show create database dialog."""
        from gui.database_dialog import DatabaseDialog
        dialog = DatabaseDialog(self.database_manager, db_type, self)
        dialog.exec_()
    
    def show_create_project_dialog(self):
        """Show create project dialog."""
        from gui.project_dialog import ProjectDialog
        dialog = ProjectDialog(self.project_manager, self.vhost_manager, self.ssl_manager, self.config, self)
        if dialog.exec_():
            self.update_projects_list()
    
    def apply_theme(self, theme: str):
        """Apply theme to the application."""
        if theme == 'dark':
            self.setStyleSheet(get_dark_theme())
        else:
            self.setStyleSheet(get_light_theme())
        
        self.current_theme = theme
        self.update_theme_button()
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
        self.config.set_theme(new_theme)
    
    def update_theme_button(self):
        """Update theme toggle button icon."""
        if self.current_theme == 'dark':
            self.theme_toggle_btn.setIcon(create_theme_icon('dark', 32))
            self.theme_toggle_btn.setText('')
            self.theme_toggle_btn.setToolTip('Switch to Light Mode')
        else:
            self.theme_toggle_btn.setIcon(create_theme_icon('light', 32))
            self.theme_toggle_btn.setText('')
            self.theme_toggle_btn.setToolTip('Switch to Dark Mode')
