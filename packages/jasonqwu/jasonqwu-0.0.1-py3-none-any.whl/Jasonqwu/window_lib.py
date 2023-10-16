import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PySide6.QtCore import QEvent
import jasonqwu_lib
import logging_lib


class App(QApplication):
    def set_log(self, log):
        self.log = log
        self.log.show.debug(f"{self.arguments()}")

    def notify(self, recevier, evt):
        if recevier.inherits("QPushButton") and evt.type() == \
                QEvent.MouseButtonPress:
            self.log.show.debug(f"{recevier}, {evt}")
        return super().notify(recevier, evt)


class Window(QWidget):
    def __init__(self, config, log):
        super().__init__()
        self.log = log
        self.setWindowTitle(config["window_title"])
        self.resize(
            config["window_width"], config["window_height"])
        self.move(
            config["window_start_x"], config["window_start_y"])

    def clicked(self):
        self.label2.setText(self.label2.text() * 2)
        self.label2.adjustSize()
        self.log.show.debug(f"按钮被点击了。")

    def widgets(self):
        self.label1 = LabelTimer(self)
        self.label1.set_log(self.log)
        self.label1.set_sec(5)
        # self.label1.start_timer(1000)

        self.label2 = QLabel(self)
        self.label2.setObjectName("notice")
        self.label2.setProperty("notice_level", "warning")
        self.label2.setText("人狠话不多")
        self.label2.move(150, 150)

        # self.label2.deleteLater()

        self.btn = PushButton(self)
        self.btn.set_log(self.log)
        self.btn.setObjectName("notice")
        # self.btn.setProperty("notice_level", "warning")
        self.btn.setText("点我")
        self.btn.move(200, 200)
        self.btn.pressed.connect(self.clicked)

        # for widget in self.findChildren(QLabel):
        #     log.show.debug(widget)

    def start_timer(self, ms):
        self.timer_id = self.startTimer(ms)

    def timerEvent(self, *args, **kwargs):
        width = self.width()
        height = self.height()
        self.resize(width + 10, height + 10)
        if height > 600:
            self.log.show.debug("Window timer 停止")
            self.killTimer(self.timer_id)

    def display(self):
        self.show()
        # 教程视频：P32 16分钟
        self.log.show.debug(f"x() = {self.x()}")
        self.log.show.debug(f"y() = {self.y()}")
        self.log.show.debug(f"pos() = {self.pos()}")
        self.log.show.debug(f"width() = {self.width()}")
        self.log.show.debug(f"height() = {self.height()}")
        self.log.show.debug(f"size() = {self.size()}")
        self.log.show.debug(f"geometry() = {self.geometry()}")
        self.log.show.debug(f"rect() = {self.rect()}")
        self.log.show.debug(f"frameSize() = {self.frameSize()}")
        self.log.show.debug(f"frameGeometry() = {self.frameGeometry()}")


class PushButton(QPushButton):
    def set_log(self, log):
        self.log = log

    def event(self, evt):
        if evt.type() == QEvent.MouseButtonPress:
            self.log.show.debug(evt)
        return super().event(evt)

    def mousePressEvent(self, *args, **kwargs):
        self.log.show.debug("鼠标被按下了......")
        return super().mousePressEvent(*args, **kwargs)


class LabelTimer(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("notice")
        self.setProperty("notice_level", "normal")
        self.setText("10")
        self.move(100, 100)

    def set_log(self, log):
        self.log = log

    def set_sec(self, sec):
        self.setText(str(sec))

    def start_timer(self, ms):
        self.timer_id = self.startTimer(ms)

    def timerEvent(self, *args, **kwargs):
        current_sec = int(self.text()) - 1
        self.log.show.debug(str(current_sec))
        self.setText(str(current_sec))
        if current_sec == 0:
            self.log.show.debug("Label timer 停止")
            self.killTimer(self.timer_id)


if __name__ == '__main__':
    log = logging_lib.Logger("log")
    app = App(sys.argv)
    log.show.debug(f"{app.arguments()}")
    file = "jasonqwu.json"
    config = jasonqwu_lib.read_from_json_file(file)
    log.show.debug(f"type = {type(config)}\nconfig = {config}")
    jasonqwu_lib.write_to_json_file(file, config)

    with open("jasonqwu.qss") as f:
        app.setStyleSheet(f.read())
    window = Window(config)
    window.widgets()
    window.start_timer(500)
    window.show()
    app.exec()
    sys.exit()
