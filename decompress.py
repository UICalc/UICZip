#  __      __   ________    _________
# |  |    |  | |__    __|  /   ______|
# |  |    |  |    |  |    |   /     
# |  |    |  |    |  |    |  |     
# |  |    |  |    |  |    |  |     
# |   \__/   |  __|  |__  |   \______
#  \________/  |________|  \_________| 
# 
#  _   _  ___   ___ ____  ___  ___
# | | | ||   | / __|_   ||   ||   \
# | |_| | | | | |__ /  /  | | |  _/
#  \___/ |___| \___|____||___||_|

# --------------    UICZip    -------------- #
# -------------- Version 0.01 -------------- #
# ---------- Decompress  Anything ---------- #

# -------------- Introduction -------------- #
################# Author:UIC #################
###### Website:united-intergalactic.com ######
####### Contact:uicalculus@outlook.com #######

# -------------- Requirements -------------- #
############### RAR: unrar,rar ###############
############## 7-Zip: py7zr, 7z ##############
################ Zip: zipfile ################


import sys
from unrar import rarfile
import zipfile
import os
import py7zr

passwords = []
len_passwords = 0
appversion = 0.01
def print_help():
    print('  _   _  ___   ___ ____  ___  ___\n | | | ||   | / __|_   ||   ||   \\\n | |_| | | | | |__ /  /  | | |  _/\n  \\___/ |___| \\___|____||___||_|') 
    print('\nWelcome to UICZip, a powerful tool that helps you to decompress anything.')
    print('Available arguments:')
    print('\t-h Help')
    print('\t-t View without decompress')
    print('\t-w Rewrite')
    print('POWERED BY UNITED INTERGALACTIC')

def check_requirements():
    print('Checking requirements...')
    if os.path.exists('C:/Program Files/7-Zip/7z.exe'):
        print('7-Zip Satisfied.')
    else:
        print('7-Zip missing.')
        return False
    return True

def load_password():
    print("Loading password database...")
    global passwords
    global len_passwords
    if not os.path.exists('C:/Users/Public/UICZip/passwords.txt'):
        print('Password file not exist. It will be generated next time.')
    else:
        f = open('C:/Users/Public/UICZip/passwords.txt', 'r')
        passwords = f.readlines()
        for index, p in enumerate(passwords):
            passwords[index] = p.replace('\n', '').replace('\r', '')
    len_passwords = len(passwords)

def write_password():
    global passwords
    if len(passwords) > len_passwords:
        passwords = list(set(passwords))
        if not os.path.exists('C:/Users/Public/UICZip'):
            os.mkdir('C:/Users/Public/UICZip')
        f = open('C:/Users/Public/UICZip/passwords.txt', 'w')
        for item in passwords:
            f.write(item + '\n')
        f.flush()
        f.close()

def decompress(f):
    global passwords
    dirname = os.path.dirname(f)
    print('Decompressing ' + f + ' to ' + dirname)

    uncompressed = True

    # zip test
    if(zipfile.is_zipfile(f)) and uncompressed:
        print('Try to decompress ' + f + ' as ZIP.')
        fp = zipfile.ZipFile(f)
        try:
            fp.extractall(path=dirname)
            fp.close()
            print(f + " Extracted without password.")
            uncompressed = False
        except:
            for pswd in passwords:
                if not uncompressed:
                    break
                print('Try: Using password ' + pswd)
                try:
                    fp.extractall(path=dirname, pwd=pswd.encode())
                    print(f + " Extracted with password.")
                    uncompressed = False
                    fp.close()
                except:
                    pass
            while uncompressed:
                pswd = input('Password error. Please enter password(Enter to skip).\n')
                if len(pswd) == 0:
                    break
                print('Try: Using password ' + pswd)
                try:
                    fp.extractall(path=dirname, pwd=pswd.encode())
                    print(f + " Extracted with password.")
                    uncompressed = False
                    passwords.append(pswd)
                    fp.close()
                except:
                    pass

    #rar test
    if(rarfile.is_rarfile(f)) and uncompressed:
        print('Try to decompress ' + f + ' as RAR.')
        fp = rarfile.RarFile(f)
        try:
            fp.extractall(path=dirname)
            fp.close()
            print(f + " Extracted without password.")
            uncompressed = False
        except:
            for pswd in passwords:
                if not uncompressed:
                    break
                print('Try: Using password ' + pswd)
                try:
                    fp.extractall(path=dirname, pwd=pswd)
                    print(f + " Extracted with password.")
                    uncompressed = False
                    fp.close()
                except:
                    pass
            while uncompressed:
                pswd = input('Password error. Please enter password(Enter to skip).\n')
                if len(pswd) == 0:
                    break
                print('Try: Using password ' + pswd)
                try:
                    fp.extractall(path=dirname, pwd=pswd)
                    print(f + " Extracted with password.")
                    uncompressed = False
                    passwords.append(pswd)
                    fp.close()
                except:
                    pass
    
    #try 7z
    if py7zr.is_7zfile(f) and uncompressed:
        print('Try to decompress ' + f + ' as 7z.')
        try:
            with py7zr.SevenZipFile(f, mode='r') as fp:
                fp.extractall(path=dirname)
                fp.close()
            uncompressed = False
            print(f + " Extracted without password.")
        except:
            for pswd in passwords:
                if not uncompressed:
                    break
                print('Try: Using password ' + pswd)
                try:
                    with py7zr.SevenZipFile(f, mode='r', password=pswd) as fp:
                        fp.extractall(path=dirname)
                        print(f + " Extracted with password.")
                        uncompressed = False
                        fp.close()
                except:
                    pass
            while uncompressed:
                pswd = input('Password error. Please enter password(Enter to skip).\n')
                if len(pswd) == 0:
                    break
                print('Try: Using password ' + pswd)
                try:
                    with py7zr.SevenZipFile(f, mode='r', password=pswd) as fp:
                        fp.extractall(path=dirname)
                        print(f + " Extracted with password.")
                        uncompressed = False
                        passwords.append(pswd)
                        fp.close()
                except:
                    pass

def main():
    if not check_requirements():
        return
    print('Starting Decompress...')
    load_password()
    files = sys.argv[1:]
    if len(files) == 0:
        print_help()
        return
    for arg in files:
        fn = arg.replace('\\', '/')
        if os.path.isfile(fn):
            decompress(fn)
        elif os.path.isdir(fn):
            for root, ds, fs in os.walk(fn):
                for fi in fs:
                    decompress(os.path.join(root, fi).replace('\\', '/'))
        else:
            print('ERROR File Path:' + fn)
    write_password()


if __name__ == '__main__':
    main()