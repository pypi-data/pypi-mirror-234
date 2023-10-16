from window_lib import *


log = logging_lib.Logger("log0")
app = App(sys.argv)
app.set_log(log)
file = "jasonqwu.json"
config = jasonqwu_lib.read_from_json_file(file)
log.show.debug(f"type = {type(config)}\nconfig = {config}")
jasonqwu_lib.write_to_json_file(file, config)

with open("jasonqwu.qss") as f:
    app.setStyleSheet(f.read())
window = Window(config, log)
window.move(400, 200)
window.resize(400, 300)
window.setGeometry(400, 100, 500, 500)
window.setFixedSize(500, 500)
# window.widgets()
count = 20
columns = 4
width = window.width() / columns
height = window.height() / (((count - 1) // columns) + 1)
for i in range(count):
    w = QLabel(window)
    w.setObjectName("notice")
    w.resize(width, height)
    w.move((i % columns) * width, (i // columns) * height)
window.show()
app.exec()
sys.exit()
