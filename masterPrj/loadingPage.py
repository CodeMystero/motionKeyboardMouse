import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,  QDesktopWidget
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer 


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        label = QLabel(self)
        layout.addWidget(label)

        movie = QMovie("loadingPage.gif")  # GIF 파일 경로로 변경해야 함
        label.setMovie(movie)
        movie.start()
        
        # 타이머 설정
        timer = QTimer(self)  # <- 추가된 부분
        timer.singleShot(8000, self.close)  # 8초 후에 close 이벤트 발생

        # Title bar 제거
        self.setWindowFlag(Qt.FramelessWindowHint)

        # 화면 중앙에 윈도우 배치
        #self.center()
        self.setGeometry(400, 200, 400, 400)
        
        
        self.setWindowTitle('GIF Viewer')
        self.show()

    # def center(self):
    #     # 창의 크기
    #     window_rect = self.frameGeometry()
    #     # 사용 중인 화면의 가운데 위치
    #     center_point = QDesktopWidget().screenGeometry().center()
    #     # 창의 가운데를 화면 가운데로 이동
    #     window_rect.moveCenter(center_point)
    #     # 윈도우를 이동
    #     self.move(window_rect.topLeft())


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()