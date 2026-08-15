#!/usr/bin/env python3
# Generate build/data/geom/<key>.py for the 11 non-lung meridians.
# Coordinates are anatomical anchors on the CC0 front/back photos (viewBox 0 0 100 150);
# intervening points are distributed evenly by index between anchors.
import os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE,'data','geom'))
from _util import place_anchored, mirror

VB='0 0 100 150'

# Each spec: abbr,count,img, anchors[(i,x,y)], extra{i:(x,y[,False])}, key[i...],
#            lines[[(x,y)...],...] (vessel/qi; if None -> from anchors), mirror(bool)
SPEC={}

def A(*a): return list(a)

# ---------- 大肠 LI (front, → face) ----------
SPEC['li']=dict(abbr='LI',count=20,img='front',mirror=True,
  anchors=A((1,22,84),(4,24,80),(5,26.5,77),(11,32,64),(14,34.5,52),(15,33,39),(17,45,24),(18,45.5,21.5),(19,47,20),(20,48,18.3)),
  extra={16:(35,36)}, key=[4,10,11,15,20],
  lines=[[(22,84),(24,80),(26.5,77),(30,69),(32,64),(34.5,52),(33,39),(43,28),(45,24),(45.5,21.5),(48,16.5)]])

# ---------- 三焦 SJ (front, → ear/brow) ----------
SPEC['sj']=dict(abbr='SJ',count=23,img='front',mirror=True,
  anchors=A((1,31,85),(4,29,78),(5,29,75),(10,34,63),(13,35.5,50),(14,34,39),(16,45,22),(17,43.5,17),(20,42.5,12.5),(21,43.5,15),(23,44.5,13)),
  extra={}, key=[5,10,14,17],
  lines=[[(31,85),(29,78),(31,71),(34,63),(35.5,50),(34,39),(43,27),(45,22),(43.5,17),(42.5,12.5),(43.5,15),(44.5,13)]])

# ---------- 胃 ST (front, face→toe, bilateral) ----------
SPEC['st']=dict(abbr='ST',count=45,img='front',mirror=True,
  anchors=A((1,45.5,15.5),(4,47.5,21),(6,43.5,20),(9,46.5,23.5),(12,45,26),
            (13,42,29),(18,41,43),(19,45.3,47),(25,45.3,57.8),(30,45.3,70),(31,42,76),
            (32,43,90),(34,43.5,106),(35,44,112),(36,43,116),(40,41.5,121),(41,45,128),(44,46.5,137),(45,45,139)),
  extra={7:(43,17),8:(43,9)}, key=[25,36,40,45,4],
  lines=[[(46.5,15),(47,18.5),(44,20),(46.5,21.5),(43.5,26),(42,32),(41,42),(43,47),(44,58),(44,68),(42,74),(43,90),(43.5,106),(44,112),(43,116),(42,121),(44.5,128),(46,134),(45,139)]])

# ---------- 脾 SP (front, toe→chest, medial) ----------
SPEC['sp']=dict(abbr='SP',count=21,img='front',mirror=True,
  anchors=A((1,48,139),(4,48,133),(5,47.5,129),(6,48,120),(9,47.5,112),(10,46,106),
            (12,42.5,70),(14,42,63),(15,42,57.5),(16,42,52),(17,38,43),(20,38,33),(21,36,46)),
  extra={}, key=[6,9,10,1],
  lines=[[(48,139),(48,133),(47.5,129),(48,120),(47.5,112),(46,105),(42.5,70),(42,57.5),(41,45),(38,40),(36,46)]])

# ---------- 心 HT (front, axilla→little finger, inner arm) ----------
SPEC['ht']=dict(abbr='HT',count=9,img='front',mirror=True,
  anchors=A((1,37,40),(3,36,64),(7,34.5,79),(9,37,84)),
  extra={}, key=[3,7,9],
  lines=[[(37,40),(36.5,52),(36,64),(35,73),(34.5,79),(35.5,82),(37,84)]])

# ---------- 小肠 SI (front, little finger→shoulder→face) ----------
SPEC['si']=dict(abbr='SI',count=19,img='front',mirror=True,
  anchors=A((1,37,84),(3,35,79),(8,37,64),(9,36,42),(11,41,37),(14,44,32),(16,46,23),(19,42.5,15.8)),
  extra={18:(44.5,16.8)}, key=[3,8,11,19],
  lines=[[(37,84),(35.5,80),(35,79),(36,73),(37,64),(36,42),(38,38),(41,37),(44,32),(46,25),(46,23),(45,18),(43.5,15.5)]])

