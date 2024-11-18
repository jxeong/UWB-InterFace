import sys
#import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QLineEdit, QPushButton, \
    QMessageBox, QDialog
from PyQt5.QtGui import QFont, QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QPoint

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('초기 설정')
        self.setGeometry(300, 300, 200, 200)

        # Layout for input fields
        layout = QVBoxLayout()

        # Input fields and labels
        self.workspace_width_input = QLineEdit(self)
        self.workspace_height_input = QLineEdit(self)
        self.danger_width_input = QLineEdit(self)
        self.danger_height_input = QLineEdit(self)

        # Confirm button
        confirm_button = QPushButton("확인", self)
        confirm_button.clicked.connect(self.accept)

        # Add widgets to layout
        layout.addWidget(QLabel("작업 공간 가로 크기:"))
        layout.addWidget(self.workspace_width_input)
        layout.addWidget(QLabel("작업 공간 세로 크기:"))
        layout.addWidget(self.workspace_height_input)
        layout.addWidget(QLabel("위험 구역 가로 크기:"))
        layout.addWidget(self.danger_width_input)
        layout.addWidget(QLabel("위험 구역 세로 크기:"))
        layout.addWidget(self.danger_height_input)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def getValues(self):
        try:
            workspace_width = int(self.workspace_width_input.text())
            workspace_height = int(self.workspace_height_input.text())
            danger_width = int(self.danger_width_input.text())
            danger_height = int(self.danger_height_input.text())
            return workspace_width, workspace_height, danger_width, danger_height
        except ValueError:
            QMessageBox.warning(self, "Input Error", "모든 값을 숫자로 입력해주세요.")
            return None

class UWBMonitoringSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.person_selected = False

    def initUI(self):
        # Set main window properties
        self.setWindowTitle('UWB Monitoring System')

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title Label
        title = QLabel("UWB 모니터링 시스템", self)
        title.setFont(QFont("Arial", 30, QFont.Bold))
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: black;")
        main_layout.addWidget(title)

        # Placeholder for workspace and danger zone
        self.workspace_frame = QFrame(self)
        self.workspace_frame.setStyleSheet("background-color: #3D3D3D;")
        self.workspace_layout = QVBoxLayout(self.workspace_frame)

        # 작업 공간 (workspace_frame) 추가
        main_layout.addWidget(self.workspace_frame, alignment=Qt.AlignCenter)
        info_layout = QVBoxLayout()

        self.info_container = QWidget(self)
        self.info_container.setFixedWidth(200)  # 정보 섹션 폭 고정
        self.info_container.setLayout(info_layout)

        self.info_label_1 = QLabel("작업 공간 크기: -", self)
        self.info_label_1.setFont(QFont("Arial", 14))
        self.info_label_1.setStyleSheet("background-color: #E0E0E0; padding: 5px; border-radius: 5px;")

        info_label_2 = QLabel("UWB 센서 개수: ", self)
        info_label_2.setFont(QFont("Arial", 14))
        info_label_2.setStyleSheet("background-color: #E0E0E0; padding: 5px; border-radius: 5px;")

        info_label_3 = QLabel("현재 작업자 수: ", self)
        info_label_3.setFont(QFont("Arial", 14))
        info_label_3.setStyleSheet("background-color: #E0E0E0; padding: 5px; border-radius: 5px;")

        self.info_label_4 = QLabel("기계작동여부: Off", self)
        self.info_label_4.setFont(QFont("Arial", 14))
        self.info_label_4.setStyleSheet("background-color: #E0E0E0; padding: 5px; border-radius: 5px;")

        info_layout.addWidget(self.info_label_1)
        info_layout.addWidget(info_label_2)
        info_layout.addWidget(info_label_3)
        info_layout.addWidget(self.info_label_4)

        # 수동 제어 버튼 추가
        self.toggle_button = QPushButton("기계 전원 On/Off 수동 버튼", self)
        self.toggle_button.clicked.connect(self.toggleMachineStatus)
        info_layout.addWidget(self.toggle_button)

        # main_layout에 info_container를 추가하여 정보 섹션이 workspace 아래에 위치하도록 설정
        main_layout.addWidget(self.info_container)

        # 프로그램 시작 시 입력 다이얼로그 호출
        self.showInputDialog()

    def showInputDialog(self):
        dialog = InputDialog()
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.getValues()
            if values:
                self.drawWorkspace(*values)

    def drawWorkspace(self, workspace_width, workspace_height, danger_width, danger_height):
        # Check if danger zone fits within the workspace
        if danger_width > workspace_width or danger_height > workspace_height:
            QMessageBox.warning(self, "Dimension Error", "위험 구역은 작업 공간의 안에 있어야 합니다.")
            return

        # Update workspace frame size
        self.workspace_frame.setFixedSize(workspace_width, workspace_height)

        # Update workspace size display
        self.info_label_1.setText(f"작업 공간 크기: {workspace_width} x {workspace_height}")

        # Clear previous widgets in workspace layout
        for i in reversed(range(self.workspace_layout.count())):
            self.workspace_layout.itemAt(i).widget().setParent(None)

        # Danger Zone (yellow background) - centered
        self.danger_zone = QFrame(self)
        self.danger_zone.setStyleSheet("background-color: #FFD000;")
        self.danger_zone.setFixedSize(danger_width, danger_height)

        # Danger Zone Icon and Label
        danger_layout = QVBoxLayout(self.danger_zone)
        danger_icon = QLabel("⚠️", self)
        danger_icon.setAlignment(Qt.AlignCenter)
        danger_icon.setFont(QFont("Arial", 40))

        danger_text = QLabel("danger zone", self)
        danger_text.setFont(QFont("Arial", 14))
        danger_text.setAlignment(Qt.AlignCenter)

        danger_layout.addWidget(danger_icon)
        danger_layout.addWidget(danger_text)

        # Add danger zone to workspace frame, centered
        self.workspace_layout.addWidget(self.danger_zone, alignment=Qt.AlignCenter)

        # Adjust main window size to fit the workspace and fixed info section width
        total_width = max(workspace_width, self.info_container.width()) + 50
        total_height = workspace_height + self.info_container.height() + 250  # 여유 공간 추가
        self.setFixedSize(total_width, total_height)

        # person 아이콘 추가
        self.person = QLabel(self.workspace_frame)
        self.person.setPixmap(QPixmap("user.png").scaled(50, 50, Qt.KeepAspectRatio))
        self.person.setFixedSize(50, 50)  # 아이콘 크기 조정
        self.person.setStyleSheet("background: transparent;")
        self.person.show()

    def mousePressEvent(self, a0: QMouseEvent = None):
        # 클릭한 위치가 person 내에 있는지 확인
        if self.person.geometry().contains(self.workspace_frame.mapFromGlobal(a0.globalPos())):
            # person을 선택하거나 선택을 해제
            self.person_selected = not self.person_selected
        elif self.person_selected:
            # person이 선택된 상태에서 다른 위치를 클릭하면 그 위치로 이동
            new_pos = self.workspace_frame.mapFromGlobal(a0.globalPos()) - QPoint(self.person.width() // 2,
                                                                                  self.person.height() // 2)
            self.person.move(new_pos)
            self.updateMachineStatus()
            self.person_selected = False  # 이동 후 선택 해제

    def updateMachineStatus(self):
        # person이 danger zone 내에 있는지 확인
        person_rect = self.person.geometry()
        danger_rect = self.danger_zone.geometry()

        if danger_rect.contains(person_rect.center()):
            self.info_label_4.setText("기계작동여부: Off")
            self.danger_zone.setStyleSheet("background-color: #2afc69;")
        else:
            self.info_label_4.setText("기계작동여부: On")
            self.danger_zone.setStyleSheet("background-color: #FFD000;")

    def toggleMachineStatus(self):
        # person이 danger zone 내에 있는지 확인
        person_rect = self.person.geometry()
        danger_rect = self.danger_zone.geometry()

        # 현재 상태에 따라 기계 작동 여부 수동 토글
        if self.info_label_4.text() == "기계작동여부: On":
                self.info_label_4.setText("기계작동여부: Off")
                self.danger_zone.setStyleSheet("background-color: #2afc69;")
        else: #사람이 작업 공간 내에 없을 때만 수동 On 가능
            if not danger_rect.contains(person_rect.center()):
                self.info_label_4.setText("기계작동여부: On")
                self.danger_zone.setStyleSheet("background-color: #FFD000;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UWBMonitoringSystem()
    window.show()
    sys.exit(app.exec_())