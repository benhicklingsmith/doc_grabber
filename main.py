import io
import sys
import validators
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfFileMerger
from pathlib import Path
from PIL import Image
from urllib.request import urlopen

url_stt = 'temp'
url_end = 'temp'
pages = 87
output = 'temp'

def get_input_params():
    print("Aquiring input parameters")
    global url_stt
    global url_end
    global pages
    global output

    args = sys.argv[1:]

    if len(args) == 1:
        print("Reading values from config file")
        filename = args[0]
        f = open(filename, "r")
        url_stt = f.readline().rstrip()                   # rstrip removes any trailing return characters
        url_end = f.readline().rstrip()
        pages = int(f.readline())
        output= f.readline().rstrip()
    elif len(args) == 0:
        print("Please provide parameters: ")
        url_stt = input("First half of URL: ")
        url_end = input("Second half of URL: ")
        pages = int(input("Page count: "))
        output = input("Output file name: ")
    else:
        # TODO - print usage
        print("Invalid input parameters")
        sys.exit()

    # display inputs for user to confirm
    print("Values provided: ")
    print("\t> URL - {}*{}".format(url_stt, url_end))
    print("\t> Pgs - {}".format(pages))

    #validate url
    if isValidUrl(url_stt + "1" + url_end)  == False: 
        print("Invalid URL provided.")
        sys.exit()

    print("Input parameters aquired")

def create_document():
    print("Creating document")

    pdf_merger = PdfFileMerger()                        # Local PdfFileMerger - this is our final output file that we will append pages to as they are created.

    for x in range(1,pages+1):
        print("Creating page " + str(x), end="\r")      # Using ,end='\r' returns the cursor to the beginning of the line and overwrites previous output
        url = url_stt + str(x) + url_end
        img = get_img_from_url(url)
        pdf = img_to_pdf(img)    
        pdf_merger.append(pdf)
    
    write_PdfFileMerger(pdf_merger)
    
    print ("Finished")

def img_to_pdf(img):
    # This function takes an img and puts it into a new blank A4 pdf page. It will fill the page.

    # validate input image
    if isValidImage(img) == False : 
        return

    canvas = Canvas("page", pagesize=A4)                # Name is not relevant as it will be lost/overwritten. TODO add overloaded method that allows for name to be passed in.
    canvas.drawInlineImage(img, 0, 0, A4[0], A4[1])     # drawInlineImage(img, x, y, width, height) - Note x,y origin is bottom left of page 
    pdf = io.BytesIO()                                  #https://stackoverflow.com/questions/26880692/how-to-create-a-file-object-in-python-without-using-open
    pdf.write(canvas.getpdfdata())                      #""   
    pdf.seek(0)                                         #""
    return pdf

def isValidImage(img):
    if img == None:
        return False
    return True

def get_img_from_url(url):
    # This function returns an image aquired from an http request to a remote server
    # that can be used as if it had been opened from the local file system.

    # validate input url
    if isValidUrl(url) == False : 
        return

    r = urlopen(url=url)                               # Use urlopen from urllib.request to make the http request
    img = io.BytesIO(r.read())                         # Use read() to get the raw bytes returned (the image bytes)
    img = Image.open(img)                              # Image.open needs the raw bytes to create. This returns Image
    return img                  

def isValidUrl(url):
    if url == None:
        return False
    is_valid = validators.url(url)
    if is_valid != True:
        return False
    return True

def write_PdfFileMerger(pdf_merger):
    with Path(output).open(mode="wb") as output_file:
        pdf_merger.write(output_file)

get_input_params()
create_document()
