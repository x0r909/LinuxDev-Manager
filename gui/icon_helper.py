"""Helper functions for creating icons from text/emoji."""
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QColor
from PyQt5.QtCore import Qt, QSize, QPointF
from PyQt5.QtGui import QPolygonF
import os


def get_asset_icon(filename):
    """Get icon from assets folder."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, 'assets', filename)
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()


def create_text_icon(text, size=32, bg_color=None, fg_color=None):
    """Create an icon from text/emoji.
    
    Args:
        text: The text or emoji to render
        size: Icon size in pixels
        bg_color: Background color (QColor or None for transparent)
        fg_color: Foreground color (QColor or None for default)
    
    Returns:
        QIcon with the rendered text
    """
    # Create pixmap
    pixmap = QPixmap(size, size)
    
    # Fill background
    if bg_color:
        pixmap.fill(bg_color)
    else:
        pixmap.fill(Qt.transparent)
    
    # Create painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)
    
    # Set font
    font = QFont()
    font.setPixelSize(int(size * 0.6))  # 60% of icon size
    painter.setFont(font)
    
    # Set color
    if fg_color:
        painter.setPen(fg_color)
    else:
        painter.setPen(QColor(255, 255, 255))
    
    # Draw text centered
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    painter.end()
    
    return QIcon(pixmap)


def create_download_icon(size=24, color=None):
    """Create a download/install icon."""
    if color is None:
        color = QColor(255, 255, 255)  # White for visibility on green button
    
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    
    # Arrow shaft
    shaft_width = size // 5
    shaft_height = size // 2
    shaft_x = (size - shaft_width) // 2
    shaft_y = size // 6
    painter.drawRect(shaft_x, shaft_y, shaft_width, shaft_height)
    
    # Arrow head
    arrow_size = size // 3
    arrow_y = shaft_y + shaft_height - size // 10
    
    points = QPolygonF([
        QPointF(size // 2, arrow_y + arrow_size),
        QPointF(size // 2 - arrow_size, arrow_y),
        QPointF(size // 2 + arrow_size, arrow_y)
    ])
    painter.drawPolygon(points)
    
    # Base line
    pen = painter.pen()
    pen.setWidth(max(2, size // 12))
    pen.setColor(color)
    painter.setPen(pen)
    
    base_y = size - size // 6
    painter.drawLine(size // 6, base_y, size - size // 6, base_y)
    
    painter.end()
    
    return QIcon(pixmap)


def create_trash_icon(size=24, color=None):
    """Create a trash/delete icon."""
    if color is None:
        color = QColor(255, 255, 255)  # White for visibility on red button
    
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Set pen
    pen = painter.pen()
    pen.setWidth(max(2, size // 12))
    pen.setColor(color)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    
    # Lid
    lid_y = size // 4
    painter.drawLine(size // 6, lid_y, size - size // 6, lid_y)
    
    # Handle
    handle_width = size // 3
    handle_x = (size - handle_width) // 2
    painter.drawLine(handle_x, lid_y - size // 8, handle_x + handle_width, lid_y - size // 8)
    
    # Can body
    can_top = lid_y + size // 12
    can_bottom = size - size // 6
    can_left = size // 4
    can_right = size - size // 4
    
    painter.drawLine(can_left, can_top, can_left, can_bottom)
    painter.drawLine(can_right, can_top, can_right, can_bottom)
    painter.drawLine(can_left, can_bottom, can_right, can_bottom)
    
    # Vertical lines inside can
    mid_x = size // 2
    painter.drawLine(mid_x, can_top + size // 8, mid_x, can_bottom - size // 8)
    
    painter.end()
    
    return QIcon(pixmap)


def create_refresh_icon(size=32, color=None):
    """Create a refresh/reload icon."""
    if color is None:
        color = QColor(33, 150, 243)  # Blue
    
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw circular arrow
    pen = painter.pen()
    pen.setWidth(max(2, size // 16))
    pen.setColor(color)
    painter.setPen(pen)
    
    # Draw arc
    margin = size // 6
    rect = pixmap.rect().adjusted(margin, margin, -margin, -margin)
    painter.drawArc(rect, 30 * 16, 300 * 16)
    
    # Draw arrow head
    import math
    angle = math.radians(30)
    center_x = size // 2
    center_y = size // 2
    radius = (size - margin * 2) // 2
    
    arrow_x = center_x + radius * math.cos(angle)
    arrow_y = center_y - radius * math.sin(angle)
    
    # Simple arrow triangle
    painter.setBrush(color)
    from PyQt5.QtCore import QPointF
    from PyQt5.QtGui import QPolygonF
    
    arrow_size = size // 8
    points = QPolygonF([
        QPointF(arrow_x, arrow_y),
        QPointF(arrow_x - arrow_size, arrow_y - arrow_size // 2),
        QPointF(arrow_x - arrow_size, arrow_y + arrow_size // 2)
    ])
    painter.drawPolygon(points)
    
    painter.end()
    
    return QIcon(pixmap)


def create_theme_icon(theme='light', size=32):
    """Create theme toggle icon (sun/moon)."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    center = size // 2
    
    if theme == 'dark':
        # Draw sun icon
        color = QColor(255, 193, 7)  # Amber
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        
        # Sun circle
        radius = size // 4
        painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)
        
        # Sun rays
        pen = painter.pen()
        pen.setWidth(max(2, size // 16))
        pen.setColor(color)
        painter.setPen(pen)
        
        import math
        ray_length = size // 6
        outer_radius = radius + ray_length // 2
        
        for i in range(8):
            angle = math.radians(i * 45)
            x1 = center + (radius + 2) * math.cos(angle)
            y1 = center + (radius + 2) * math.sin(angle)
            x2 = center + outer_radius * math.cos(angle)
            y2 = center + outer_radius * math.sin(angle)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    else:
        # Draw moon icon
        color = QColor(158, 158, 158)  # Gray
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        
        # Moon circle
        radius = size // 3
        painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)
        
        # Cut out crescent
        painter.setCompositionMode(QPainter.CompositionMode_DestinationOut)
        offset = radius // 2
        painter.drawEllipse(
            center - radius + offset,
            center - radius - offset // 2,
            radius * 2,
            radius * 2
        )
    
    painter.end()
    
    return QIcon(pixmap)
