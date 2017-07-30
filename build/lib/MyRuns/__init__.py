from .MyRuns import create_app
from .version import __version__
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
app = create_app()

__ALL__ = ['MyRuns', 'settings', 'cli_script']