# ---------- 膀胱 BL (BACK photo, eye→head→back(2 lines)→leg→little toe) ----------
SPEC['bl']=dict(abbr='BL',count=67,img='back',mirror=True,
  anchors=A((3,47.5,9),(10,47.5,20),(11,46,29),(30,47,68.5),
            (31,47.5,64),(35,48.5,70),(36,45,81),(40,45.5,110),
            (41,43,33),(54,43.5,69),(55,45.5,114),(60,44,128),(67,42,138.5)),
  extra={1:(47.5,4.5,False),2:(47.5,7,False)},
  key=[13,15,18,20,23,40,57,67],
  lines=[
    [(47.5,4.5),(47.5,9),(48,6),(47.5,20),(46,29),(47,68.5),(48.5,70),(45,81),(45.5,110),(45,120),(44,128),(43,134),(42,138.5)],
    [(43,33),(43,50),(43.5,69)],
  ])

# ---------- 肾 KI (front, sole→medial leg→chest) ----------
SPEC['ki']=dict(abbr='KI',count=27,img='front',mirror=True,
  anchors=A((1,46,140),(3,48,129),(7,48,124),(10,48,112),(11,48.3,69),
            (16,48.3,57.5),(21,48.3,46),(22,46.5,43),(27,46.5,28)),
  extra={}, key=[1,3,10],
  lines=[[(46,140),(47.5,132),(48,129),(48,124),(48,112),(48.3,69),(48.3,57.5),(48.3,46),(46.5,40),(46.5,28)]])

# ---------- 心包 PC (front, chest→middle finger, inner arm) ----------
SPEC['pc']=dict(abbr='PC',count=9,img='front',mirror=True,
  anchors=A((1,38,41),(3,33,64),(6,31,76),(7,30.5,79),(9,27,85)),
  extra={}, key=[6,7,9],
  lines=[[(38,41),(35,50),(33,64),(31.5,74),(31,76),(30.5,79),(28,82),(27,85)]])

# ---------- 胆 GB (front, outer eye→head-side→body-side→lateral leg→4th toe) ----------
SPEC['gb']=dict(abbr='GB',count=44,img='front',mirror=True,
  anchors=A((1,44.5,14),(8,42,10),(12,43,15),(14,46,12),(17,46,6),(20,46,18.5),
            (21,41,31),(24,39,45),(25,36,55),(29,38,71),(30,35,77),
            (34,42,114),(40,43,128),(44,42,138)),
  extra={}, key=[20,21,30,34,40,44],
  lines=[[(44.5,14),(42.5,11),(42,10),(46,10),(46,6),(45.5,14),(46,18.5),(41,31),(38,42),(39,45),(36,55),(38,60),(40,67),(35,77),(39,92),(41,110),(42,114),(43,122),(43,128),(43,134),(42,138)]])

# ---------- 肝 LR (front, big toe→medial leg→flank) ----------
SPEC['lr']=dict(abbr='LR',count=14,img='front',mirror=True,
  anchors=A((1,47,139),(3,47,134),(4,47.5,129),(8,47,111),(9,46,102),(12,46,70),(13,38,52),(14,40,45)),
  extra={}, key=[3,8,13,14],
  lines=[[(47,139),(47,134),(47.5,129),(48,120),(47,111),(46,102),(46,70),(42,58),(38,52),(40,45)]])


def dmulti(lines):
    segs=[]
    for ln in lines:
        segs.append('M'+' L'.join('%g,%g'%(x,y) for x,y in ln))
    return ' '.join(segs)

def build_geom(key):
    s=SPEC[key]; ab=s['abbr']; n=s['count']
    codes=['%s%d'%(ab,i) for i in range(1,n+1)]
    anchors=[('%s%d'%(ab,i),x,y) for (i,x,y) in s['anchors']]
    keyset={'%s%d'%(ab,i) for i in s.get('key',[])}
    coords=place_anchored(anchors, codes, key=keyset)
    for i,v in s.get('extra',{}).items():
        c='%s%d'%(ab,i)
        d={'x':v[0],'y':v[1],'onMain':(v[2] if len(v)>2 else True)}
        if c in keyset: d['k']=1
        coords[c]=d
    lines=s.get('lines') or [[ (a[1],a[2]) for a in anchors ]]
    vessel=dmulti(lines)
    vfaint=dmulti([[(mirror(x),y) for (x,y) in ln] for ln in lines]) if s.get('mirror') else None
    qi=[[x,y] for x,y in lines[0]]
    G={'img':s['img'],'viewBox':VB,
       'qi':{'vbw':100,'vbh':150,'path':qi},
       'overlay':{'vessel':vessel,'flow':vessel},
       'coords':coords}
    if vfaint: G['overlay']['vesselFaint']=vfaint
    # write file
    out=os.path.join(HERE,'data','geom',key+'.py')
    with open(out,'w',encoding='utf-8') as f:
        f.write('# auto-generated by gen_geom.py — anatomical coords on CC0 photo\n')
        f.write('G='+repr(G)+'\n')
    non_main=sum(1 for c in coords.values() if not c.get('onMain',True))
    print('geom %-4s %2d pts, vessel segs=%d, off-figure=%d -> %s'%(key,n,len(lines),non_main,out))

if __name__=='__main__':
    keys=sys.argv[1:] or list(SPEC)
    for k in keys: build_geom(k)
