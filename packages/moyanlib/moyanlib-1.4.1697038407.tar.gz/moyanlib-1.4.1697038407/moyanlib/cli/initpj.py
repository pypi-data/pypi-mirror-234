from pip._internal import main as pip
from pipenv import cli
def hygl():
    try:
        import pipenv
    except:
        pip(['install','pipenv'])
    cli.command