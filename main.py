import os
import shutil
import requests
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileMerger
from pathlib import Path

url_stt = 'null'
url_end = 'null'
pages = 1
output_dir = 'temp'


def tidy_up():
    # delete the directory if it already exists
    try:
        shutil.rmtree(output_dir) # use shutil.rmtree here instead of os.rmdir as it works if the directory is not empty
    except OSError as err:
        print("Deletion of the directory %s failed" % output_dir)

def setup():
    tidy_up()

    global url_stt
    global url_end
    global pages

    url_stt = input("First half of URL: ")
    url_end = input("Second half of URL: ")
    pages = int(input("Page count: "))

    print("Values provided: ")
    print("\t> URL - {}_{}".format(url_stt, url_end))
    print("\t> Pgs - {}".format(pages))

    # create output directory
    os.mkdir(output_dir)
    print("Setup complete")


def get_pages():
    for x in range(1,pages+1):
        # Update user on profress
        progress = "Getting page " + str(x)
        print (progress, end="\r")              # Using ,end='\r' returns the cursor to the beginning of the line and overwrites previous output
        
        # local variables
        url = url_stt + str(x) + url_end
        filename = output_dir + '\\page' + str(x) + '.jpg'

        # Get and write the file to local jpg
        r = requests.get(url, stream = True)    # Use stream = True to guarantee no interruptions.
        r.raw.decode_content = True             # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        with open(filename,'wb') as f:          # Open a local file with wb ( write binary ) permission.
            shutil.copyfileobj(r.raw, f)        # Copy downloaded file to local jpg in output folder
    

    print ("Finished getting pages")

def create_pdf():
    # First - convert each jpg to a pdf
    print("Creating pages")
    pages_act = pages+1
    for x in range(1,pages_act):
        print("Creating page " + str(x), end="\r")
        filename = output_dir + '\\page' + str(x)
        filename_jpg = filename + '.jpg'
        filename_pdf = filename + '.pdf'
        canvas = Canvas(filename_pdf, pagesize=A4)
        canvas.drawInlineImage(filename_jpg, 0, 0, A4[0], A4[1])
        canvas.save()
    
    print("Finished creating pages")
    print("Creating single doc")

    # Second - merge all pdfs into one output file
    pdf_merger = PdfFileMerger()
    for x in range(1,pages_act):
        print("Appending page " + str(x), end="\r")
        input_file = output_dir + '\\page' + str(x) + '.pdf'
        pdf_merger.append(input_file)

    print("Finished appending pages")
    with Path("document.pdf").open(mode="wb") as output_file:
        pdf_merger.write(output_file)
    
    print("Finished creating single doc")

    
setup()
get_pages()
create_pdf()
tidy_up()
