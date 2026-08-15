#!/usr/bin/env python3
"""生成任脉(ren)/督脉(du)的 geom —— 复用胸腹骨度(前正中)/椎体(脊柱)/爱迪生侧脸(头顶)/五官。
任脉=前正中线(front); 督脉=脊柱(back)+头面(headside)。"""
import os
HERE=os.path.dirname(os.path.abspath(__file__))

def poly(seq): return 'M'+' L'.join(f'{x},{y}' for x,y in seq)

# ---------------- 任脉 CV (front 前正中线, x=51.5) ----------------
midx=51.5; navel=63.6; tiantu=37.7; CVc=1.2; cun=(navel-tiantu)/17
ab=lambda b:(midx, round(navel+b*cun,1)); ch=lambda c:(midx, round(tiantu+c*CVc,1))
CV={'CV1':(midx,83.0),'CV2':(midx,72.0),'CV3':ab(4),'CV4':ab(3),'CV5':ab(2),'CV6':ab(1.5),
 'CV7':ab(1),'CV8':ab(0),'CV9':ab(-1),'CV10':ab(-2),'CV11':ab(-3),'CV12':ab(-4),'CV13':ab(-5),
 'CV14':ab(-6),'CV15':ab(-7),'CV16':(midx,51.5),'CV17':ch(6.8),'CV18':ch(5.6),'CV19':ch(4.3),
 'CV20':ch(3),'CV21':ch(1),'CV22':ch(0),'CV23':(midx,29.0),'CV24':(midx,24.5)}
CV_key={'CV4','CV6','CV8','CV12','CV17','CV22'}   # 关元/气海/神阙/中脘/膻中/天突

def build_ren():
    order=[f'CV{i}' for i in range(1,25)]
    coords={}
    for c in order:
        x,y=CV[c]; d={'x':x,'y':y,'onMain':True}
        if c in CV_key: d['k']=1
        coords[c]=d
    seq=[CV[c] for c in order]
    vessel=poly(seq)
    # 胸腹正中放大: 窗口式 front, CV2-22
    zc=[f'CV{i}' for i in range(2,23)]
    zx=[CV[c][0] for c in zc]; zy=[CV[c][1] for c in zc]
    w=max(zx)-min(zx)+18; h=max(zy)-min(zy)+8; x0=round((min(zx)+max(zx))/2-w/2,1); y0=round(min(zy)-4,1)
    zoom=[{'id':'trunk','chip':'⊕ 胸腹正中放大','title':'任脉 · 胸腹诸穴','sub':'前正中线放大（真人图 CC0）· 骨度分寸',
           'viewBox':f'{x0} {y0} {round(w,1)} {round(h,1)}','img':'front','imgH':150,
           'vessel':poly([CV[c] for c in zc]),
           'points':[{'code':c,'x':CV[c][0],'y':CV[c][1]} for c in zc]}]
    G={'img':'front','viewBox':'0 0 100 150','qi':{'vbw':100,'vbh':150,'path':[[x,y] for x,y in seq]},
       'overlay':{'vessel':vessel,'flow':vessel,'clusters':[{'x':midx+3,'y':60,'label':'腹','zoom':'trunk'}]},
       'coords':coords,'zoom':zoom}
    return G

# ---------------- 督脉 GV (back 脊柱 + headside 头面) ----------------
SPINE={'GV1':(49.5,84.0),'GV2':(49.5,82.0),'GV3':(49.5,70.0),'GV4':(49.5,64.9),'GV5':(49.5,62.3),
 'GV6':(49.5,58.1),'GV7':(49.5,55.3),'GV8':(49.5,52.6),'GV9':(49.5,47.0),'GV10':(49.5,44.5),
 'GV11':(49.5,42.0),'GV12':(49.5,37.0),'GV13':(49.5,32.0),'GV14':(49.5,30.0)}
HEAD={'GV15':(84,48),'GV16':(83,38),'GV17':(78,25),'GV18':(67,15),'GV19':(61,13),'GV20':(55,12),
 'GV21':(49,16),'GV22':(44,20),'GV23':(40,24),'GV24':(37,28),'GV25':(17,64),'GV26':(21,75),'GV27':(22,79)}
GV_key={'GV4','GV9','GV14','GV20','GV26'}   # 命门/至阳/大椎/百会/水沟

def build_du():
    order=[f'GV{i}' for i in range(1,29)]
    coords={}
    for c in order:
        if c in SPINE: x,y=SPINE[c]; om=True
        else: x,y=SPINE['GV14']; om=False    # 头面穴主图隐藏(在头zoom看), 占位坐标
        d={'x':x,'y':y,'onMain':om}
        if c in GV_key and om: d['k']=1
        coords[c]=d
    seq=[SPINE[c] for c in [f'GV{i}' for i in range(1,15)]]
    vessel=poly(seq)
    # 脊背放大: 窗口式 back GV1-14
    zx=[p[0] for p in SPINE.values()]; zy=[p[1] for p in SPINE.values()]
    w=max(zx)-min(zx)+18; h=max(zy)-min(zy)+8; x0=round((min(zx)+max(zx))/2-w/2,1); y0=round(min(zy)-4,1)
    hv=poly([HEAD[f'GV{i}'] for i in range(15,28)])
    zoom=[{'id':'spine','chip':'⊕ 脊背正中放大','title':'督脉 · 脊柱诸穴','sub':'后正中线放大（真人图 CC0）· 椎体对位',
           'viewBox':f'{x0} {y0} {round(w,1)} {round(h,1)}','img':'back','imgH':150,
           'vessel':vessel,'points':[{'code':c,'x':SPINE[c][0],'y':SPINE[c][1]} for c in SPINE]},
          {'id':'head','chip':'⊕ 头顶·面放大','title':'督脉 · 百会→水沟','sub':'公有领域真人侧脸(爱迪生, PD)· 头顶正中诸穴',
           'viewBox':'0 0 100 99.8','img':'headside','vessel':hv,
           'points':[{'code':c,'x':HEAD[c][0],'y':HEAD[c][1]} for c in HEAD]}]
    G={'img':'back','viewBox':'0 0 100 150','qi':{'vbw':100,'vbh':150,'path':[[x,y] for x,y in seq]},
       'overlay':{'vessel':vessel,'flow':vessel,'clusters':[{'x':49.5,'y':22,'label':'头','zoom':'head'},{'x':52,'y':55,'label':'脊','zoom':'spine'}]},
       'coords':coords,'zoom':zoom}
    return G

if __name__=='__main__':
    for key,G in [('ren',build_ren()),('du',build_du())]:
        out=os.path.join(HERE,'data','geom',key+'.py')
        with open(out,'w',encoding='utf-8') as f:
            f.write('# 任督奇经 geom — 复用骨度/椎体/侧脸模型 (gen_renDu.py)\n')
            f.write('G='+repr(G)+'\n')
        print(f'wrote {key} geom: {len(G["coords"])} pts, zooms={[z["id"] for z in G["zoom"]]}')
