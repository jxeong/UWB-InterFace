## Ex 3-8. 창을 화면의 가운데로.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        self.center() # 창이 화면의 가운데에 위치하게 함
        self.show()

    def center(self):
        qr = self.frameGeometry() #창 위치와 크기 정보 읽어옴
        cp = QDesktopWidget().availableGeometry().center() #모니터의 가운데 위치 파악
        qr.moveCenter(cp) #직사각형 위치를 화면 중심으로 이동
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
