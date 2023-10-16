import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import logging_lib


log = logging_lib.Logger("log0")


class Window:
    def __init__(self):
        # 从文件中加载 UI 定义
        self.qfile = QFile("window.ui")
        self.qfile = QFile("http_client.ui")
        self.qfile.open(self.qfile.ReadOnly)
        self.qfile.close

        # 从 UI 定义中动态创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如：self.ui.text_edit, self.ui.button
        self.ui = QUiLoader().load(self.qfile)

        # self.ui.button.clicked.connect(self.handle_calc)

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
            self.ui,
            "统计结果",
            f'''薪资20000以上的有：\n{salary_above_20k}
            \n薪资20000以下的有：\n{salary_below_20k}''')
        log.show.debug(info)

    def show(self):
        self.ui.show()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
    sys.exit()


if __name__ == '__main__':
    main()
