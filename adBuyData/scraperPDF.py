from PIL import Image
import pytesseract
import glob
import os


def filelist(pathspec):
    files = [X for X in glob.glob(pathspec) if os.stat(X).st_size != 0]
    #make sure to return only pdf files
    return files



if __name__ == "__main__":

    #for state in states
    #enter state directory
    print filelist("cafdsfa")
    #for file in fileList
    #fileName = file.split('.')
    #im = Image.open(file)
    #im.save(fileName+.tiff)