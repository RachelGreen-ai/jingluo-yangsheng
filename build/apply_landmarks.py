#!/usr/bin/env python3
"""Overlay landmark-computed acupoint coordinates onto the geom files.

Regions handled this pass (clean MediaPipe wins):
  * leg  (st/sp/ki/gb/lr): front_legfoot crop  ->  WINDOWED zoom into `front`
          photo, coords from Pose (body_front).  Main-figure leg coords updated.
  * face (li/st/si):       front_face crop, coords from FaceMesh (face_pts).

Deferred (kept as-is): torso, hand, head/ear, back-shu, foot.

Windowed zoom = the full base photo drawn at natural size with the SVG viewBox
cropped to a sub-rectangle; points keep their full-body coordinates, so the
zoom and the main figure are guaranteed consistent (no remapping).
"""
import os, runpy, shutil, sys
from acu_formulas import body_front, body_back, face_pts, fronthand_pts, palm_hand, dorsal_hand, torso_pts, backshu_pts

HERE = os.path.dirname(os.path.abspath(__file__))
GEOM = os.path.join(HERE, 'data', 'geom')
MZOOM= os.path.join(HERE, 'data', 'mzoom')
BK   = os.path.join(GEOM, '_pre_lm')
BKM  = os.path.join(MZOOM, '_pre_lm')
os.makedirs(BK, exist_ok=True); os.makedirs(BKM, exist_ok=True)

MF = body_front()      # front frame (viewBox 0 0 100 150)
MB = body_back()       # back  frame
FC = face_pts()        # front_face frame (0 0 100 100)
FH = fronthand_pts()   # front_hand frame (0 0 100 114.5)
PH = palm_hand()       # hand.b64 palm frame (0 0 100 157)
DH = dorsal_hand()     # dorsalhand.b64 frame (0 0 100 157.8) — ulnar side cropped
TR = torso_pts()       # front frame (0 0 100 150), navel-calibrated 骨度
BS = backshu_pts()     # back frame, 膀胱经背俞 按椎体定位

def bl_vessel(coords):
    """膀胱经主图双线: 内线(BL11-40含八髎会阳→接腿→足) + 外线(BL41-54)。返回(路径, 镜像路径)。"""
    mir=lambda x: round(99-x,2)
    def poly(codes, m=False):
        pts=[coords[c] for c in codes if c in coords and coords[c].get('x') is not None]
        if len(pts)<2: return ''
        return 'M'+' L'.join(f"{(mir(p['x']) if m else p['x'])},{p['y']}" for p in pts)
    inner=[f'BL{i}' for i in list(range(11,41))+list(range(55,68))]
    outer=[f'BL{i}' for i in range(41,55)]
    d =(poly(inner)+' '+poly(outer)).strip()
    dm=(poly(inner,True)+' '+poly(outer,True)).strip()
    return d, dm

LEG_MERIDIANS   = {'st','sp','ki','gb','lr'}
FACE_MERIDIANS  = {'li','st','si'}
HAND_MERIDIANS  = {'li','ht','si','pc','sj'}
TORSO_MERIDIANS = {'st','sp','ki'}

# 连接段穴位(肩/腋/胁/髋等)不在地标公式内，手工核对后的坐标，放在躯干侧不压到手臂
CONNECTOR = {
 'gb':{'GB21':(44,32),'GB22':(41.5,40),'GB23':(42,43.5),'GB24':(43,47.5),
       'GB25':(40,55),'GB26':(40.5,60),'GB27':(41,65),'GB28':(41.5,68.5),
       'GB29':(42,73),'GB30':(41.5,78)},
}
# 颈侧穴：Pose 鼻/耳/口/肩地标标定的颈部坐标系(人迎在喉结旁·气舍在颈根·天容在下颌角)
NECK = {'ST9':(48.5,27.0),'ST10':(48.2,29.0),'ST11':(48.0,31.2),
        'LI18':(47.0,27.0),'LI17':(46.3,28.6),
        'SI16':(45.8,26.3),'SI17':(46.0,24.2),'SJ16':(45.2,23.6)}

