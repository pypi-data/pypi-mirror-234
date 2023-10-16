import Aciembler.translator
from tabulate import tabulate
from HHLtools.prints import *
import os
import sys
import shutil
import time
from tkinter import filedialog
import tkinter as tk
import platform



def new_file():
    base = os.path.dirname(os.path.abspath(__file__))
    if ((path := filedialog.asksaveasfilename(defaultextension='.xlsx')) == ''):
        return
    try:
        shutil.copy(base + '/data/Template.xlsx', path)
    except Exception as e:
        print(e)


def edit_file(path=''):
    if path != '':
        print('File found! Opening file')
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            os.system(f'open {path}')
    else:
        if ((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            return

        print('File found! Opening file')
        time.sleep(1.5)
        if platform.system() == 'Windows':
            os.startfile(path)
        else:
            os.system(f'open {path}')

    while ((choice := input('Finished editing? [y/n]: ')) != 'y'):
        pass



def load_file(path=''):
    if path == '':
        if ((path := filedialog.askopenfilename(defaultextension='.xlsx')) == ''):
            return

    print('Scanning source code...')
    time.sleep(0.5)
    print('Which base are you using for the memory address in the source code')
    print(tabulate([['[1]', 'Denary'], ['[2]', 'Binary'], ['[3]', 'Hexadecimal']]))

    while ((choice := input('Input your choice [1], [2], [3]: ')) not in ['1', '2', '3']):
        print('Invalid input, please input again')

    choice = int(choice)
    base = ['d', 'b', 'h'][choice - 1]

    while (input('Code Loaded Successfully, execute now? [y/n]: ') != 'y'):
        pass

    print('')
    print('Preparing translation...')
    time.sleep(1)
    print('Loading translator...')
    if platform.system() == 'Windows':
        print(r'C:\Windows\System32\translator.exe')
    else:
        print('~/System/Applications/translator.app')
    time.sleep(0.5)
    print('Translator loaded successfully, doing first pass...')
    time.sleep(0.5)
    translator.run(base, path)
    print("Aciembling completed")



def exit():
    sys.exit(0)


root = 0


def start():
    global root
    print('正在加载资源....')
    time.sleep(.5)
    print('正在调取文件....')
    time.sleep(.5)
    print('海内存知己, 天涯若比邻......')
    time.sleep(.5)
    print('与君初相识, 犹如故人归......')
    time.sleep(.5)
    print('有朋自远方来, 不亦说乎......')
    time.sleep(.5)
    print('青, 取之于蓝, 而青于蓝; 冰, 水为之而寒......')
    time.sleep(.5)
    print('正在准备您的Aciembler, 请勿关闭计算机......')
    print('正在连接服务器......')
    time.sleep(1)
    print('请稍后......')
    time.sleep(0.5)
    print('网络似乎出了点问题......')
    time.sleep(0.5)
    print('连接失败! 正在调取离线Aciembler')
    time.sleep(1)
    print('加载完成, 正在进入....')

    prints(' Welcome to the Aciembler-preter ', fontStyle=FontStyle.BOLD, fontColor=FontColor.BLACK,
           backgroundColor=BackgroundColor.WHITE)
    print('v1.0.16')
    print('developed by 黄浩霖 & 姚安北')
    print('Guangdong Country Garden School')
    print(f'你好, {os.getlogin()}, 别来无恙啊')

    while True:
        table = [['[1]', 'Create New File'], ['[2]', 'Edit exsiting file'], ['[3]', 'Load Existing File'],
                 ['[4]', 'Help'], ['[5]', 'Exit']]
        print(tabulate(table))
        choice = input('Input your choice 1, 2, 3, 4, 5: ')
        root = tk.Tk()
        root.withdraw()
        match choice:
            case '1':
                new_file()
            case '2':
                edit_file()
            case '3':
                load_file()
            case '4':
                ins = \
                    """
                    INSTRUCTION
                    ======================================================
                    1. Create New File
                        Select a directory you will create your program at, no need to add the file extension,
                        it will be automatically added

                    2. Edit exsiting file
                        Select your program, and it will open automatically

                    3. Load Existing File
                        Select your program, and it will be loaded and executed
                    ======================================================
                    """
                print(ins)
            case '5':
                exit()
            case _:
                print('Invalid input, please input again!')

