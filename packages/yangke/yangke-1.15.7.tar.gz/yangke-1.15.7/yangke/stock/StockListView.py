import os

from yangke.common.QtImporter import Qt, QModelIndex, QSize, QRect, QFont, QPen, QColor, QFileDialog, QComboBox, \
    QStyleOptionViewItem, QStyle, QPainter, QPointF, QRectF, QPainterPath, QStyledItemDelegate


class StockItemDelegate(QStyledItemDelegate):
    def __init__(self):
        """
        【所有组件】面板中所有组件的显示方式
        """
        super().__init__()
        self.width = 220
        self.height = 25

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if index.isValid():
            painter.save()

            color_primary = QColor(os.getenv('QTMATERIAL_PRIMARYCOLOR'))
            color_light_primary = QColor(os.getenv('QTMATERIAL_PRIMARYLIGHTCOLOR'))
            color_secondary = QColor(os.getenv('QTMATERIAL_SECONDARYCOLOR'))
            color_light_secondary = QColor(os.getenv('QTMATERIAL_SECONDARYLIGHTCOLOR'))
            color_dark_secondary = QColor(os.getenv('QTMATERIAL_SECONDARYDARKCOLOR'))
            color_primary_text = QColor(os.getenv('QTMATERIAL_PRIMARYTEXTCOLOR'))
            color_secondary_text = QColor(os.getenv('QTMATERIAL_SECONDARYTEXTCOLOR'))

            user_data = index.data(Qt.UserRole)
            symbol = user_data.get("name")  # 组件在Ebsilon中的id
            name = user_data.get("名称")
            rect = QRectF()
            rect.setX(option.rect.x())
            rect.setY(option.rect.y())
            rect.setWidth(self.width - 1)
            rect.setHeight(self.height - 1)

            # 绘制圆角矩形
            radius = 7
            path: QPainterPath = QPainterPath()
            path.moveTo(rect.topRight() - QPointF(radius, 0))
            path.lineTo(rect.topLeft() + QPointF(radius, 0))
            path.quadTo(rect.topLeft(), rect.topLeft() + QPointF(0, radius))
            path.lineTo(rect.bottomLeft() + QPointF(0, -radius))
            path.quadTo(rect.bottomLeft(), rect.bottomLeft() + QPointF(radius, 0))
            path.lineTo(rect.bottomRight() - QPointF(radius, 0))
            path.quadTo(rect.bottomRight(), rect.bottomRight() + QPointF(0, -radius))
            path.lineTo(rect.topRight() + QPointF(0, radius))  # 8
            path.quadTo(rect.topRight(), rect.topRight() + QPointF(-radius, -0))

            # 绘制数据位置
            symbol_rect = QRect(int(rect.left() + 5), int(rect.top() + 5), int(rect.width() - 30), 20)  # 中文组件名所在的区域
            name_rect = QRect(int(rect.right() - 100), int(rect.top() + 5), int(rect.width() - 100), 20)  # EBS_ID

            if option.state & QStyle.State_Selected:
                painter.setPen(QPen(color_secondary))
                painter.setBrush(color_primary)
                painter.drawPath(path)
            elif option.state & QStyle.State_MouseOver:
                painter.setPen(color_primary)
                painter.setBrush(color_light_secondary)
                painter.drawPath(path)
            else:
                painter.setPen(QPen(color_light_primary))
                painter.setBrush(Qt.NoBrush)
                painter.drawPath(path)

            # 绘制组件名
            # painter.drawEllipse(circle)
            painter.setPen(QPen(color_secondary_text))
            painter.setFont(QFont("Times", 10, QFont.Bold))
            painter.drawText(symbol_rect, Qt.AlignLeft, symbol)  # 绘制中文组件名

            # 绘制右侧的EBS_ID
            painter.setPen(QPen(color_secondary_text))
            painter.setFont(QFont("Times", 10))
            painter.drawText(name_rect, Qt.AlignLeft, name)

            painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(self.width, self.height)
