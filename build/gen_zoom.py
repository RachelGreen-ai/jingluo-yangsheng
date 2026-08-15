#!/usr/bin/env python3
# Add detail-zoom modals (局部放大图) to each meridian, cropped from the hi-res CC0 photo,
# with every point in the region plotted large + fully labeled. Also decides which points get a
# name label on the MAIN figure (the sparse ones) vs. in a zoom (the dense clusters).
# Run AFTER gen_geom.py + snap_geom.py (it reads the snapped coords and rewrites geom/<key>.py).
import os,sys,runpy,base64
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
SRC={'front':Image.open('/tmp/front1280.jpg').convert('RGB'),
     'back':Image.open('/tmp/back1280.jpg').convert('RGB')}
PXU=12.8  # pixels per normalized unit at 1280 wide (150 units tall = 1920)

# shared region crops: name -> (x0,y0,x1,y1, src)
RECTS={
 'front_hand'   :(14,58,42,90,'front'),
 'front_face'   :(36,3,58,25,'front'),
 'front_headside':(37,3,51,23,'front'),
 'front_earhead':(38,8,52,22,'front'),
 'front_torso'  :(34,26,58,72,'front'),
 'front_legfoot':(33,99,57,127,'front'),
 'back_shu'     :(35,26,61,73,'back'),
 'back_foot'    :(34,118,52,143,'back'),
}

# per meridian: list of (rectname, id, chip, title, sub, clusterLabel)
ZOOMS={
 'li':[('front_hand','hand','⊕ 手·前臂放大','手 · 前臂 放大','手背、腕、前臂桡侧诸穴','手'),
       ('front_face','face','⊕ 面·颈放大','面 · 颈 放大','颈、面、鼻旁诸穴','面')],
 'sj':[('front_hand','hand','⊕ 手·前臂放大','手 · 前臂 放大','无名指、手背、腕、前臂诸穴','手'),
       ('front_earhead','head','⊕ 耳·头侧放大','耳 · 头侧 放大','绕耳与眉梢诸穴','耳')],
 'st':[('front_face','face','⊕ 头面放大','头 · 面 放大','眼下、面颊、下关、头维诸穴','面'),
       ('front_torso','torso','⊕ 胸腹放大','胸 · 腹 放大','胸线、腹线（天枢等）诸穴','腹'),
       ('front_legfoot','leg','⊕ 小腿·足放大','小腿 · 足 放大','足三里到厉兑诸穴','腿')],
 'sp':[('front_torso','torso','⊕ 胸腹放大','胸 · 腹 放大','腹、胸胁诸穴','腹'),
       ('front_legfoot','leg','⊕ 小腿·足放大','小腿内侧 · 足 放大','隐白到阴陵泉诸穴','腿')],
 'ht':[('front_hand','hand','⊕ 手·腕放大','手 · 腕 放大','肘内到小指诸穴','手')],
 'si':[('front_hand','hand','⊕ 手·前臂放大','手 · 前臂 放大','小指、手背、腕、前臂诸穴','手'),
       ('front_face','face','⊕ 面颊·耳放大','面颊 · 耳 放大','颈、颧、耳前诸穴','面')],
 'bl':[('back_shu','shu','⊕ 背俞穴放大','背部 · 俞穴 放大','背部两条侧线的脏腑俞穴','背'),
       ('back_foot','foot','⊕ 小腿·足放大','小腿 · 足外侧 放大','委中以下到至阴诸穴','足')],
 'ki':[('front_torso','torso','⊕ 胸腹放大','胸 · 腹 放大','腹、胸诸穴','腹'),
       ('front_legfoot','leg','⊕ 足·小腿放大','足 · 小腿内侧 放大','涌泉到阴谷诸穴','腿')],
 'pc':[('front_hand','hand','⊕ 手·腕放大','手 · 腕 · 中指 放大','曲泽到中冲诸穴','手')],
 'gb':[('front_headside','head','⊕ 头侧·耳放大','头侧 · 耳 放大','颞、耳、风池诸穴','头'),
       ('front_legfoot','leg','⊕ 小腿·足放大','小腿 · 足外侧 放大','阳陵泉到足窍阴诸穴','腿')],
 'lr':[('front_legfoot','leg','⊕ 足·小腿放大','足 · 小腿内侧 放大','大敦到膝内诸穴','腿')],
}

