import time
import os
import subprocess
from safaribooks import SafariBooks


class Object(object):
    bookid = None
    # cred = SafariBooks.parse_cred("mac.96@live.it:aprilia65")
    cred = SafariBooks.parse_cred("mortacci.tua.tua@gmail.com:mortacci.tua2")
    no_cookies = False
    log = False
    kindle = False


def convertEPUBFromCode(bookid: str):
    folder = list((f for f in os.scandir('.\\Books')
                  if (f.is_dir() and (bookid in f.name))))
    if len(folder) > 0:
        folder = folder[0]
        print("Found book: " + folder.name)
        convertEPUBFromFolder(folder.path)
    else:
        print("Book {0} not found".format(bookid))


def convertEPUBFromFolder(path: str):
    files = list((f for f in os.scandir(path) if (
        f.is_file() and ('.epub' in f.name))))
    fclear = list((f for f in files if '_CLEAR.epub' in f.name))
    if len(fclear) > 0:
        print("Found book converted: " + fclear[0].path)
    else:
        epub = files[0]
        print("Start conversion in: " + epub.path)
        path1 = '"C:\\Books\\safaribooks\\' + epub.path[2:] + '"'
        path2 = '"C:\\Books\\safaribooks\\' + \
            epub.path[2:-5] + '_CLEAR' + epub.path[-5:] + '"'
        cmd = 'cd "C:\\Program Files (x86)\\Calibre2" && .\\ebook-convert.exe {0} {1}'.format(
            path1, path2)
        print(cmd)
        proc = subprocess.Popen(
            cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()
        if err:
            print("Conversion error")
            print(err.decode('windows-1252'))
        else:
            print("Conversion completed")


def handle_error(bookid, file, error):
    print("Error " + error + " on book " + bookid)
    with open(file, 'a') as f:
        f.write(bookid + '\n')


def pop(file):
    with open(file, 'r+') as f:  # open file in read / write mode
        firstLine = f.readline()  # read the first line and throw it out
        data = f.read()  # read the rest
        f.seek(0)  # set the cursor to the top of the file
        f.write(data)  # write the data back
        f.truncate()  # set the file size to the current size
        return firstLine


def waiting(sec: int):
    if sec > 0:
        print("wainting {0} sec...".format(sec))
        time.sleep(sec)


def start_batch_download():
    args = Object()
    timesec = 0
    while True:
        waiting(timesec)
        print("Check books")
        bookid = pop('books.txt').split(" ")[0].strip()
        if not bookid:
            timesec = 60
            continue
        args.bookid = bookid
        print("Download book " + bookid)
        try:
            SafariBooks(args)
        except Exception as e:
            handle_error(bookid, 'books_error.txt', str(e))
            timesec = 15
            continue
        with open('books_downloaded.txt', 'a') as f:
            f.write(bookid + '\n')
        print("Completed " + bookid)
        # convertEPUBFromCode(bookid)
        timesec = 15


if __name__ == "__main__":
    # folder_list = list((f for f in os.scandir('.\\Books') if f.is_dir()))
    # for folder in folder_list:
    #     print("Found folder: " + folder.name)
    #     convertEPUBFromFolder(folder.path)
    # convertEPUBFromCode('9781492076322')
    start_batch_download()
