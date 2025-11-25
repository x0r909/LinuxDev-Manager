"""Terminal widget for embedded terminal in GUI."""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QLineEdit, QComboBox, QLabel, QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt, QProcess, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QColor
from gui.icon_helper import create_refresh_icon
import os


class TerminalWidget(QWidget):
    """Embedded terminal widget with dev environment support."""
    
    command_executed = pyqtSignal(str, int)  # command, exit_code
    
    def __init__(self, config, project_manager, parent=None):
        """Initialize terminal widget."""
        super().__init__(parent)
        
        self.config = config
        self.project_manager = project_manager
        self.current_project = None
        self.process = None
        self.command_history = []
        self.history_index = -1
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Project selector group
        selector_group = QGroupBox("Development Environment")
        selector_layout = QHBoxLayout()
        selector_group.setLayout(selector_layout)
        
        # Project selector
        selector_layout.addWidget(QLabel("Project:"))
        self.project_combo = QComboBox()
        self.project_combo.addItem("System Default", None)
        self.project_combo.currentIndexChanged.connect(self.on_project_changed)
        selector_layout.addWidget(self.project_combo, 1)
        
        # Refresh projects button
        refresh_btn = QPushButton()
        refresh_btn.setIcon(create_refresh_icon(24))
        refresh_btn.setMaximumWidth(40)
        refresh_btn.setToolTip("Refresh project list")
        refresh_btn.clicked.connect(self.refresh_projects)
        selector_layout.addWidget(refresh_btn)
        
        # Clear terminal button
        clear_btn = QPushButton("Clear")
        clear_btn.setMaximumWidth(80)
        clear_btn.clicked.connect(self.clear_terminal)
        selector_layout.addWidget(clear_btn)
        
        layout.addWidget(selector_group)
        
        # Environment info
        self.env_info_label = QLabel("Environment: System Default")
        self.env_info_label.setStyleSheet("color: #666; font-size: 9pt; padding: 5px;")
        layout.addWidget(self.env_info_label)
        
        # Terminal output
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Monospace", 10))
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.output_text, 1)
        
        # Command input area
        input_layout = QHBoxLayout()
        
        # Prompt label
        self.prompt_label = QLabel("$")
        self.prompt_label.setFont(QFont("Monospace", 10, QFont.Bold))
        self.prompt_label.setStyleSheet("color: #4EC9B0;")
        input_layout.addWidget(self.prompt_label)
        
        # Command input
        self.command_input = QLineEdit()
        self.command_input.setFont(QFont("Monospace", 10))
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d30;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 1px solid #007ACC;
            }
        """)
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.installEventFilter(self)
        input_layout.addWidget(self.command_input, 1)
        
        # Execute button
        exec_btn = QPushButton("Execute")
        exec_btn.setProperty("class", "success")
        exec_btn.clicked.connect(self.execute_command)
        input_layout.addWidget(exec_btn)
        
        layout.addLayout(input_layout)
        
        # Quick commands group
        quick_group = QGroupBox("Quick Commands")
        quick_layout = QHBoxLayout()
        quick_group.setLayout(quick_layout)
        
        commands = [
            ("pwd", "Print working directory"),
            ("ls -la", "List files"),
            ("npm install", "Install npm packages"),
            ("composer install", "Install composer packages"),
            ("php -v", "PHP version"),
            ("node -v", "Node version"),
        ]
        
        for cmd, tooltip in commands:
            btn = QPushButton(cmd)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, c=cmd: self.quick_command(c))
            quick_layout.addWidget(btn)
        
        layout.addWidget(quick_group)
        
        # Load projects
        self.refresh_projects()
        
        # Welcome message
        self.append_output("=== LinuxDev Manager Terminal ===", "#4EC9B0")
        self.append_output("Type commands to execute in the development environment.\n", "#888")
    
    def eventFilter(self, obj, event):
        """Handle key events for command history."""
        if obj == self.command_input and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Up:
                self.navigate_history(-1)
                return True
            elif event.key() == Qt.Key_Down:
                self.navigate_history(1)
                return True
        return super().eventFilter(obj, event)
    
    def navigate_history(self, direction):
        """Navigate through command history."""
        if not self.command_history:
            return
        
        self.history_index += direction
        
        if self.history_index < 0:
            self.history_index = 0
        elif self.history_index >= len(self.command_history):
            self.history_index = len(self.command_history)
            self.command_input.clear()
            return
        
        if self.history_index < len(self.command_history):
            self.command_input.setText(self.command_history[self.history_index])
    
    def refresh_projects(self):
        """Refresh project list."""
        self.project_combo.clear()
        self.project_combo.addItem("System Default", None)
        
        projects = self.project_manager.get_projects()
        for project in projects:
            self.project_combo.addItem(
                f"{project['name']} ({project['type']})",
                project
            )
    
    def on_project_changed(self, index):
        """Handle project selection change."""
        self.current_project = self.project_combo.itemData(index)
        
        if self.current_project:
            project_path = self.current_project['path']
            project_name = self.current_project['name']
            project_type = self.current_project['type']
            
            self.env_info_label.setText(
                f"Environment: {project_name} | Type: {project_type} | Path: {project_path}"
            )
            self.append_output(f"\n--- Switched to project: {project_name} ---", "#4EC9B0")
            self.append_output(f"Working directory: {project_path}", "#888")
            
            # Update prompt
            self.prompt_label.setText(f"{project_name} $")
        else:
            home_dir = os.path.expanduser("~")
            self.env_info_label.setText(f"Environment: System Default | Path: {home_dir}")
            self.append_output("\n--- Switched to system default ---", "#4EC9B0")
            self.prompt_label.setText("$")
    
    def clear_terminal(self):
        """Clear terminal output."""
        self.output_text.clear()
        self.append_output("=== Terminal Cleared ===\n", "#888")
    
    def quick_command(self, command):
        """Execute a quick command."""
        self.command_input.setText(command)
        self.execute_command()
    
    def execute_command(self):
        """Execute the command in the input field."""
        command = self.command_input.text().strip()
        
        if not command:
            return
        
        # Add to history
        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Get working directory
        if self.current_project:
            working_dir = self.current_project['path']
        else:
            working_dir = os.path.expanduser("~")
        
        # Display command
        prompt = self.prompt_label.text()
        self.append_output(f"\n{prompt} {command}", "#569CD6")
        
        # Clear input
        self.command_input.clear()
        
        # Setup process
        self.process = QProcess(self)
        self.process.setWorkingDirectory(working_dir)
        
        # Set environment
        env = self.process.processEnvironment()
        
        # Add project-specific environment variables
        if self.current_project:
            project_type = self.current_project['type']
            project_path = self.current_project['path']
            
            # Add common paths
            env.insert("PROJECT_ROOT", project_path)
            env.insert("PROJECT_NAME", self.current_project['name'])
            env.insert("PROJECT_TYPE", project_type)
            
            # Add node_modules/.bin to PATH if it exists
            node_bin = os.path.join(project_path, "node_modules", ".bin")
            if os.path.exists(node_bin):
                current_path = env.value("PATH", "")
                env.insert("PATH", f"{node_bin}:{current_path}")
            
            # Add vendor/bin to PATH if it exists (for PHP/Composer projects)
            vendor_bin = os.path.join(project_path, "vendor", "bin")
            if os.path.exists(vendor_bin):
                current_path = env.value("PATH", "")
                env.insert("PATH", f"{vendor_bin}:{current_path}")
        
        self.process.setProcessEnvironment(env)
        
        # Connect signals
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.handle_finished)
        
        # Start process with shell
        self.process.start("bash", ["-c", command])
        
        if not self.process.waitForStarted():
            self.append_output("Error: Failed to start process", "#f44336")
    
    def handle_stdout(self):
        """Handle standard output."""
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode('utf-8', errors='replace')
        self.append_output(text, "#d4d4d4")
    
    def handle_stderr(self):
        """Handle standard error."""
        data = self.process.readAllStandardError()
        text = bytes(data).decode('utf-8', errors='replace')
        self.append_output(text, "#f48771")
    
    def handle_finished(self, exit_code, exit_status):
        """Handle process finished."""
        if exit_code == 0:
            self.append_output(f"\n[Process completed with exit code {exit_code}]", "#4EC9B0")
        else:
            self.append_output(f"\n[Process exited with code {exit_code}]", "#f44336")
        
        self.command_executed.emit(self.command_input.text(), exit_code)
        self.process = None
    
    def append_output(self, text, color=None):
        """Append text to output with optional color."""
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if color:
            self.output_text.setTextColor(QColor(color))
        else:
            self.output_text.setTextColor(QColor("#d4d4d4"))
        
        cursor.insertText(text)
        self.output_text.setTextCursor(cursor)
        self.output_text.ensureCursorVisible()
