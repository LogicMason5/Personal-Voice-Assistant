# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Jarvis 2.0")
        MainWindow.resize(1440, 900)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1440, 900))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # Run button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1180, 800, 101, 51))
        self.pushButton.setStyleSheet("""
            background-color: rgb(0, 170, 255);
            font: 75 18pt "MS Shell Dlg 2";
            color: white;
            border-radius: 10px;
        """)
        self.pushButton.setObjectName("pushButton")

        # Exit button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1310, 800, 101, 51))
        self.pushButton_2.setStyleSheet("""
            background-color: rgb(255, 0, 0);
            font: 75 18pt "MS Shell Dlg 2";
            color: white;
            border-radius: 10px;
        """)
        self.pushButton_2.setObjectName("pushButton_2")

        # Top-left gif label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 401, 91))
        self.label_2.setText("")
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        # Time box
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(640, 30, 291, 61))
        self.textBrowser.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: white;
            border: none;
        """)
        self.textBrowser.setObjectName("textBrowser")

        # Date box
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(930, 30, 291, 61))
        self.textBrowser_2.setStyleSheet("""
            font: 75 16pt "MS Shell Dlg 2";
            background-color: transparent;
            color: white;
            border: none;
        """)
        self.textBrowser_2.setObjectName("textBrowser_2")

        # Status / output box
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(1000, 500, 431, 281))
        self.textBrowser_3.setStyleSheet("""
            font: 11pt "MS Shell Dlg 2";
            background-color: rgba(0, 0, 0, 120);
            color: white;
            border-radius: 10px;
            padding: 10px;
        """)
        self.textBrowser_3.setObjectName("textBrowser_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jarvis 2.0"))
        self.pushButton.setText(_translate("MainWindow", "Run"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Load GIFs
        self.load_gifs()

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.run_jarvis)
        self.ui.pushButton_2.clicked.connect(self.close_app)

        # Timer for time/date
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        # Initial display
        self.show_time()
        self.ui.textBrowser_3.append("System initialized.")
        self.ui.textBrowser_3.append("Press Run to start Jarvis.\n")

    def load_gifs(self):
        # Background animated GIF
        self.bg_movie = QtGui.QMovie("Jarvis/utils/images/live_wallpaper.gif")
        self.ui.label.setMovie(self.bg_movie)
        self.bg_movie.start()

        # Top-left animated GIF
        self.init_movie = QtGui.QMovie("Jarvis/utils/images/initiating.gif")
        self.ui.label_2.setMovie(self.init_movie)
        self.init_movie.start()

    def show_time(self):
        current_time = QtCore.QTime.currentTime().toString("hh:mm:ss")
        current_date = QtCore.QDate.currentDate().toString("dddd, dd MMMM yyyy")

        self.ui.textBrowser.setText(current_time)
        self.ui.textBrowser_2.setText(current_date)

    def run_jarvis(self):
        self.ui.textBrowser_3.append("Jarvis is running...")
        self.ui.textBrowser_3.append("Listening for commands...")
        self.ui.statusbar.showMessage("Jarvis started", 3000)

    def close_app(self):
        self.ui.textBrowser_3.append("Closing Jarvis...")
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
