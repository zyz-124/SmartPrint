import os
import sys

if getattr(sys, "frozen", False):
    BUNDLE_DIR = sys._MEIPASS
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BUNDLE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = BUNDLE_DIR

SUBJECTS_DIR = os.path.join(BASE_DIR, "subjects")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMPLATES_DIR = os.path.join(BUNDLE_DIR, "templates")
FORMATS_DIR = os.path.join(BUNDLE_DIR, "formats")

DEFAULT_FORMAT = "思维导图"
DEFAULT_THEME = "素雅灰"
DEFAULT_STYLE = "简约几何"
