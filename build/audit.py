#!/usr/bin/env python3
"""逐穴审查：把一条经在主图上的所有 onMain 穴位渲染出来(带名)，肉眼查错。
用法: python3 build/audit.py gb   |   python3 build/audit.py all
输出 /tmp/audit_<key>.jpg
"""
import sys, os, base64, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
from PIL import Image, ImageDraw, ImageFont
CJK='/System/Library/Fonts/STHeiti Medium.ttc'
A=os.path.join(os.path.dirname(os.path.abspath(__file__)),'assets')

def load(img):
    raw=base64.b64decode(open(os.path.join(A,img+'.b64')).read().strip())
    return Image.open(io.BytesIO(raw)).convert('RGB')

VBH={'front':150,'back':150}

def audit(key):
    M=build.get_M(key)
    img=M['img']; vbh=VBH.get(img,150)
    im=load(img).copy(); W,H=im.size; dr=ImageDraw.Draw(im)
    fnt=ImageFont.truetype(CJK,max(11,W//60))
    n=0
    for p in M['points']:
        if not p.get('onMain',True) or p.get('x') is None: continue
        x,y=p['x'],p['y']; px,py=x/100*W,y/vbh*H
        dr.ellipse([px-3,py-3,px+3,py+3],fill=(200,30,30),outline=(255,255,255))
        dr.text((px+4,py-7),f"{p['code']} {p['name']}",fill=(10,40,160),font=fnt)
        n+=1
    out=f'/tmp/audit_{key}.jpg'; im.save(out,quality=86)
    print(f'{key:5s} {img:5s} {n:2d} onMain pts -> {out}')

if __name__=='__main__':
    keys=sys.argv[1:] or ['gb']
    if keys==['all']: keys=build.ALL
    for k in keys: audit(k)
