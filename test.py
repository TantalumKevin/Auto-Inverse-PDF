import datetime
import os

from PIL import Image
import PIL.ImageOps  
import glob

import fitz



def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间

    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)   # 打开pdf
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg] #取出指定页
        rotate = int(0) # 不进行旋转
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 5  
        zoom_y = zoom_x
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img = PIL.ImageOps.invert(img)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        img.save(imagePath + '/' + 'images_%s.png' % pg, "PNG")
        print("<<转换进度>>\t"+str(100*pg/pdfDoc.pageCount)+"%", flush=True)
 
    endTime_pdf2img = datetime.datetime.now()  # 结束时间
    print('pdf转换时间=', (endTime_pdf2img - startTime_pdf2img).seconds)


def pic2pdf(imagePath, newPath):
  doc = fitz.open()
  for img in sorted(glob.glob(imagePath + "/*")): # 读取图片，确保按文件名排序
    print("添加页面"+str(img))
    imgdoc = fitz.open(img)         # 打开图片
    pdfbytes = imgdoc.convertToPDF()    # 使用图片创建单页的 PDF
    imgpdf = fitz.open("pdf", pdfbytes)
    doc.insertPDF(imgpdf)          # 将当前页插入文档
  if os.path.exists(newPath):
    os.remove(newPath)
  doc.save(newPath)          # 保存pdf文件
  doc.close()

if __name__ == "__main__":
    pdfPath = "./PDF/陶瓷.pdf"
    newPath = "./out/反色-陶瓷.pdf"
    imagePath = "实分析"
    pyMuPDF_fitz(pdfPath, imagePath)
    pic2pdf(imagePath,newPath)

