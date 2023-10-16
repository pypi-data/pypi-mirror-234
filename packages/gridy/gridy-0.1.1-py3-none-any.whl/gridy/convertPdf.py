from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter,XMLConverter,HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO,StringIO

converters={"xml":XMLConverter,"html":HTMLConverter,"text":TextConverter}

def convert_pdf_doc(pdf_path,output_type="xml"):
    rsc=PDFResourceManager()
    bio=BytesIO()
    conv=converters[output_type](rsc,bio,laparams=LAParams())
    interp=PDFPageInterpreter(rsc,conv)

    with open(pdf_path,'rb') as fp:
        for pg in PDFPage.get_pages(fp,caching=False,check_extractable=True):
            interp.process_page(pg)
        
        txt=bio.getvalue()
    # close open handles

    conv.close()
    bio.close()

    if txt:
        return txt