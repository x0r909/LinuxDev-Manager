"""Qt stylesheet definitions for the application."""


def get_light_theme() -> str:
    """Get light theme stylesheet."""
    return """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    font-family: 'Ubuntu', 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #212121;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QPushButton.success {
    background-color: #4CAF50;
}

QPushButton.success:hover {
    background-color: #388E3C;
}

QPushButton.success:pressed {
    background-color: #2E7D32;
}

QPushButton.danger {
    background-color: #F44336;
}

QPushButton.danger:hover {
    background-color: #D32F2F;
}

QPushButton.danger:pressed {
    background-color: #C62828;
}

QPushButton.warning {
    background-color: #FF9800;
}

QPushButton.warning:hover {
    background-color: #F57C00;
}

QPushButton.package-action {
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    min-height: 28px;
}

QPushButton#theme-toggle {
    background-color: transparent;
    border: 1px solid #E0E0E0;
    color: #424242;
    padding: 6px 12px;
    font-size: 16pt;
}

QPushButton#theme-toggle:hover {
    background-color: #F5F5F5;
    border-color: #BDBDBD;
}

QGroupBox {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 8px;
    color: #424242;
}

QLabel {
    color: #424242;
}

QLabel.title {
    font-size: 18pt;
    font-weight: bold;
    color: #212121;
}

QLabel.subtitle {
    font-size: 12pt;
    color: #757575;
}

QLabel.status-running {
    color: #4CAF50;
    font-weight: bold;
}

QLabel.status-stopped {
    color: #F44336;
    font-weight: bold;
}

QLabel.status-not-installed {
    color: #9E9E9E;
}

QLineEdit, QTextEdit, QComboBox {
    background-color: white;
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    padding: 6px;
    color: #212121;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #757575;
    margin-right: 6px;
}

QTableWidget {
    background-color: white;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    gridline-color: #E0E0E0;
}

QTableWidget::item {
    padding: 4px;
    color: #212121;
}

QTableWidget::item:selected {
    background-color: #E3F2FD;
    color: #212121;
}

QHeaderView::section {
    background-color: #FAFAFA;
    color: #424242;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #E0E0E0;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #F5F5F5;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #BDBDBD;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #9E9E9E;
}

QScrollBar:horizontal {
    background-color: #F5F5F5;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #BDBDBD;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #9E9E9E;
}

QTabWidget::pane {
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    background-color: white;
}

QTabBar::tab {
    background-color: #FAFAFA;
    color: #757575;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: white;
    color: #2196F3;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #F5F5F5;
}

QProgressBar {
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    text-align: center;
    background-color: #F5F5F5;
    color: #212121;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}

QCheckBox {
    spacing: 8px;
    color: #424242;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #BDBDBD;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #2196F3;
    border-color: #2196F3;
}

QCheckBox::indicator:hover {
    border-color: #2196F3;
}

QMessageBox {
    background-color: white;
}

QToolTip {
    background-color: #424242;
    color: white;
    border: none;
    padding: 4px;
    border-radius: 2px;
}
"""


def get_dark_theme() -> str:
    """Get dark theme stylesheet."""
    return """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    font-family: 'Ubuntu', 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
    color: #e0e0e0;
}

QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #42A5F5;
}

QPushButton:pressed {
    background-color: #1976D2;
}

QPushButton:disabled {
    background-color: #424242;
    color: #757575;
}

QPushButton.success {
    background-color: #4CAF50;
}

QPushButton.success:hover {
    background-color: #66BB6A;
}

QPushButton.success:pressed {
    background-color: #388E3C;
}

QPushButton.danger {
    background-color: #F44336;
}

QPushButton.danger:hover {
    background-color: #EF5350;
}

QPushButton.danger:pressed {
    background-color: #D32F2F;
}

QPushButton.warning {
    background-color: #FF9800;
}

QPushButton.warning:hover {
    background-color: #FFA726;
}

QPushButton.package-action {
    padding: 6px 12px;
    border-radius: 4px;
    font-weight: 600;
    min-height: 28px;
}

QPushButton#theme-toggle {
    background-color: transparent;
    border: 1px solid #404040;
    color: #e0e0e0;
    padding: 6px 12px;
    font-size: 16pt;
}

QPushButton#theme-toggle:hover {
    background-color: #2d2d2d;
    border-color: #505050;
}

QGroupBox {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
    color: #e0e0e0;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 8px;
    color: #e0e0e0;
}

QLabel {
    color: #e0e0e0;
}

QLabel.title {
    font-size: 18pt;
    font-weight: bold;
    color: #ffffff;
}

QLabel.subtitle {
    font-size: 12pt;
    color: #b0b0b0;
}

QLabel.status-running {
    color: #66BB6A;
    font-weight: bold;
}

QLabel.status-stopped {
    color: #EF5350;
    font-weight: bold;
}

QLabel.status-not-installed {
    color: #757575;
}

QLineEdit, QTextEdit, QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #505050;
    border-radius: 4px;
    padding: 6px;
    color: #e0e0e0;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #b0b0b0;
    margin-right: 6px;
}

QTableWidget {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 4px;
    gridline-color: #404040;
}

QTableWidget::item {
    padding: 4px;
    color: #e0e0e0;
}

QTableWidget::item:selected {
    background-color: #1565C0;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #252525;
    color: #e0e0e0;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #404040;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #505050;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #606060;
}

QScrollBar:horizontal {
    background-color: #2d2d2d;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #505050;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #606060;
}

QTabWidget::pane {
    border: 1px solid #404040;
    border-radius: 4px;
    background-color: #2d2d2d;
}

QTabBar::tab {
    background-color: #252525;
    color: #b0b0b0;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #2d2d2d;
    color: #2196F3;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #353535;
}

QProgressBar {
    border: 1px solid #404040;
    border-radius: 4px;
    text-align: center;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}

QCheckBox {
    spacing: 8px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #505050;
    border-radius: 3px;
    background-color: #2d2d2d;
}

QCheckBox::indicator:checked {
    background-color: #2196F3;
    border-color: #2196F3;
}

QCheckBox::indicator:hover {
    border-color: #2196F3;
}

QMessageBox {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QToolTip {
    background-color: #424242;
    color: white;
    border: none;
    padding: 4px;
    border-radius: 2px;
}
"""


# Keep MAIN_STYLE for backward compatibility (defaults to light theme)
MAIN_STYLE = get_light_theme()


def get_status_color(status: str) -> str:
    """
    Get color for service status.
    
    Args:
        status: Status string
        
    Returns:
        Color hex code
    """
    colors = {
        'running': '#4CAF50',
        'stopped': '#F44336',
        'not_installed': '#9E9E9E',
        'error': '#FF5722'
    }
    return colors.get(status, '#9E9E9E')


def get_status_icon(status: str) -> str:
    """
    Get icon for service status.
    
    Args:
        status: Status string
        
    Returns:
        Icon character
    """
    icons = {
        'running': '●',
        'stopped': '○',
        'not_installed': '◌',
        'error': '⚠'
    }
    return icons.get(status, '◌')
