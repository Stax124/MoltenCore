import argparse
import inspect
import os
import sys


def build():
    os.system(f'docker build --build-arg TRINITY_TOKEN={os.environ["TRINITY"]} -t "modular-bot" .')

def start():
    os.system('python main.py')
    
def migrate():
    os.system('alembic revision --autogenerate')
    
def upgrade():
    os.system('alembic upgrade head')

def poetryExport():
    os.system('poetry export > requirements.txt')

functions_found = [i[0] for i in inspect.getmembers(sys.modules[__name__], inspect.isfunction)]
parser = argparse.ArgumentParser(description='Utility script for modular-bot')
parser.add_argument("script", help="Script to run", choices=functions_found)
args = parser.parse_args()

# call function with name in args.script
sys.modules[__name__].__dict__[args.script]()
