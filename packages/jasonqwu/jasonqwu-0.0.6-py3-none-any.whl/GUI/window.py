import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_window import Ui_window
import logging_lib


log = logging_lib.Logger("log0")


class Window(QMainWindow):
    def __init__(self):
        # 加载 Ui_window 定义
        super(Window, self).__init__()
        self.ui = Ui_window()
        self.ui.setupUi(self)
        self.ui.button.clicked.connect(self.handle_calc)

    def handle_calc(self):
        info = self.ui.text_edit.toPlainText()

        # 薪资20000以上和以下的人员名单
        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')
            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'
        QMessageBox.about(
            self,
            "统计结果",
            f'''薪资20000以上的有：\n{salary_above_20k}
            \n薪资20000以下的有：\n{salary_below_20k}''')
        log.show.debug(info)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
    sys.exit()


if __name__ == '__main__':
    main()
