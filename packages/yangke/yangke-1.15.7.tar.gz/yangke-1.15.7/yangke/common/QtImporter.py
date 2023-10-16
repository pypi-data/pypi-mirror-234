"""
该类同时兼容PyQt6、PySide6和PyQt5，且优先使用顺序是PyQt6 -> PySide6 -> PyQt5。

本模块使得可以在Qt6环境上运行以前以Qt5语法编写的程序。
本模块在Qt5运行环境中，并不做Qt6语法的兼容，因此，如果程序是以Qt6语法写的，请直接安装Qt6的库，如PySide6或PyQt6。

从该模块引入Qt组件时，优先尝试直接引入最终的类名.
如果Qt中有多个同名的类，则尝试引入类所在的模块，然后以[模块.类型]的方式引入特定的类
"""
import traceback
from enum import Enum
from yangke.common.config import logger

try:
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtCore import (QDir, QStringListModel, Qt, QModelIndex, QSize, QRectF, QRect, QLineF, QLine,
                              QPointF, QPoint, QMimeData, QFileInfo,
                              pyqtSignal, pyqtSlot, QCoreApplication, QDate, QDateTime, QTime, QLocale, QUrl, QFile,
                              QMetaObject, QObject, QTimer, QThread)
    from PyQt6.QtGui import (QStandardItemModel, QStandardItem, QIcon, QPainter, QPainterPath, QPen, QColor, QFont,
                             QImage, QBrush, QTransform, QIntValidator, QKeyEvent, QResizeEvent, QAction, QDrag,
                             QFileSystemModel, QDesktopServices, QScreen, QSurface, QShortcut, QPixmap,
                             QKeySequence)
    from PyQt6.QtWidgets import (QTreeView, QMessageBox, QStyledItemDelegate,
                                 QStyleOptionViewItem,
                                 QListView, QStyle, QWidget, QFrame,
                                 QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                                 QGraphicsItem, QGraphicsSceneMouseEvent,
                                 QHeaderView, QProgressBar, QButtonGroup,
                                 QSizePolicy, QRadioButton, QDialogButtonBox,
                                 QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent,
                                 QGraphicsSceneContextMenuEvent, QMenu, QApplication, QGraphicsLineItem,
                                 QMainWindow,
                                 QHBoxLayout, QGridLayout, QVBoxLayout, QPushButton, QFormLayout, QLayout,
                                 QLineEdit, QTextEdit, QComboBox, QTableWidgetItem, QLabel, QCheckBox, QTableWidget,
                                 QDialog, QInputDialog, QDockWidget, QDoubleSpinBox, QDial, QDateEdit,
                                 QSplitter, QStatusBar, QTabWidget, QScrollArea, QFileDialog,
                                 QListWidget, QListWidgetItem, QColorDialog, QToolBar,
                                 QAbstractItemView, QTableWidgetSelectionRange,
                                 QGraphicsSceneDragDropEvent, QGraphicsTextItem,
                                 )

    try:
        from PyQt6.QtWebEngineWidgets import QWebEngineView  # pip install PyQt6-WebEngine
    except:
        pass

    import PyQt6.QtCore as QtCore
    from PyQt6.QtCore import Qt
    from PyQt6 import uic

    try:
        # 只有单独安装了pip install PyQt6-QScintilla之后，PyQt6包下才有Qsci包
        from PyQt6 import Qsci
        from PyQt6.Qsci import QsciScintilla, QsciDocument, QsciLexer, QsciLexerPython, QsciAPIs

        QsciScintilla.WrapCharacter = QsciScintilla.WrapMode.WrapCharacter
        QsciScintilla.WrapFlagByText = QsciScintilla.WrapVisualFlag.WrapFlagByText
        QsciScintilla.AcsAll = QsciScintilla.AutoCompletionSource.AcsAll
        QsciScintilla.AcusExplicit = QsciScintilla.AutoCompletionUseSingle.AcusExplicit
        QsciScintilla.NumberMargin = QsciScintilla.MarginType.NumberMargin
    except:
        pass
    QDesktopWidget = QScreen  # Qt6中移除了QDesktopWidget，官方建议使用QScreen代替，但二者的区别并未处理

    # Qt6中组件对其方式常量所在的位置发生改变
    Horizontal = Qt.Horizontal = Qt.Orientation.Horizontal
    Vertical = Qt.Vertical = Qt.Orientation.Vertical

    DisplayRole = Qt.DisplayRole = Qt.ItemDataRole.DisplayRole
    DecorationRole = Qt.DecorationRole = Qt.ItemDataRole.DecorationRole
    EditRole = Qt.EditRole = Qt.ItemDataRole.EditRole
    ToolTipRole = Qt.ToolTipRole = Qt.ItemDataRole.ToolTipRole
    StatusTipRole = Qt.StatusTipRole = Qt.ItemDataRole.StatusTipRole
    WhatsThisRole = Qt.WhatsThisRole = Qt.ItemDataRole.WhatsThisRole
    FontRole = Qt.FontRole = Qt.ItemDataRole.FontRole
    TextAlignmentRole = Qt.TextAlignmentRole = Qt.ItemDataRole.TextAlignmentRole
    BackgroundRole = Qt.BackgroundRole = Qt.ItemDataRole.BackgroundRole
    ForegroundRole = Qt.ForegroundRole = Qt.ItemDataRole.ForegroundRole
    CheckStateRole = Qt.CheckStateRole = Qt.ItemDataRole.CheckStateRole
    AccessibleTextRole = Qt.AccessibleTextRole = Qt.ItemDataRole.AccessibleTextRole
    AccessibleDescriptionRole = Qt.AccessibleDescriptionRole = Qt.ItemDataRole.AccessibleDescriptionRole
    SizeHintRole = Qt.SizeHintRole = Qt.ItemDataRole.SizeHintRole
    InitialSortOrderRole = Qt.InitialSortOrderRole = Qt.ItemDataRole.InitialSortOrderRole
    UserRole = Qt.UserRole = Qt.ItemDataRole.UserRole

    # Qt6中组件尺寸自适应方式常量所在的位置发生改变
    QSizePolicy.Fixed = Fixed = QSizePolicy.Policy.Fixed
    QSizePolicy.Minimum = Minimum = QSizePolicy.Policy.Minimum
    QSizePolicy.Maximum = Maximum = QSizePolicy.Policy.Maximum
    QSizePolicy.Preferred = Preferred = QSizePolicy.Policy.Preferred
    QSizePolicy.MinimumExpanding = MinimumExpanding = QSizePolicy.Policy.MinimumExpanding
    QSizePolicy.Expanding = Expanding = QSizePolicy.Policy.Expanding
    QSizePolicy.Ignored = Ignored = QSizePolicy.Policy.Ignored

    # Qt6中组件尺寸自适应方式常量所在的位置发生改变
    DockWidgetClosable = QDockWidget.DockWidgetClosable = QDockWidget.DockWidgetFeature.DockWidgetClosable
    DockWidgetFloatable = QDockWidget.DockWidgetFloatable = QDockWidget.DockWidgetFeature.DockWidgetFloatable
    DockWidgetMovable = QDockWidget.DockWidgetMovable = QDockWidget.DockWidgetFeature.DockWidgetMovable
    NoDockWidgetFeatures = QDockWidget.NoDockWidgetFeatures = QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
    DockWidgetVerticalTitleBar = QDockWidget.DockWidgetVerticalTitleBar = QDockWidget.DockWidgetFeature.DockWidgetVerticalTitleBar

    # Qt6中QTabWidget的属性位置发生变化
    QTabWidget.North = QTabWidget.TabPosition.North
    QTabWidget.South = QTabWidget.TabPosition.South
    QTabWidget.West = QTabWidget.TabPosition.West
    QTabWidget.East = QTabWidget.TabPosition.East
    QTabWidget.Triangular = QTabWidget.TabShape.Triangular
    QTabWidget.Rounded = QTabWidget.TabShape.Rounded

    QAbstractItemView.NoEditTriggers = QAbstractItemView.EditTrigger.NoEditTriggers
    QAbstractItemView.AllEditTriggers = QAbstractItemView.EditTrigger.AllEditTriggers
    QAbstractItemView.AnyKeyPressed = QAbstractItemView.EditTrigger.AnyKeyPressed
    QAbstractItemView.EditKeyPressed = QAbstractItemView.EditTrigger.EditKeyPressed
    QAbstractItemView.DoubleClicked = QAbstractItemView.EditTrigger.DoubleClicked
    QAbstractItemView.SelectedClicked = QAbstractItemView.EditTrigger.SelectedClicked

    Qt.ApplicationModal = Qt.WindowModality.ApplicationModal
    Qt.WindowModal = Qt.WindowModality.WindowModal
    Qt.NonModal = Qt.WindowModality.NonModal

    FieldRole = QFormLayout.FieldRole = QFormLayout.ItemRole.FieldRole
    LabelRole = QFormLayout.LabelRole = QFormLayout.ItemRole.LabelRole
    SpanningRole = QFormLayout.SpanningRole = QFormLayout.ItemRole.SpanningRole

    SetDefaultConstraint = QLayout.SetDefaultConstraint = QLayout.SizeConstraint.SetDefaultConstraint
    SetNoConstraint = QLayout.SetNoConstraint = QLayout.SizeConstraint.SetNoConstraint
    SetMinimumSize = QLayout.SetMinimumSize = QLayout.SizeConstraint.SetMinimumSize
    SetFixedSize = QLayout.SetFixedSize = QLayout.SizeConstraint.SetFixedSize
    SetMaximumSize = QLayout.SetMaximumSize = QLayout.SizeConstraint.SetMaximumSize
    SetMinAndMaxSize = QLayout.SetMinAndMaxSize = QLayout.SizeConstraint.SetMinAndMaxSize

    ItemIsMovable = QGraphicsItem.ItemIsMovable = QGraphicsItem.GraphicsItemFlag.ItemIsMovable
    ItemIsSelectable = QGraphicsItem.ItemIsSelectable = QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
    ItemIsFocusable = QGraphicsItem.ItemIsFocusable = QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
    ItemClipsToShape = QGraphicsItem.ItemClipsToShape = QGraphicsItem.GraphicsItemFlag.ItemClipsToShape
    ItemClipsChildrenToShape = QGraphicsItem.ItemClipsChildrenToShape = QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape
    ItemIgnoresTransformations = QGraphicsItem.ItemIgnoresTransformations = QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations
    ItemIgnoresParentOpacity = QGraphicsItem.ItemIgnoresParentOpacity = QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity
    ItemDoesntPropagateOpacityToChildren = QGraphicsItem.ItemDoesntPropagateOpacityToChildren = QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren
    ItemStacksBehindParent = QGraphicsItem.ItemStacksBehindParent = QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent
    ItemUsesExtendedStyleOption = QGraphicsItem.ItemUsesExtendedStyleOption = QGraphicsItem.GraphicsItemFlag.ItemUsesExtendedStyleOption
    ItemHasNoContents = QGraphicsItem.ItemHasNoContents = QGraphicsItem.GraphicsItemFlag.ItemHasNoContents
    ItemSendsGeometryChanges = QGraphicsItem.ItemSendsGeometryChanges = QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
    ItemAcceptsInputMethod = QGraphicsItem.ItemAcceptsInputMethod = QGraphicsItem.GraphicsItemFlag.ItemAcceptsInputMethod
    ItemNegativeZStacksBehindParent = QGraphicsItem.ItemNegativeZStacksBehindParent = QGraphicsItem.GraphicsItemFlag.ItemNegativeZStacksBehindParent
    ItemIsPanel = QGraphicsItem.ItemIsPanel = QGraphicsItem.GraphicsItemFlag.ItemIsPanel
    ItemSendsScenePositionChanges = QGraphicsItem.ItemSendsScenePositionChanges = QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
    ItemContainsChildrenInShape = QGraphicsItem.ItemContainsChildrenInShape = QGraphicsItem.GraphicsItemFlag.ItemContainsChildrenInShape

    # Qt6中的颜色常量位置发生变化，PySide6语法和PyQt5一样
    Qt.color0 = color0 = Qt.GlobalColor.color0
    Qt.color1 = color1 = Qt.GlobalColor.color1
    Qt.black = black = QColor("#000000")
    Qt.white = white = QColor("#FFFFFF")
    Qt.darkGray = darkGray = Qt.GlobalColor.darkGray
    Qt.gray = gray = Qt.GlobalColor.gray
    Qt.lightGray = lightGray = Qt.GlobalColor.lightGray
    Qt.red = red = QColor("#FF0000")
    Qt.green = green = QColor("#00FF00")
    Qt.blue = blue = QColor("#0000FF")
    Qt.cyan = cyan = Qt.GlobalColor.cyan
    Qt.magenta = magenta = Qt.GlobalColor.magenta
    Qt.yellow = yellow = QColor("#FFFF00")
    Qt.darkRed = darkRed = Qt.GlobalColor.darkRed
    Qt.darkGreen = darkGreen = Qt.GlobalColor.darkGreen
    Qt.darkBlue = darkBlue = Qt.GlobalColor.darkBlue
    Qt.darkCyan = darkCyan = Qt.GlobalColor.darkCyan
    Qt.darkMagenta = darkMagenta = Qt.GlobalColor.darkMagenta
    Qt.darkYellow = darkYellow = Qt.GlobalColor.darkYellow
    Qt.transparent = transparent = Qt.GlobalColor.transparent

    ListMode = QListView.ListMode = QListView.ViewMode.ListMode
    IconMode = QListView.IconMode = QListView.ViewMode.IconMode

    Antialiasing = QPainter.Antialiasing = QPainter.RenderHint.Antialiasing
    TextAntialiasing = QPainter.TextAntialiasing = QPainter.RenderHint.TextAntialiasing
    SmoothPixmapTransform = QPainter.SmoothPixmapTransform = QPainter.RenderHint.SmoothPixmapTransform
    LosslessImageRendering = QPainter.LosslessImageRendering = QPainter.RenderHint.LosslessImageRendering
    VerticalSubpixelPositioning = QPainter.VerticalSubpixelPositioning = QPainter.RenderHint.VerticalSubpixelPositioning
    NonCosmeticBrushPatterns = QPainter.NonCosmeticBrushPatterns = QPainter.RenderHint.NonCosmeticBrushPatterns

    # PySide6语法和PyQt5一样
    AlignLeft = Qt.AlignLeft = Qt.AlignmentFlag.AlignLeft
    AlignLeading = Qt.AlignLeading = Qt.AlignmentFlag.AlignLeading
    AlignRight = Qt.AlignRight = Qt.AlignmentFlag.AlignRight
    AlignTrailing = Qt.AlignTrailing = Qt.AlignmentFlag.AlignTrailing
    AlignHCenter = Qt.AlignHCenter = Qt.AlignmentFlag.AlignHCenter
    AlignJustify = Qt.AlignJustify = Qt.AlignmentFlag.AlignJustify
    AlignAbsolute = Qt.AlignAbsolute = Qt.AlignmentFlag.AlignAbsolute
    AlignHorizontal_Mask = Qt.AlignHorizontal_Mask = Qt.AlignmentFlag.AlignHorizontal_Mask
    AlignTop = Qt.AlignTop = Qt.AlignmentFlag.AlignTop
    AlignBottom = Qt.AlignBottom = Qt.AlignmentFlag.AlignBottom
    AlignVCenter = Qt.AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    AlignVertical_Mask = Qt.AlignVertical_Mask = Qt.AlignmentFlag.AlignVertical_Mask
    AlignCenter = Qt.AlignCenter = Qt.AlignmentFlag.AlignCenter
    AlignBaseline = Qt.AlignBaseline = Qt.AlignmentFlag.AlignBaseline

    # PySide6语法和PyQt5一样
    NoPen = Qt.NoPen = Qt.PenStyle.NoPen  # PySide6语法和PyQt5一样
    SolidLine = Qt.SolidLine = Qt.PenStyle.SolidLine  # PySide6语法和PyQt5一样
    DashLine = Qt.DashLine = Qt.PenStyle.DashLine  # PySide6语法和PyQt5一样
    DotLine = Qt.DotLine = Qt.PenStyle.DotLine  # PySide6语法和PyQt5一样
    DashDotLine = Qt.DashDotLine = Qt.PenStyle.DashDotLine  # PySide6语法和PyQt5一样
    DashDotDotLine = Qt.DashDotDotLine = Qt.PenStyle.DashDotDotLine  # PySide6语法和PyQt5一样
    CustomDashLine = Qt.CustomDashLine = Qt.PenStyle.CustomDashLine  # PySide6语法和PyQt5一样
    # MPenStyle = Qt.MPenStyle = Qt.PenStyle.MPenStyle  # PySide6语法和PyQt5一样

    CustomContextMenu = Qt.CustomContextMenu = Qt.ContextMenuPolicy.CustomContextMenu

    Qt.Key_Escape = Qt.Key.Key_Escape
    Qt.Key_Control = Qt.Key.Key_Control
    Qt.Key_Alt = Qt.Key.Key_Alt
    Qt.Key_Shift = Qt.Key.Key_Shift
    Qt.Key_Delete = Qt.Key.Key_Delete
    Qt.Key_Backspace = Qt.Key.Key_Backspace
    Qt.Key_Up = Qt.Key.Key_Up
    Qt.Key_Down = Qt.Key.Key_Down
    Qt.Key_Left = Qt.Key.Key_Left
    Qt.Key_Right = Qt.Key.Key_Right
    Qt.Key_F1 = Qt.Key.Key_F1
    Qt.Key_F2 = Qt.Key.Key_F2
    Qt.Key_F3 = Qt.Key.Key_F3
    Qt.Key_F4 = Qt.Key.Key_F4
    Qt.Key_F5 = Qt.Key.Key_F5
    Qt.Key_F6 = Qt.Key.Key_F6
    Qt.Key_F7 = Qt.Key.Key_F7
    Qt.Key_F8 = Qt.Key.Key_F8
    Qt.Key_F9 = Qt.Key.Key_F9
    Qt.Key_F10 = Qt.Key.Key_F10
    Qt.Key_F11 = Qt.Key.Key_F11
    Qt.Key_F12 = Qt.Key.Key_F12
    Qt.Key_0 = Qt.Key.Key_0
    Qt.Key_1 = Qt.Key.Key_1
    Qt.Key_2 = Qt.Key.Key_2
    Qt.Key_3 = Qt.Key.Key_3
    Qt.Key_4 = Qt.Key.Key_4
    Qt.Key_5 = Qt.Key.Key_5
    Qt.Key_6 = Qt.Key.Key_6
    Qt.Key_7 = Qt.Key.Key_7
    Qt.Key_8 = Qt.Key.Key_8
    Qt.Key_9 = Qt.Key.Key_9
    Qt.Key_A = Qt.Key.Key_A
    Qt.Key_B = Qt.Key.Key_B
    Qt.Key_C = Qt.Key.Key_C
    Qt.Key_D = Qt.Key.Key_D
    Qt.Key_E = Qt.Key.Key_E
    Qt.Key_F = Qt.Key.Key_F
    Qt.Key_G = Qt.Key.Key_G
    Qt.Key_H = Qt.Key.Key_H
    Qt.Key_I = Qt.Key.Key_I
    Qt.Key_J = Qt.Key.Key_J
    Qt.Key_K = Qt.Key.Key_K
    Qt.Key_L = Qt.Key.Key_L
    Qt.Key_M = Qt.Key.Key_M
    Qt.Key_N = Qt.Key.Key_N
    Qt.Key_O = Qt.Key.Key_O
    Qt.Key_P = Qt.Key.Key_P
    Qt.Key_Q = Qt.Key.Key_Q
    Qt.Key_R = Qt.Key.Key_R
    Qt.Key_S = Qt.Key.Key_S
    Qt.Key_T = Qt.Key.Key_T
    Qt.Key_U = Qt.Key.Key_U
    Qt.Key_V = Qt.Key.Key_V
    Qt.Key_W = Qt.Key.Key_W
    Qt.Key_X = Qt.Key.Key_X
    Qt.Key_Y = Qt.Key.Key_Y
    Qt.Key_Z = Qt.Key.Key_Z
    Qt.Key_AsciiTilde = Qt.Key.Key_AsciiTilde

    QStyle.State_On = QStyle.StateFlag.State_On
    QStyle.State_Off = QStyle.StateFlag.State_Off
    QStyle.State_Item = QStyle.StateFlag.State_Item
    QStyle.State_Mini = QStyle.StateFlag.State_Mini
    QStyle.State_None = QStyle.StateFlag.State_None
    QStyle.State_AutoRaise = QStyle.StateFlag.State_AutoRaise
    QStyle.State_Bottom = QStyle.StateFlag.State_Bottom
    QStyle.State_Editing = QStyle.StateFlag.State_Editing
    QStyle.State_DownArrow = QStyle.StateFlag.State_DownArrow
    QStyle.State_Enabled = QStyle.StateFlag.State_Enabled
    QStyle.State_FocusAtBorder = QStyle.StateFlag.State_FocusAtBorder
    QStyle.State_HasFocus = QStyle.StateFlag.State_HasFocus
    QStyle.State_KeyboardFocusChange = QStyle.StateFlag.State_KeyboardFocusChange
    QStyle.State_MouseOver = QStyle.StateFlag.State_MouseOver
    QStyle.State_NoChange = QStyle.StateFlag.State_NoChange
    QStyle.State_Top = QStyle.StateFlag.State_Top
    QStyle.State_UpArrow = QStyle.StateFlag.State_UpArrow
    QStyle.State_Window = QStyle.StateFlag.State_Window
    QStyle.State_Sibling = QStyle.StateFlag.State_Sibling
    QStyle.State_Selected = QStyle.StateFlag.State_Selected

    QFont.Black = QFont.Weight.Black
    QFont.Bold = QFont.Weight.Bold
    QFont.Light = QFont.Weight.Light
    QFont.DemiBold = QFont.Weight.DemiBold
    QFont.ExtraBold = QFont.Weight.ExtraBold
    QFont.ExtraLight = QFont.Weight.ExtraLight
    QFont.Medium = QFont.Weight.Medium
    QFont.Normal = QFont.Weight.Normal
    QFont.Thin = QFont.Weight.Thin

    Qt.ArrowCursor = Qt.CursorShape.ArrowCursor
    Qt.UpArrowCursor = Qt.CursorShape.UpArrowCursor
    Qt.CrossCursor = Qt.CursorShape.CrossCursor
    Qt.WaitCursor = Qt.CursorShape.WaitCursor
    Qt.IBeamCursor = Qt.CursorShape.IBeamCursor
    Qt.SizeVerCursor = Qt.CursorShape.SizeVerCursor
    Qt.SizeHorCursor = Qt.CursorShape.SizeHorCursor
    Qt.SizeBDiagCursor = Qt.CursorShape.SizeBDiagCursor
    Qt.SizeFDiagCursor = Qt.CursorShape.SizeFDiagCursor
    Qt.SizeAllCursor = Qt.CursorShape.SizeAllCursor
    Qt.BlankCursor = Qt.CursorShape.BlankCursor
    Qt.SplitVCursor = Qt.CursorShape.SplitVCursor
    Qt.PointingHandCursor = Qt.CursorShape.PointingHandCursor
    Qt.ForbiddenCursor = Qt.CursorShape.ForbiddenCursor
    Qt.OpenHandCursor = Qt.CursorShape.OpenHandCursor
    Qt.ClosedHandCursor = Qt.CursorShape.ClosedHandCursor
    Qt.WhatsThisCursor = Qt.CursorShape.WhatsThisCursor
    Qt.BusyCursor = Qt.CursorShape.BusyCursor
    Qt.LastCursor = Qt.CursorShape.LastCursor
    Qt.BitmapCursor = Qt.CursorShape.BitmapCursor
    Qt.CustomCursor = Qt.CursorShape.CustomCursor
    Qt.DragCopyCursor = Qt.CursorShape.DragCopyCursor
    Qt.DragMoveCursor = Qt.CursorShape.DragMoveCursor
    Qt.DragLinkCursor = Qt.CursorShape.DragLinkCursor

    Qt.NoFocusReason = Qt.FocusReason.NoFocusReason
    Qt.MouseFocusReason = Qt.FocusReason.MouseFocusReason
    Qt.TabFocusReason = Qt.FocusReason.TabFocusReason
    Qt.BacktabFocusReason = Qt.FocusReason.BacktabFocusReason
    Qt.ActiveWindowFocusReason = Qt.FocusReason.ActiveWindowFocusReason
    Qt.PopupFocusReason = Qt.FocusReason.PopupFocusReason
    Qt.ShortcutFocusReason = Qt.FocusReason.ShortcutFocusReason
    Qt.MenuBarFocusReason = Qt.FocusReason.MenuBarFocusReason
    Qt.OtherFocusReason = Qt.FocusReason.OtherFocusReason

    Qt.ShiftModifier = Qt.Modifier.SHIFT
    Qt.ControlModifier = Qt.Modifier.CTRL
    Qt.AltModifier = Qt.Modifier.ALT
    Qt.MetaModifier = Qt.Modifier.META

    Qt.LeftButton = Qt.MouseButton.LeftButton
    Qt.RightButton = Qt.MouseButton.RightButton
    Qt.MiddleButton = Qt.MouseButton.MiddleButton

    QMessageBox.Yes = QMessageBox.StandardButton.Yes
    QMessageBox.No = QMessageBox.StandardButton.No
    QMessageBox.Retry = QMessageBox.StandardButton.Retry
    QMessageBox.Reset = QMessageBox.StandardButton.Reset
    QMessageBox.Close = QMessageBox.StandardButton.Close
    QMessageBox.Cancel = QMessageBox.StandardButton.Cancel
    QMessageBox.Escape = QMessageBox.StandardButton.Escape
    QMessageBox.Discard = QMessageBox.StandardButton.Discard

    Qt.LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
    Qt.NoDockWidgetArea = Qt.DockWidgetArea.NoDockWidgetArea
    Qt.AllDockWidgetAreas = Qt.DockWidgetArea.AllDockWidgetAreas
    Qt.RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea
    Qt.TopDockWidgetArea = Qt.DockWidgetArea.TopDockWidgetArea
    Qt.BottomDockWidgetArea = Qt.DockWidgetArea.BottomDockWidgetArea

    Qt.ElideNone = Qt.TextElideMode.ElideNone
    Qt.ElideRight = Qt.TextElideMode.ElideRight
    Qt.ElideLeft = Qt.TextElideMode.ElideLeft
    Qt.ElideMiddle = Qt.TextElideMode.ElideMiddle

    Qt.RoundCap = Qt.PenCapStyle.RoundCap
    Qt.FlatCap = Qt.PenCapStyle.FlatCap
    Qt.SquareCap = Qt.PenCapStyle.SquareCap

    Qt.RoundJoin = Qt.PenJoinStyle.RoundJoin
    Qt.RoundJoin = Qt.PenJoinStyle.MPenJoinStyle
    Qt.RoundJoin = Qt.PenJoinStyle.BevelJoin
    Qt.RoundJoin = Qt.PenJoinStyle.MiterJoin
    Qt.RoundJoin = Qt.PenJoinStyle.SvgMiterJoin

    Qt.NoBrush = Qt.BrushStyle.NoBrush
    Qt.SolidPattern = Qt.BrushStyle.SolidPattern
    Qt.BDiagPattern = Qt.BrushStyle.BDiagPattern
    Qt.ConicalGradientPattern = Qt.BrushStyle.ConicalGradientPattern
    Qt.CrossPattern = Qt.BrushStyle.CrossPattern
    Qt.Dense1Pattern = Qt.BrushStyle.Dense1Pattern
    Qt.Dense2Pattern = Qt.BrushStyle.Dense2Pattern
    Qt.Dense3Pattern = Qt.BrushStyle.Dense3Pattern
    Qt.Dense4Pattern = Qt.BrushStyle.Dense4Pattern
    Qt.Dense5Pattern = Qt.BrushStyle.Dense5Pattern
    Qt.Dense6Pattern = Qt.BrushStyle.Dense6Pattern
    Qt.Dense7Pattern = Qt.BrushStyle.Dense7Pattern
    Qt.DiagCrossPattern = Qt.BrushStyle.DiagCrossPattern
    Qt.FDiagPattern = Qt.BrushStyle.FDiagPattern
    Qt.HorPattern = Qt.BrushStyle.HorPattern
    Qt.LinearGradientPattern = Qt.BrushStyle.LinearGradientPattern
    Qt.RadialGradientPattern = Qt.BrushStyle.RadialGradientPattern
    Qt.TexturePattern = Qt.BrushStyle.TexturePattern
    Qt.VerPattern = Qt.BrushStyle.VerPattern

    Qt.WindingFill = Qt.FillRule.WindingFill
    Qt.OddEvenFill = Qt.FillRule.OddEvenFill

    QGraphicsView.RubberBandDrag = QGraphicsView.DragMode.RubberBandDrag
    QGraphicsView.NoDrag = QGraphicsView.DragMode.NoDrag
    QGraphicsView.ScrollHandDrag = QGraphicsView.DragMode.ScrollHandDrag

    QFileDialog.ShowDirsOnly = QFileDialog.Option.ShowDirsOnly
    QFileDialog.DontResolveSymlinks = QFileDialog.Option.DontResolveSymlinks

    QMessageBox.Ok = QMessageBox.StandardButton.Ok
    QMessageBox.No = QMessageBox.StandardButton.No
    QMessageBox.Yes = QMessageBox.StandardButton.Yes
    QMessageBox.YesAll = QMessageBox.StandardButton.YesAll
    QMessageBox.YesToAll = QMessageBox.StandardButton.YesToAll
    QMessageBox.Reset = QMessageBox.StandardButton.Reset
    QMessageBox.Retry = QMessageBox.StandardButton.Retry
    QMessageBox.Discard = QMessageBox.StandardButton.Discard
    QMessageBox.Abort = QMessageBox.StandardButton.Abort
    QMessageBox.Ignore = QMessageBox.StandardButton.Ignore

    QFrame.NoFrame = QFrame.Shape.NoFrame
    QFrame.Box = QFrame.Shape.Box
    QFrame.Panel = QFrame.Shape.Panel
    QFrame.WinPanel = QFrame.Shape.WinPanel
    QFrame.HLine = QFrame.Shape.HLine
    QFrame.VLine = QFrame.Shape.VLine
    QFrame.StyledPanel = QFrame.Shape.StyledPanel

    QFrame.Plain = QFrame.Shadow.Plain
    QFrame.Raised = QFrame.Shadow.Raised
    QFrame.Sunken = QFrame.Shadow.Sunken

    QApplication.exec_ = QApplication.exec

    logger.info("使用PyQt6创建GUI界面")
    qt_version = "pyqt6"

