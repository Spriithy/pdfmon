from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def read_pdf(file):
    # create a StringIO object to hold the text of the PDF file
    text_io = StringIO()

    # create a PDFResourceManager object
    rsrcmgr = PDFResourceManager()

    # create a TextConverter object
    converter = TextConverter(rsrcmgr, text_io, laparams=LAParams())

    # create a PDFPageInterpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, converter)

    # open the PDF file
    with open(file, "rb") as fp:
        # iterate over the pages of the PDF file
        for page in PDFPage.get_pages(fp):
            # process each page
            interpreter.process_page(page)

    # close the converter
    converter.close()

    # get the text from the StringIO object
    text = text_io.getvalue()

    # close the StringIO object
    text_io.close()

    # return the text of the PDF file
    return text
