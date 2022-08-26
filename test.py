import datetime, os, numpy, fitz, PIL.ImageOps
from xml.dom.minidom import Document 
from PIL import Image



def Inverse(pdfPath, newPath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    pdfDoc = fitz.open(pdfPath)   # 打开源PDF
    outdoc = fitz.open()    # 建立输出PDF
    for page in pdfDoc:
        pix = page.get_pixmap(dpi=600)
        page.get_svg_image()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = PIL.ImageOps.invert(img)
        imgdoc = numpy.array(img)   
        (width, height,_) = imgdoc.shape
        samples = bytearray(imgdoc.tobytes())  
        nndoc = fitz.open('png',samples) 
        pix = fitz.Pixmap(fitz.csRGB, width, height, samples)
        outdoc.new_page(pno=-1,width=width, height=height)
        newpage = outdoc[-1]
        #newpage.show_pdf_page(
        pdfbytes = nndoc.convert_to_pdf()    # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        outdoc.insertPDF(imgpdf)          # 将当前页插入文档
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf转换时间=', (endTime_pdf2img - startTime_pdf2img).seconds,'s')
    if os.path.exists(newPath):
        os.remove(newPath)
    pdfDoc.close()
    outdoc.save(newPath)          # 保存pdf文件
    outdoc.close()

if __name__ == "__main__":
    pdfPath = "./PDF/陶瓷.pdf"
    newPath = "./out/反色-陶瓷.pdf"
    Inverse(pdfPath, newPath)