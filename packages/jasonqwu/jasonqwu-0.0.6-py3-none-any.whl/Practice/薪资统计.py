from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit

def calculate():
	print("统计按钮被点击了。")

def main():
	app = QApplication([])

	window = QMainWindow()
	window.setWindowTitle("薪资统计")
	window.resize(500, 400)
	window.move(300, 310)

	text = QPlainTextEdit(window)
	text.setPlaceholderText("请输入薪资表")
	text.resize(300, 350)
	text.move(10, 25)

	button = QPushButton("统计", window)
	button.move(380, 80)
	button.clicked.connect(calculate)

	window.show()

	app.exec_()

if __name__ == '__main__':
	main()