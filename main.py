import sys
import pandas as pd
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DataVisualizer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create main layout
        layout = QVBoxLayout()

        # Create widgets
        self.loadButton = QPushButton('Load CSV')
        self.loadButton.clicked.connect(self.loadCSV)

        self.comboBox = QComboBox(self)
        self.comboBox.setVisible(False)
        self.comboBox.currentIndexChanged.connect(self.plotData)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setVisible(False)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.canvas.setVisible(False)

        # Add widgets to layout
        layout.addWidget(self.loadButton)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.tableWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('CSV Data Visualizer')
        self.show()

    def loadCSV(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Load CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if filePath:
            self.data = pd.read_csv(filePath)
            self.showDataInTable()
            self.populateComboBox()

    def showDataInTable(self):
        self.tableWidget.setVisible(True)
        self.tableWidget.setRowCount(self.data.shape[0])
        self.tableWidget.setColumnCount(self.data.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(self.data.columns)

        for row in range(self.data.shape[0]):
            for col in range(self.data.shape[1]):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(self.data.iloc[row, col])))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def populateComboBox(self):
        self.comboBox.setVisible(True)
        self.comboBox.clear()
        self.comboBox.addItems(self.data.columns)

    def plotData(self):
        column = self.comboBox.currentText()
        ax = self.canvas.figure.subplots()
        ax.bar(self.data.index, self.data[column])
        ax.set_title(column)
        self.canvas.draw()
        self.canvas.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = DataVisualizer()
    sys.exit(app.exec_())
