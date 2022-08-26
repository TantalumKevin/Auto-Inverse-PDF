import datetime, os, fitz

def Inverse(pdfPath, newPath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    pdfDoc = fitz.open(pdfPath)   # 打开源PDF
    outdoc = fitz.open()    # 建立输出PDF
    for page in pdfDoc:
        pix = page.get_pixmap(dpi=600)
        pix.invert_irect()
        outdoc.new_page(pno=-1, width= page.rect.x1, height= page.rect.y1)          # 输出文件新建页
        outpage = outdoc[-1]
        outpage.insert_image(outpage.rect,pixmap=pix)
        
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('转换时间=', (endTime_pdf2img - startTime_pdf2img).seconds,'s')
    if os.path.exists(newPath):
        os.remove(newPath)
    pdfDoc.close()
    outdoc.save(newPath)          # 保存pdf文件
    outdoc.close()

if __name__ == "__main__":
    pdfPath = "./PDF/陶瓷.pdf"
    newPath = "./out/反色-陶瓷.pdf"
    Inverse(pdfPath, newPath)