import logging
from rich import print, pretty, inspect
from rich.traceback import install
from rich.console import Console
from rich.logging import RichHandler

console = Console()

test_data = [
    {"jsonrpc": "2.0", "method": "sum", "params": [None, 1, 2, 4, False, True], "id": "1",},
    {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]},
    {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": "2"},
]

def test_log():
    enabled = False
    context = {
        "foo": "bar",
    }
    movies = ["Deadpool", "Rise of the Skywalker"]
    console.log("Hello from", console, "!")
    console.log(test_data, log_locals=True)

def test_rich():
	a = [1, 2]
	print("Hello [red]rich[/red] :boy:")
	print(locals())
	pretty.install()	# locals() => print(locals())
	inspect(a, methods=True)
	install()
	# 1/0
	FORMAT = "%(message)s"
	logging.basicConfig(
		level = "NOTSET",
		format = FORMAT,
		datefmt = "[%X]",
		handlers = [RichHandler()]
		)
	log = logging.getLogger("rich")
	log.info("hello rich")
	log.error("hello rich")
	log.debug("hello rich")
	test_log()