def idx(code):
    return int(''.join(c for c in code if c.isdigit()))

def make_crop(name):
    x0,y0,x1,y1,src=RECTS[name]
    im=SRC[src]
    box=(int(x0*PXU),int(y0*PXU),int(x1*PXU),int(y1*PXU))
    crop=im.crop(box)
    p=os.path.join(HERE,'assets',name+'.jpg')
    crop.save(p,quality=88)
    b=base64.b64encode(open(p,'rb').read()).decode()
    open(os.path.join(HERE,'assets',name+'.b64'),'w').write(b)
    return len(b)

def build_zoom(key):
    gpath=os.path.join(HERE,'data','geom',key+'.py')
    G=runpy.run_path(gpath)['G']
    coords=G['coords']
    zooms=[]; clusters=[]; inzoom=set()
    for (rectname,zid,chip,title,sub,clab) in ZOOMS.get(key,[]):
        x0,y0,x1,y1,src=RECTS[rectname]
        w=x1-x0; zvh=round((y1-y0)/w*100,1)
        inpts=[]
        for code,c in coords.items():
            if c.get('x') is None or not c.get('onMain',True): continue
            x,y=c['x'],c['y']
            if x0<=x<=x1 and y0<=y<=y1: inpts.append((idx(code),code,x,y))
        if len(inpts)<2: continue
        inpts.sort()
        zpts=[{'code':code,'x':round((x-x0)/w*100,2),'y':round((y-y0)/w*100,2)} for (_,code,x,y) in inpts]
        vessel='M'+' L'.join('%g,%g'%(p['x'],p['y']) for p in zpts)
        zooms.append({'id':zid,'chip':chip,'title':title,'sub':sub+'（真人图 CC0）',
                      'viewBox':'0 0 100 %g'%zvh,'img':rectname,'vessel':vessel,'points':zpts})
        for (_,code,_,_) in inpts: inzoom.add(code)
        clusters.append({'x':round((x0+x1)/2,2),'y':round((y0+y1)/2,2),'label':clab,'zoom':zid})
    # main-figure labels: label every on-figure point NOT shown in a zoom; alternate
    # label sides along the meridian so adjacent labels don't collide.
    for code,c in coords.items():
        if code in inzoom: c.pop('k',None); c.pop('lab',None)
    labeled=sorted([code for code,c in coords.items()
                    if c.get('x') is not None and c.get('onMain',True) and code not in inzoom], key=idx)
    for i,code in enumerate(labeled):
        coords[code]['k']=1
        coords[code]['lab']='L' if i%2==0 else 'R'
    if zooms:
        G['zoom']=zooms
        G['overlay']['clusters']=clusters
    with open(gpath,'w',encoding='utf-8') as f:
        f.write('# gen_geom.py + snap_geom.py + gen_zoom.py — coords, paths & detail zooms on CC0 photo\n')
        f.write('G='+repr(G)+'\n')
    print('%-4s zooms=%d labeled-on-main=%d in-zoom=%d'%(
        key,len(zooms),sum(1 for c in coords.values() if c.get('k')),len(inzoom)))

if __name__=='__main__':
    # crops first (dedup shared)
    made=set()
    for zl in ZOOMS.values():
        for z in zl:
            if z[0] not in made: make_crop(z[0]); made.add(z[0])
    print('crops:',sorted(made))
    keys=sys.argv[1:] or list(ZOOMS)
    for k in keys: build_zoom(k)
