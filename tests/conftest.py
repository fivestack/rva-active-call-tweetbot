from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent

sys.path.insert(0, str(PROJECT_ROOT.absolute()))

from src import rva_active_call_tweetbot
