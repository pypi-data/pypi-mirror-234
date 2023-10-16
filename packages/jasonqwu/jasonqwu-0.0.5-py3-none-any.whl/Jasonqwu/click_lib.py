import click
 
@click.command()
#@click.option('--rate', '-r', type=int, help="输入比率（整数）")  # 指定 rate 是 int 类型
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')

def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
	hello()