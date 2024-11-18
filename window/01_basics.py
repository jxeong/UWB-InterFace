## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QToolTip, QMainWindow, QAction, qApp, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, QDate, Qt, QTime, QDateTime

# 날짜 예제 (QDate, Qt)
now = QDate.currentDate()
#print(now.toString('yyyy.MM.dd'))
#print(now.toString(Qt.ISODate)) #-로 구분되는 표준 형식
print(now.toString(Qt.DefaultLocaleLongDate)) #컴퓨터 기본 설정

# 시간 예제 (QTime): hh.mm.ss로 프린트 형식 설정 가능
time = QTime.currentTime()
print(time.toString())
print(time.toString(Qt.DefaultLocaleLongDate))
print(time.toString(Qt.DefaultLocaleShortDate))

# 날짜, 시간 같이 (QDateTime)
dateTime = QDateTime.currentDateTime()
print(dateTime.toString('yyyy-MM-dd hh:mm'))

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # exit?
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # 상태바(화면 하단)
        #self.statusBar().showMessage('Not Okay')
        self.statusBar()

        # 메뉴바
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

        # 툴바
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # 툴팁(=마우스 올렸을 때 설명) self에 하면 화면에 마우스 올리면 나타남
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('I can''t understand you')

        # 버튼
        btn = QPushButton('to. seonghwa', self)
        btn.setToolTip('I <b>love</b> you') # 마우스 올렸을 때 설명
        btn.move(50,200)
        btn.resize(btn.sizeHint()) #버튼 크기 알아서 정해주는 코드(텍스트 사이즈 맞춰)
        btn.clicked.connect(QCoreApplication.instance().quit)
        # 버튼 누르면 clicked signal 발생하고
        # connect 메소드가 시그널을 quit 슬롯에 연결

        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('icon.png'))
        #self.move(500, 300) #창 띄울 위치 설정(가로, 세로)
        #self.resize(500, 200) #창 크기 설정(가로, 세로)
        self.setGeometry(300, 300, 500, 600) #창 위치, 크기 고정(창 위치+창 크기)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   #ex = MyApp()
   #sys.exit(app.exec_())