def windowed(z, coords, codes, base='front', pad_x=8, pad_top=4, pad_bot=5, minw=22, vessel=None):
    """Rebuild a crop zoom as a windowed zoom into the full `front`/`back` photo."""
    codes=[c for c in codes if c in coords]
    if not codes: return z
    xs=[coords[c][0] for c in codes]; ys=[coords[c][1] for c in codes]
    cx=(min(xs)+max(xs))/2
    w=max(max(xs)-min(xs)+pad_x*2, minw); h=(max(ys)-min(ys))+pad_top+pad_bot
    x0=round(cx-w/2,1); y0=round(min(ys)-pad_top,1)
    sc=sorted(codes, key=_num)
    if vessel is None:
        vessel='M'+' L'.join(f'{coords[c][0]},{coords[c][1]}' for c in sc)
    return {**z, 'img':base, 'imgH':150,
            'viewBox':f'{x0} {y0} {round(w,1)} {round(h,1)}', 'vessel':vessel,
            'points':[{'code':c,'x':coords[c][0],'y':coords[c][1]} for c in sc]}

def zoom_vessel(z):
    """Polyline through this zoom's points in numeric code order."""
    pts=sorted(z.get('points',[]), key=lambda p:_num(p['code']))
    if len(pts)<2: return z.get('vessel','')
    return 'M'+' L'.join(f"{p['x']},{p['y']}" for p in pts)

def _num(code):
    import re; m=re.search(r'(\d+)$',code); return int(m.group(1)) if m else 0

def windowed_leg(z, coords):
    """Rebuild a front_legfoot zoom as a windowed zoom into `front`."""
    codes=[p['code'] for p in z['points'] if p['code'] in coords]
    if not codes: return z
    xs=[coords[c][0] for c in codes]; ys=[coords[c][1] for c in codes]
    cx=(min(xs)+max(xs))/2
    w=max(max(xs)-min(xs)+13, 24); h=(max(ys)-min(ys))+9
    x0=round(cx-w/2,1); y0=round(min(ys)-4.5,1)
    codes.sort(key=_num)
    vessel='M'+' L'.join(f'{coords[c][0]},{coords[c][1]}' for c in codes)
    return {**z, 'img':'front', 'imgH':150,
            'viewBox':f'{x0} {y0} {round(w,1)} {round(h,1)}',
            'vessel':vessel,
            'points':[{'code':c,'x':coords[c][0],'y':coords[c][1]} for c in codes]}

def rebuild_vessel(G):
    """Polyline through on-figure points in numeric order (keeps points on line)."""
    pts=[(c,v) for c,v in G['coords'].items()
         if v.get('onMain',True) and v.get('x') is not None]
    pts.sort(key=lambda cv:_num(cv[0]))
    seq=[(v['x'],v['y']) for _,v in pts]
    if len(seq)<2: return
    mirror=lambda x: round(99-x,2)
    d='M'+' L'.join(f'{x},{y}' for x,y in seq)
    dm='M'+' L'.join(f'{mirror(x)},{y}' for x,y in seq)
    G.setdefault('overlay',{})
    G['overlay']['vessel']=d; G['overlay']['flow']=d
    if 'vesselFaint' in G['overlay']: G['overlay']['vesselFaint']=dm
    G['qi']={'vbw':100,'vbh':150,'path':[[x,y] for x,y in seq]}

