import sys

import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from RangeFunctions import *



class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Holdem Range Visualiser'
        self.filename = 'BB3Bet'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.main_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.main_widget)

        h_plot = PlotCanvas(self.main_widget)
        button = QPushButton('Browse', self)
        button.clicked.connect(self.getfiles)

        self.layout.addWidget(button)
        self.layout.addWidget(h_plot)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def getfiles(self):
         self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.currentPath(),
                                                                 '*.csv')


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(53 / 255, 53 / 255, 53 / 255), tight_layout=True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.filename = 'BB3Bet'
        self.plot_data()
        self.draw()

    def plot_data(self):
        columns = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        rows = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        cell_text = [[b + a if columns.index(a) > columns.index(b) else a + b for a in columns] for b in columns]

        self.ax = self.figure.add_subplot()
        self.ax.axis('tight')
        self.ax.axis('off')
        self.ax.set_facecolor('black')

        hand_dict = create_dict(filename='BB3bet', stat='3Bet PF')
        col_data, label = create_array(hand_dict, hand_list)

        df = pd.DataFrame(col_data, index=rows, columns=columns)
        vals = np.around(df.values, 2)
        norm = plt.Normalize(vals.min() - 1, vals.max() + 1)
        colours = plt.cm.Greens(norm(vals))

        visual = self.ax.table(cellText=cell_text, cellLoc='center', loc='center', cellColours=colours)
        visual.scale(1.0, 1.5)



if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    App.setPalette(palette)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(App.exec_())
