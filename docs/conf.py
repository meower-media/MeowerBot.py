import sys
import os

sys.path.append(os.path.abspath('sphinxext'))

extensions = ['myst-parser']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

version = "2.3.0"

copyright = "ShowierData9978, 2022 - 2023"

