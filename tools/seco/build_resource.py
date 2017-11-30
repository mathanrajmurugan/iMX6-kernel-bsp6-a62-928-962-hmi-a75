#!/usr/bin/python

import base64

IMAGES = [("green", "sbc_j8.png")]



f = open("resources.py", "w")

HEADER = """import wx
import wx.lib.embeddedimage
"""
f.write(HEADER)

for img in IMAGES:
    img_text = base64.encodestring(open(img[1],"rb").read())
    f.write("%s = wx.lib.embeddedimage.PyEmbeddedImage(\"\"\""% img[0])
    f.write(img_text)
    f.write("\"\"\")\n\n")

f.close
