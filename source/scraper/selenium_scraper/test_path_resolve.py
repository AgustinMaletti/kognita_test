# from pathlib import Path
# from source.config import BASE_DIR, BASE_DIR_DATA
#
# # BASE_DIR_here = Path(__file__).resolve().parent.parent.parent
#
# print('hello world')
# print(BASE_DIR.joinpath('data'))
# filename = 'data2.txt'
# FILE_DATA_NAME = BASE_DIR_DATA.joinpath(filename)
from time import sleep

while True:
    print('Please enter a keyword to search in StackOverFlow:', end=' ')
    keyword = input('')
    sleep(1)
    print('How much questions do you wont per page, 15, 30 or 50:', end=' ')
    q_per_page = input('')
    print('Please enter the name of the file:', end=' ')
    file_name = input('')
    if '.' in file_name:
        file_name = file_name.split('.')[0]
        file_name = file_name + '.json'
    print('Your config is:')
    print('keyword: ', keyword)
    print('Question per page:', q_per_page)
    print('File name ', file_name)

    print('Its Ok, yes or no')
    ok_or_not = input()
    if ok_or_not == 'yes':
        break
    else:
        continue
print('Loading config')

