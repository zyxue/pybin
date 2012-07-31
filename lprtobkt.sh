f=$1

pdf2ps ${f} _tmp.ps
psbook _tmp.ps _tmp2.ps
ps2pdf _tmp2.ps _tmp3.pdf

# lpr -P Lexmark-C543\
#  -o MediaColor=PrinterS\
#  -o PageSize=Letter\
#  -o PageRegion=Letter\
#  -o InputSlot=Tray1\
#  -o Trays=Tray1\
#  -o OptDuplex=InstalledM\
#  -o Resolution=2400x1200dpi\
#  -o TonerDarkness=PrinterS\
#  -o LexBrightness=PrinterS\
#  -o LexContrast=PrinterS\
#  -o LexSaturation=PrinterS\
#  -o LexLineDetail=PrinterS\
#  -o CyanBalance=PrinterS\
#  -o MagentaBalance=PrinterS\
#  -o YellowBalance=PrinterS\
#  -o BlackBalance=PrinterS\
#  -o OutputBin=PrinterS\
#  -o MediaType=PrinterS\
#  -o LexBlankPage=PrinterS\
#  -o ManualRGBImage=PrinterS\
#  -o ManualRGBText=PrinterS\
#  -o ManualRGBGraphics=PrinterS\
#  -o ManualCMYK=PrinterS\
#  -o Duplex=None\
#  -o Collate=True\
#  -o SepPages=PrinterS\
#  -o SepSource=PrinterS\
#  -o sides=two-sided-long-edge\
#  -o number-up=2\
#  _tmp3.pdf

rm _tmp.ps _tmp2.ps # _tmp3.pdf