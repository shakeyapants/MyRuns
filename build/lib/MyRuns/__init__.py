from .MyRuns import app
from .version import __version__
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

__ALL__ = ['MyRuns', 'settings', 'cli_script']