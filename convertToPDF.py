from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
import sys

point = 1
textsize = 12
inch = 72

def convert(fileName, outName):
    print('converting %s to pdf' %fileName)
    ptr = open(fileName, 'r')  # text file I need to convert
    episodes = ptr.read().split('\n\n=======')
    episodes = ['=======' + x for x in episodes]
    episodes[0] = episodes[0][7:]
    height = len(episodes[1].split('\n')) + 3
    width = max([len(x) for x in episodes[1].split('\n')]) 

    ptr.close()

    c = canvas.Canvas(outName , pagesize=(width*textsize*0.65 , height*textsize))

    for ep in episodes:
        v = (height - 2) * textsize
        c.setStrokeColorRGB(0,0,0)
        c.setFillColorRGB(0,0,0)
        c.setFont('Courier', textsize * point)
        for line in ep.split('\n'):
            c.drawString( 0.3 * inch, v, line)
            v -= textsize * point    
        c.showPage()
    c.save()


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