except:
    # traceback.print_exc()
    try:
        # 此处为PySide6的组件引入方式
        from PySide6 import QtGui, QtWidgets
        from PySide6.QtCore import (QDir, QStringListModel, Qt, QModelIndex, QPointF, QPoint, QRectF, QRect, QLineF,
                                    QLine, QSize, QCoreApplication, QDate, QDateTime, QLocale,
                                    QMetaObject, QObject, QTime, QUrl,
                                    QFile, Signal, Slot, Qt, QFileInfo, QMimeData, QMimeDatabase, QFileDevice,
                                    QLibrary, QLockFile, QTimer, QSaveFile, QBasicTimer, QTimeLine, QKeyCombination)
        from PySide6.QtGui import (QStandardItemModel, QStandardItem, QIcon, QPainter, QPainterPath, QPen, QColor,
                                   QFont, QPixmap,
                                   QImage, QBrush, QTransform, QIntValidator, QKeyEvent, QResizeEvent, QKeySequence,
                                   QDrag, QTextTable)
        from PySide6.QtWidgets import (QFileSystemModel, QTreeView, QMessageBox, QStyledItemDelegate,
                                       QStyleOptionViewItem, QTableWidgetSelectionRange,
                                       QListView, QStyle, QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                                       QGraphicsItem, QGridLayout, QFrame,
                                       QVBoxLayout, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem,
                                       QGraphicsSceneHoverEvent, QSizePolicy,
                                       QGraphicsSceneContextMenuEvent, QMenu, QApplication, QGraphicsLineItem,
                                       QMainWindow, QProgressBar, QButtonGroup, QRadioButton, QDialogButtonBox,
                                       QHBoxLayout, QPushButton,
                                       QLineEdit, QTextEdit, QComboBox, QTableWidgetItem, QLabel, QCheckBox,
                                       QTableWidget,
                                       QDialog, QInputDialog, QHeaderView,
                                       QSplitter, QStatusBar, QTabWidget, QScrollArea, QFileDialog, QLayout,
                                       QListWidget,
                                       QListWidgetItem,
                                       QDockWidget, QFormLayout, QColorDialog, QToolBar,
                                       QAbstractItemView, QGraphicsSceneDragDropEvent, QGraphicsTextItem
                                       )

        # 这个是常用的QAction，如果需要使用Qt3DInput的QAction，需要引入Qt3DInput后以Qt3DInput.QAction的形式引用
        from PySide6.QtGui import QAction

        from PySide6.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
        from PySide6.QtGui import QIntValidator, QKeyEvent, QBrush, QColor, QFont, QIcon, QPainter, \
            QPainterPath, QPen
        from PySide6.QtGui import QScreen
        import PySide6.QtCore as QtCore
        from PySide6.QtGui import QRegularExpressionValidator as QRegExpValidator
        from PySide6.QtUiTools import QUiLoader

        # QRegExpValidator  # Pyside6中没有QRegExpValidator类，但存在QRegularExpressionValidator，二者区别未处理

        QDesktopWidget = QScreen  # Qt6中移除了QDesktopWidget，官方建议使用QScreen代替，但二者的区别并未处理
        pyqtSignal = Signal  # PySide6中的Signal就是PyQt5中的pyqtSignal
        pyqtSlot = Slot

        QFrame.NoFrame = QFrame.Shape.NoFrame
        QFrame.Box = QFrame.Shape.Box
        QFrame.Panel = QFrame.Shape.Panel
        QFrame.WinPanel = QFrame.Shape.WinPanel
        QFrame.HLine = QFrame.Shape.HLine
        QFrame.VLine = QFrame.Shape.VLine
        QFrame.StyledPanel = QFrame.Shape.StyledPanel

        QFrame.Plain = QFrame.Shadow.Plain
        QFrame.Raised = QFrame.Shadow.Raised
        QFrame.Sunken = QFrame.Shadow.Sunken

        from PySide6.Qt3DInput import Qt3DInput


        # Qt6中组件对其方式常量所在的位置发生改变，
        # 但PySide6为了保持与PyQt语法的一致性，已经针对PyQt5的语法做了兼容工作，将Qt6中的常量位置映射到了Qt5原来的位置，
        # 因此PySide6虽然升级了，但是其中的大部分常量使用PyQt5的语法仍可以访问到

        class uic:  # PySide6和PyQt5加载.ui文件的工具不同，这里构建一个uic工具，用于加载ui文件
            def __init__(self):
                ...

            @staticmethod
            def loadUi(ui_file) -> QWidget:
                loader = QUiLoader()
                widget = loader.load(ui_file)
                return widget


        logger.info("使用PySide6创建GUI界面")
        qt_version = "pyside6"
    except:
        # 此处为PyQt5的Qt组件引入方式
        from PyQt5 import QtGui, QtWidgets
        from PyQt5.QtCore import (QDir, QStringListModel, Qt, QModelIndex, QSize, QRectF, QRect, QLineF, QLine,
                                  QPointF, QPoint, QFileInfo, QMimeData,
                                  pyqtSignal, pyqtSlot, QCoreApplication, QDate, QDateTime, QTime, QLocale, QUrl, QFile,
                                  QMetaObject, QObject, QTimer, QThread)
        from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QIcon, QPainter, QPainterPath, QPen, QColor, QFont,
                                 QImage, QBrush, QTransform, QIntValidator, QRegExpValidator, QKeyEvent, QResizeEvent,
                                 QKeySequence, QDrag, QPixmap,
                                 )
        from PyQt5.QtWidgets import (QFileSystemModel, QTreeView, QMessageBox, QStyledItemDelegate,
                                     QStyleOptionViewItem,
                                     QListView, QStyle, QWidget, QFrame,
                                     QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                                     QGraphicsItem, QGraphicsSceneMouseEvent,
                                     QHeaderView, QTableWidgetSelectionRange,
                                     QSizePolicy, QAction,
                                     QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent,
                                     QGraphicsSceneContextMenuEvent, QMenu, QApplication, QGraphicsLineItem,
                                     QMainWindow,
                                     QHBoxLayout, QGridLayout, QVBoxLayout, QPushButton, QFormLayout, QLayout,
                                     QLineEdit, QTextEdit, QComboBox, QTableWidgetItem, QLabel, QCheckBox, QTableWidget,
                                     QDialog, QInputDialog, QDockWidget, QDoubleSpinBox, QDial, QDateEdit,
                                     QSplitter, QStatusBar, QTabWidget, QScrollArea, QFileDialog, qApp,
                                     QListWidget, QListWidgetItem,
                                     QDesktopWidget, QColorDialog, QToolBar,
                                     QShortcut, QAbstractItemView,
                                     QProgressBar, QButtonGroup, QRadioButton, QDialogButtonBox,
                                     QGraphicsSceneDragDropEvent, QGraphicsTextItem
                                     )

        from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine

        import PyQt5.QtCore as QtCore
        from PyQt5.QtCore import Qt
        from PyQt5 import uic

        try:
            # 只有单独安装了pip install QScintilla之后，PyQt5包下才有Qsci包
            from PyQt5 import Qsci
            from PyQt5.Qsci import QsciScintilla, QsciDocument, QsciLexer, QsciLexerPython, QsciAPIs
        except:
            pass

        QScreen = QDesktopWidget  # Qt6中移除了QDesktopWidget，官方建议使用QScreen代替，但二者的区别并未处理
        Signal = pyqtSignal
        Slot = pyqtSlot

        # Qt6中组件对其方式常量所在的位置发生改变
        Horizontal = Qt.Horizontal
        Vertical = Qt.Vertical

        # Qt6中组件尺寸自适应方式常量所在的位置发生改变
        Fixed = QSizePolicy.Fixed
        Minimum = QSizePolicy.Minimum
        Maximum = QSizePolicy.Maximum
        Preferred = QSizePolicy.Preferred
        MinimumExpanding = QSizePolicy.MinimumExpanding
        Expanding = QSizePolicy.Expanding
        Ignored = QSizePolicy.Ignored

        # Qt6中组件尺寸自适应方式常量所在的位置发生改变
        DockWidgetClosable = QDockWidget.DockWidgetClosable
        DockWidgetFloatable = QDockWidget.DockWidgetFloatable
        DockWidgetMovable = QDockWidget.DockWidgetMovable
        NoDockWidgetFeatures = QDockWidget.NoDockWidgetFeatures
        DockWidgetVerticalTitleBar = QDockWidget.DockWidgetVerticalTitleBar
        AllDockWidgetFeatures = QDockWidget.AllDockWidgetFeatures  # 不建议使用该属性，因为Qt6中没有该属性，且该属性可以通过以上几项组合实现

        logger.info("使用PyQt5创建GUI界面")
        qt_version = "pyqt5"

# class QColorEnum(Enum):
#     black = Qt.black
#     red = Qt.red
