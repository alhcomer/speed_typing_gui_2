from ctypes import alignment
from tkinter.ttk import Separator, Style
from english_words import english_words_lower_alpha_set
from PyQt6.QtWidgets import (QWidget, QStyle, QPushButton, QLineEdit, QDialog, QToolButton,
        QInputDialog, QApplication, QLabel, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QLCDNumber, QSlider)
from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont, QMouseEvent
import random
import sys
import time


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.widgets = Widgets()
        self.setCentralWidget(self.widgets)
        # self.setStyleSheet(stylesheet)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.title_bar = TitleBar(self)
        self.setContentsMargins(0, self.title_bar.height(), 0, 0)
        self.resize(640, self.title_bar.height() + 480)
        
        


    # def changeEvent(self, event):
    #     if event.type() == event.WindowStateChange:
    #         self.title_bar.setWindowState(self.windowState())

    # def resizeEvent(self, event):
    #     self.title_bar.resize(self.width(), self.title_bar.height())
        

        

class TitleBar(QWidget):
    clickPos = None
    def __init__(self, parent):
        super().__init__(parent)
        self.autoFillBackground()
        # self.setBackgroundRole(QPalette.shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addStretch()

        self.title = QLabel("Speed Typing Test", self, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.title.setForegroundRole(QPalette.light)

        style = self.style()
        print(style)
        ref_size = self.fontMetrics().height()
        ref_size += style.pixelMetric(style.PixelMetric.PM_ButtonMargin) * 2
        self.setMaximumHeight(ref_size + 2)

        btn_size = QSize(ref_size, ref_size)
        for action in ('min', 'normal', 'max', 'close'):
            btn = QToolButton(self)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            layout.addWidget(btn)
            btn.setFixedSize(btn_size)

            iconType = getattr(style,
                f'SP_TitleBar{action.capitalize()}Button')
            btn.setIcon(style.standardIcon(iconType))

            if action == 'close':
                colorNormal = 'red'
                colorHover = 'orangered'
            else:
                colorNormal = 'palette(mid)'
                colorHover = 'palette(light)'
            btn.setStyleSheet('''
                QToolButton {{
                    background-color: {};
                }}
                QToolButton:hover {{
                    background-color: {}
                }}
            '''.format(colorNormal, colorHover))

            signal = getattr(self, action + 'Clicked')
            btn.clicked.connect(signal)

            setattr(self, action + 'Button', btn)
        
        self.normalButton.hide()

        self.updateTitle(parent.windowTitle())
        parent.windowTitleChanged.connect(self.updateTitle)

    def updateTitle(self, title=None):
        if title is None:
            title = self.window().windowTitle()
        width = self.title.width()
        width -= self.style().pixelMetric(QStyle.PixelMetric.PM_LayoutHorizontalSpacing) * 2
        self.title.setText(self.fontMetrics().elidedText(
            title, Qt.TextElideMode.ElideRight, width))

    def windowStateChanged(self, state):
        self.normalButton.setVisible(state == Qt.WindowState.WindowMaximized)
        self.maxButton.setVisible(state != Qt.WindowState.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clickPos = event.windowPos().toPoint()

    def mouseReleaseEvent(self, QMouseEvent):
        self.clickPos = None

    def closeClicked(self):
        self.window().close()
    
    def maxClicked(self):
        self.window().showMaximized()

    def normalClicked(self):
        self.window().showNormal()

    def minClicked(self):
        self.window().showMinimized()

    def resizeEvent(self, event):
        self.title.resize(self.minButton.x(), self.height())
        self.updateTitle()
        
            

   

            
            



        # https://stackoverflow.com/questions/44241612/custom-titlebar-with-frame-in-pyqt5
        # This page is usefull in trying to create a title bar

        
        
        


          


class Widgets(QWidget):
    def __init__(self):
        super().__init__()
        self.words_list = list(english_words_lower_alpha_set)

        title_label = QLabel("Welcome to the Speed Typing Test!")
        title_label.setFont(QFont('Helvetica', 22))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        word_to_type = QLabel(random.choice(self.words_list))
        word_to_type.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label = QLabel("Start Typing to Begin")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        


        grid = QGridLayout()
        grid.addWidget(title_label, 1, 1)
        grid.addWidget(word_to_type, 2, 1)
        grid.addWidget(instruction_label, 3, 1)
        



        self.setLayout(grid)
        

        self.show()

        
        

        # title_label = QLabel("Press Me!")


        # # Set the central widget of the Window.
        # self.setCentralWidget(title_label)
        # self.show()

stylesheet = """
    QMainWindow {
        border-image: url(background.jpg)
    }
"""





def main():

    app = QApplication(sys.argv)
    main_window = MainWindow()
    layout = QVBoxLayout(main_window)
    # main_widgets = Widgets()
    # layout.addWidget(main_widgets)
    main_window.show()
    main_window.setWindowTitle("Aidan's Speed Typing Test")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()