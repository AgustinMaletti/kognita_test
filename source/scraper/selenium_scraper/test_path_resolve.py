from pathlib import Path
from source.config import BASE_DIR, BASE_DIR_DATA

# BASE_DIR_here = Path(__file__).resolve().parent.parent.parent

print('base dir data is')
# print(BASE_DIR.joinpath('data'))
filename = 'data2.txt'
FILE_DATA_NAME = BASE_DIR_DATA.joinpath(filename)