def patch(key):
    gf=os.path.join(GEOM,key+'.py')
    G=runpy.run_path(gf)['G']
    body = MB if key=='bl' else MF
    changed=[]
    # 1) main-figure coords for landmark-placed body points (limbs + torso + 背俞)
    for c,v in G['coords'].items():
        src = body.get(c) or (TR.get(c) if key in TORSO_MERIDIANS else None) \
              or (BS.get(c) if key=='bl' else None)
        if src and v.get('x') is not None and v.get('onMain',True):
            v['x'],v['y']=src; changed.append(c)
    overrides=dict(CONNECTOR.get(key,{})); overrides.update({c:xy for c,xy in NECK.items() if c in G['coords']})
    for c,(x,y) in overrides.items():                      # 手工连接段 + 颈侧覆盖
        v=G['coords'].get(c)
        if v and v.get('x') is not None:
            v['x'],v['y']=float(x),float(y); changed.append(c)
    # 2) zooms
    newzoom=[]
    for z in G.get('zoom',[]):
        zc=[p['code'] for p in z.get('points',[])]
        if z.get('img')=='front_legfoot' and key in LEG_MERIDIANS:
            newzoom.append(windowed(z, MF, zc))
        elif z.get('img')=='front_torso' and key in TORSO_MERIDIANS:
            newzoom.append(windowed(z, TR, zc, pad_x=8, pad_top=4, pad_bot=4, minw=24))
        elif z.get('img')=='front_face' and key in FACE_MERIDIANS:
            for p in z['points']:
                if p['code'] in FC: p['x'],p['y']=FC[p['code']]
            newzoom.append(z)
        elif z.get('img')=='front_hand' and key in HAND_MERIDIANS:
            hit=False
            for p in z['points']:
                if p['code'] in FH: p['x'],p['y']=FH[p['code']]; hit=True
            if hit and z.get('vessel'): z['vessel']=zoom_vessel(z)
            newzoom.append(z)
        elif z.get('img')=='back_shu' and key=='bl':          # 背俞→窗口式 back，双线
            inner=[f'BL{i}' for i in range(11,36)]; outer=[f'BL{i}' for i in range(41,55)]
            vp=lambda cs:'M'+' L'.join(f'{BS[c][0]},{BS[c][1]}' for c in cs if c in BS)
            zc=[p['code'] for p in z['points']]
            newzoom.append(windowed(z, BS, zc, base='back', pad_x=10, pad_top=4, pad_bot=5,
                                    vessel=vp(inner)+' '+vp(outer)))
        else:
            newzoom.append(z)
    G['zoom']=newzoom
    # 3) vessel through updated points
    if key=='bl':
        d,dm=bl_vessel(G['coords'])
        G.setdefault('overlay',{}); G['overlay']['vessel']=d; G['overlay']['flow']=d
        if 'vesselFaint' in G['overlay']: G['overlay']['vesselFaint']=dm
    elif changed:
        rebuild_vessel(G)
    # write (back up once)
    bkf=os.path.join(BK,key+'.py')
    if not os.path.exists(bkf): shutil.copy(gf,bkf)
    with open(gf,'w',encoding='utf-8') as f:
        f.write('# geom + landmark-computed coords (apply_landmarks.py)\n')
        f.write('G='+repr(G)+'\n')
    print(f'patched {key:4s}: {len(changed)} main coords, zooms={[z.get("id") for z in newzoom]}')

def patch_mzoom(key):
    """Update the mzoom palm zoom (img=='hand') point coords from palm_hand()."""
    mf=os.path.join(MZOOM,key+'.py')
    if not os.path.exists(mf): return
    ns=runpy.run_path(mf)
    Z=ns.get('Z',[]); DROP=ns.get('DROP',[]); CLU=ns.get('CLUSTERS',[]); HIDE=ns.get('HIDE',[])
    hit=[]
    for z in Z:
        tbl = PH if z.get('img')=='hand' else (DH if z.get('img')=='dorsalhand' else None)
        if tbl:                                       # palm (hand.b64) or dorsum (dorsalhand.b64)
            zhit=[]
            for p in z['points']:
                if p['code'] in tbl: p['x'],p['y']=tbl[p['code']]; zhit.append(p['code'])
            if zhit and z.get('vessel'): z['vessel']=zoom_vessel(z)
            hit+=zhit
    if not hit: return
    bkf=os.path.join(BKM,key+'.py')
    if not os.path.exists(bkf): shutil.copy(mf,bkf)
    with open(mf,'w',encoding='utf-8') as f:
        f.write('# mzoom + landmark palm coords (apply_landmarks.py)\n')
        f.write('Z='+repr(Z)+'\nDROP='+repr(DROP)+'\nHIDE='+repr(HIDE)+'\nCLUSTERS='+repr(CLU)+'\n')
    print(f'  mzoom {key}: palm coords -> {hit}')

if __name__=='__main__':
    keys=sys.argv[1:] or ['st','sp','ki','gb','lr','li','si']
    for k in keys:
        patch(k)
        patch_mzoom(k)
