#!/usr/bin/env python3
"""Acupoint formulas as WHO bone-proportional (骨度分寸) functions of MediaPipe
landmarks.  Each region returns {code:(x,y)} in atlas viewBox coords.

骨度 standards used:
  upper arm  腋前纹→肘横纹      = 9寸   (shoulder→elbow landmark ~acromion→elbow)
  forearm    肘横纹→腕横纹      = 12寸  (elbow→wrist)
  thigh      股骨大转子→腘/膝   = 19寸  (hip→knee)
  lower leg  膝中(犊鼻)→外踝    = 16寸  (knee→ankle)
  medial leg 胫骨内侧髁→内踝    = 13寸
  post thigh 臀横纹→腘横纹      = 14寸
"""
import numpy as np, json, os
from landmark_acu import LM, get_landmarks

def _seg(a, b, t):        # point t of the way from a to b
    return a*(1-t) + b*t

# ---------------------------------------------------------------- FRONT body
def body_front():
    d = get_landmarks('front','pose'); L = LM(d)
    sh,el,wr = L(12), L(14), L(16)          # person's right arm (our left, x<50)
    hip,kn,an = L(24), L(26), L(28)         # person's right leg
    # unit vectors / lateral sign: for our-left leg, lateral(outer)=toward x-, medial=toward x+
    LATx = -1.0   # add LATx*n for lateral
    out = {}
    # ---- Stomach (front of leg, lateral to tibia) ----
    out['ST31'] = tuple(_seg(hip,kn,0.02) + [0,1])           # 髀关 inguinal
    out['ST32'] = tuple(_seg(kn,hip,6/19))                    # 伏兔 膝上6寸
    out['ST33'] = tuple(_seg(kn,hip,3/19))                    # 阴市 膝上3寸
    out['ST34'] = tuple(_seg(kn,hip,2/19) + [LATx*0.6,0])     # 梁丘 膝上2寸 外
    out['ST35'] = tuple(kn + [LATx*0.8, 1.6])                # 犊鼻 外膝眼
    out['ST36'] = tuple(_seg(kn,an,3/16) + [LATx*1.0,0])     # 足三里 犊鼻下3寸
    out['ST37'] = tuple(_seg(kn,an,6/16) + [LATx*1.0,0])     # 上巨虚 下6寸
    out['ST38'] = tuple(_seg(kn,an,8/16) + [LATx*1.0,0])     # 条口 下8寸
    out['ST39'] = tuple(_seg(kn,an,9/16) + [LATx*1.0,0])     # 下巨虚 下9寸
    out['ST40'] = tuple(_seg(kn,an,8/16) + [LATx*2.2,0])     # 丰隆 外侧
    out['ST41'] = tuple(_seg(an,kn,0.10))                    # 解溪 踝前
    # ---- Spleen (medial leg, medial to tibia) ----
    MEDx = +1.0
    out['SP10'] = tuple(_seg(kn,hip,2/19) + [MEDx*2.2,0])    # 血海 膝内上2寸
    out['SP9']  = tuple(kn + [MEDx*2.6, 3.0])               # 阴陵泉 胫骨内侧髁下
    out['SP8']  = tuple(_seg(kn,an,5/16) + [MEDx*2.4,0])    # 地机
    out['SP7']  = tuple(_seg(an,kn,6/13) + [MEDx*2.2,0])    # 漏谷 内踝上6寸
    out['SP6']  = tuple(_seg(an,kn,3/13) + [MEDx*2.0,0])    # 三阴交 内踝上3寸
    out['SP5']  = tuple(an + [MEDx*2.4, -1.5])              # 商丘 内踝前下
    # ---- Liver (between SP and midline, medial) ----
    out['LR9']  = tuple(_seg(kn,hip,4/19) + [MEDx*3.0,0])  # 阴包 膝上4寸
    out['LR8']  = tuple(kn + [MEDx*3.2, 0.2])              # 曲泉 膝内侧横纹端
    out['LR7']  = tuple(kn + [MEDx*2.6, 2.2])              # 膝关 阴陵泉后
    out['LR6']  = tuple(_seg(an,kn,7/13) + [MEDx*1.2,0])   # 中都 内踝上7寸(胫骨内侧)
    out['LR5']  = tuple(_seg(an,kn,5/13) + [MEDx*1.2,0])   # 蠡沟 内踝上5寸(胫骨内侧)
    out['LR4']  = tuple(an + [MEDx*1.4, -2.0])             # 中封 内踝前
    # ---- Gallbladder (lateral thigh/leg) ----
    out['GB31'] = tuple(_seg(kn,hip,7/19) + [LATx*2.6,0])  # 风市 膝上7寸 外
    out['GB32'] = tuple(_seg(kn,hip,5/19) + [LATx*2.6,0])  # 中渎
    out['GB33'] = tuple(kn + [LATx*2.6,-1.0])             # 膝阳关
    out['GB34'] = tuple(kn + [LATx*2.4, 3.4])            # 阳陵泉 腓骨头前下
    out['GB35'] = tuple(_seg(kn,an,7/16) + [LATx*2.8,0]) # 阳交
    out['GB36'] = tuple(_seg(kn,an,7/16) + [LATx*3.4,0]) # 外丘
    out['GB37'] = tuple(_seg(an,kn,5/16) + [LATx*2.8,0]) # 光明 外踝上5寸
    out['GB38'] = tuple(_seg(an,kn,4/16) + [LATx*2.8,0]) # 阳辅 外踝上4寸
    out['GB39'] = tuple(_seg(an,kn,3/16) + [LATx*2.6,0]) # 悬钟 外踝上3寸
    # ---- Kidney (medial, lower) ----
    out['KI10'] = tuple(kn + [MEDx*3.6, 0.5])            # 阴谷 膝内后
    out['KI9']  = tuple(_seg(an,kn,5/13) + [MEDx*2.6,0]) # 筑宾 内踝上5寸
    out['KI8']  = tuple(_seg(an,kn,2/13) + [MEDx*1.5,0]) # 交信 内踝上2寸(复溜前)
    out['KI7']  = tuple(_seg(an,kn,2/13) + [MEDx*2.4,0]) # 复溜 内踝上2寸
    out['KI3']  = tuple(an + [MEDx*2.2, -0.5])           # 太溪 内踝后
    out['KI6']  = tuple(an + [MEDx*2.0, 1.5])            # 照海 内踝下
    # ---- arm elbow points (cubital crease) ----
    out['LU5'] = tuple(el + [LATx*1.2, 0.2])            # 尺泽 肘横纹桡侧
    out['LI11']= tuple(el + [LATx*2.0, -0.5])           # 曲池 肘横纹外端
    out['PC3'] = tuple(el + [0, 0.3])                   # 曲泽 肘横纹中
    out['HT3'] = tuple(el + [MEDx*2.0, 0.2])            # 少海 肘横纹内端
    # ---- shoulder (肩峰周围, Pose 肩关节) ----
    out['LI15']= tuple(sh + [-0.5, 1.6])                # 肩髃 肩峰前下
    out['LI16']= tuple(sh + [1.6, -2.0])                # 巨骨 锁骨肩胛冈叉间
    out['SJ14']= tuple(sh + [-1.6, 2.6])                # 肩髎 肩峰后下
    out['SJ15']= tuple(sh + [3.0, -2.4])                # 天髎 肩胛上角(斜方肌)
    # ---- 肝经上股/腹股沟 + 脾经股内 (Pose 髋膝内侧) ----
    out['SP11']= tuple(_seg(kn,hip,8/19) + [MEDx*2.6,0])# 箕门 血海上6寸(股内)
    out['LR12']= tuple(hip + [MEDx*2.3, 0.5])           # 急脉 腹股沟(耻骨结节旁)
    out['LR11']= tuple(hip + [MEDx*2.6, 3.0])           # 阴廉 气冲下2寸
    out['LR10']= tuple(hip + [MEDx*2.6, 6.0])           # 足五里 气冲下3寸
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- BACK body
def body_back():
    d = get_landmarks('back','pose'); L = LM(d)
    # atlas draws BL on our-left leg (x~43) -> use person's left-side landmarks (odd)
    sh,el,wr = L(11), L(13), L(15)
    hip,kn,an,heel = L(23), L(25), L(27), L(29)
    out = {}
    # ---- Bladder (back midline is spine; leg line lateral) ----
    out['BL36'] = tuple(hip + [0, 2.0])                 # 承扶 臀横纹中
    out['BL37'] = tuple(_seg(hip,kn,6/14))              # 殷门 承扶下6寸
    out['BL40'] = tuple(kn + [0,0.5])                   # 委中 腘横纹中
    out['BL39'] = tuple(kn + [2.0,0.5])                 # 委阳 外侧
    out['BL55'] = tuple(_seg(kn,an,2/16))              # 合阳
    out['BL56'] = tuple(_seg(kn,an,5/16))              # 承筋 合阳承山之间
    out['BL57'] = tuple(_seg(kn,an,8/16))              # 承山 腓肠肌下
    out['BL58'] = tuple(_seg(kn,an,9/16)+[-2.0,0])     # 飞扬
    out['BL38'] = tuple(kn+[2.0,-2.2])                 # 浮郄 委阳上1寸
    out['BL60'] = tuple(_seg(an,heel,0.4)+[-2.0,0])    # 昆仑 外踝后
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- BACK-SHU (back.b64, 膀胱经背俞穴 按椎体定位)
def backshu_pts():
    """BL11-54 + 八髎/会阳，按椎体连续编号 + 解剖锚点(肺俞=肩胛冈/膈俞=肩胛下角/大肠俞=髂嵴)插值。
    内线1.5寸、外线3寸旁开脊柱；八髎在骶后孔近正中。返回 back frame 坐标。"""
    ANCH=[(1,32),(3,37),(7,47),(16,70),(19,78),(22,82)]   # (椎idx, y)
    def yv(idx):
        for k in range(len(ANCH)-1):
            i0,y0=ANCH[k]; i1,y1=ANCH[k+1]
            if idx<=i1: return y0+(y1-y0)*(idx-i0)/(i1-i0)
        return ANCH[-1][1]
    spine=49.5; INN=spine-3; OUT=spine-6; B8=spine-1.2
    INNER={11:1,12:2,13:3,14:4,15:5,16:6,17:7,18:9,19:10,20:11,21:12,22:13,
           23:14,24:15,25:16,26:17,27:18,28:19,29:20,30:21}
    OUTER={41:2,42:3,43:4,44:5,45:6,46:7,47:9,48:10,49:11,50:12,51:13,52:14,53:19,54:21}
    BALIAO={31:18,32:19,33:20,34:21}
    out={}
    for c,i in INNER.items():  out[f'BL{c}']=(INN, round(yv(i),2))
    for c,i in OUTER.items():  out[f'BL{c}']=(OUT, round(yv(i),2))
    for c,i in BALIAO.items(): out[f'BL{c}']=(B8,  round(yv(i),2))
    out['BL35']=(B8, round(yv(22),2))           # 会阳 尾骨旁
    return {k:(float(v[0]),float(v[1])) for k,v in out.items()}

# ---------------------------------------------------------------- FACE
def face_pts():
    d = get_landmarks('front_face','face'); L = LM(d)
    # person's-right side (our left, nearer/fuller because face turns to his left)
    eyeIn, eyeOut, iris = L(133), L(33), L(468)
    ala, mouth, noseT   = L(98), L(61), L(1)
    brow, ear, chin     = L(105), L(234), L(152)
    P = np.array
    out = {}
    out['BL1']  = tuple(eyeIn + [0.6,-0.6])                 # 睛明 内眦上
    out['BL2']  = tuple([eyeIn[0], brow[1]+1.0])            # 攒竹 眉头
    out['ST1']  = tuple([iris[0], iris[1]+3.2])             # 承泣 瞳孔下眶
    out['ST2']  = tuple([iris[0], iris[1]+5.6])             # 四白 承泣下
    out['ST3']  = tuple([iris[0], ala[1]])                 # 巨髎 平鼻翼
    out['ST4']  = tuple([iris[0], mouth[1]-0.4])           # 地仓 口角旁
    out['ST7']  = tuple(ear + [3.2,1.2])                   # 下关 颧弓下
    out['ST6']  = tuple(_seg(ear,chin,0.42) + [1.5,0])     # 颊车 下颌角前
    out['ST5']  = tuple(_seg(ear,chin,0.5) + [4.5,0])      # 大迎 下颌角前下
    out['ST8']  = tuple([eyeOut[0]-1.0, brow[1]-8.5])      # 头维 额角发际
    out['LI20'] = tuple(ala + [-1.2,0.2])                  # 迎香 鼻翼旁
    out['LI19'] = tuple(ala + [-0.6,3.2])                  # 口禾髎 鼻孔下·近人中
    out['GB1']  = tuple(eyeOut + [-1.6,0.2])               # 瞳子髎 外眦旁
    out['SI18'] = tuple([eyeOut[0], iris[1]+8.5])          # 颧髎 外眦直下颧下
    out['SI19'] = tuple(ear + [0.4,0.5])                   # 听宫 耳屏前
    out['SJ21'] = tuple(ear + [0.4,-2.4])                  # 耳门 耳屏上
    out['SJ23'] = tuple(eyeOut + [0.4,-7.5])               # 丝竹空 眉梢
    out['GB14'] = tuple([iris[0], brow[1]-3.0])            # 阳白 眉上1寸
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- TORSO (front.b64, chest+abdomen)
# 骨度: 天突→脐=17寸(竖直), 两乳头间=8寸(水平); 脐位由真人图肚脐视觉标定.
# 胸部按肋间较密(CVc), 腹部按脐相对(CV). 线旁开: 肾0.5/胃2/脾4寸.
def torso_pts():
    d = get_landmarks('front','pose'); L = LM(d)
    midx = (L(11)[0]+L(12)[0]+L(23)[0]+L(24)[0])/4    # trunk midline ~51.7
    navel_y = 63.6; tiantu_y = 37.7
    CV = (navel_y-tiantu_y)/17.0                        # abdomen cun (vertical)
    CVc = 1.2; CH = 2.05                                # chest cun / horizontal cun
    ab = lambda lat,below: (round(midx-lat*CH,2), round(navel_y+below*CV,2))   # navel-relative
    ch = lambda lat,cun:   (round(midx-lat*CH,2), round(tiantu_y+cun*CVc,2))   # 天突-relative
    out = {}
    out.update({'ST12':ch(4,-0.5),'ST13':ch(4,1.5),'ST14':ch(4,3),'ST15':ch(4,4.5),'ST16':ch(4,5.7),
                'ST17':ch(4,6.8),'ST18':ch(4,8),
                'ST19':ab(2,-6),'ST20':ab(2,-5),'ST21':ab(2,-4),'ST22':ab(2,-3),'ST23':ab(2,-2),
                'ST24':ab(2,-1),'ST25':ab(2,0),'ST26':ab(2,1),'ST27':ab(2,2),'ST28':ab(2,3),
                'ST29':ab(2,4),'ST30':ab(2,5)})
    out.update({'SP12':ab(3.5,5),'SP13':ab(4,4.3),'SP14':ab(4,1.3),'SP15':ab(4,0),'SP16':ab(4,-3),
                'SP17':ch(6,6.8),'SP18':ch(6,5.7),'SP19':ch(6,4.5),'SP20':ch(6,3),'SP21':ch(6.5,8)})
    out.update({'KI11':ab(0.5,5),'KI12':ab(0.5,4),'KI13':ab(0.5,3),'KI14':ab(0.5,2),'KI15':ab(0.5,1),
                'KI16':ab(0.5,0),'KI17':ab(0.5,-2),'KI18':ab(0.5,-3),'KI19':ab(0.5,-4),'KI20':ab(0.5,-5),
                'KI21':ab(0.5,-6),'KI22':ch(2,6.8),'KI23':ch(2,5.7),'KI24':ch(2,4.5),'KI25':ch(2,3),
                'KI26':ch(2,1.5),'KI27':ch(2,0)})
    # 胸胁散点: 心包天池(乳旁1寸)、肝经期门(乳下)/章门(胁11肋端)
    out.update({'PC1':ch(5,6.8), 'LR14':ch(4,8.4), 'LR13':ab(6,-4.5)})
    return {k:(float(v[0]),float(v[1])) for k,v in out.items()}

# ---------------------------------------------------------------- PALM (hand.b64, right hand, palm-up, fingers up)
def palm_hand():
    d = get_landmarks('hand','hand'); L = LM(d)
    W = L(0)                                   # wrist
    def tip(t,dip,dx):                         # beyond fingertip + radial/ulnar nudge
        return L(t)+(L(t)-L(dip))*0.10+np.array([dx,0.0])
    out = {
      # lung
      'LU9':  np.array([W[0]+0.75*(L(1)[0]-W[0]), W[1]-4]),   # 太渊 桡侧腕横纹
      'LU10': L.blend(1,2,0.5)+[2,0],                         # 鱼际 第1掌骨中点
      'LU11': L(4)+(L(4)-L(3))*0.15,                          # 少商 拇指桡侧甲角
      # fingertip 井穴 (thumb at +x; index radial=+x, pinky ulnar=-x)
      'LI1':  tip(8,7,+1.2),    # 商阳 index radial
      'PC9':  tip(12,11,0.0),   # 中冲 middle
      'SJ1':  tip(16,15,-1.2),  # 关冲 ring ulnar
      'HT9':  tip(20,19,+1.0),  # 少冲 pinky radial
      'SI1':  tip(20,19,-1.2),  # 少泽 pinky ulnar
      # small-intestine ulnar border (visible on palm photo's pinky edge)
      'SI2':  L(17)+(L(20)-L(17))*0.25+[-2.5,0],   # 前谷 掌指关节前尺侧
      'SI3':  L(17)+(L(0)-L(17))*0.10+[-3.0,0],    # 后溪 掌指关节后尺侧(掌纹头)
      'SI4':  L(17)+(L(0)-L(17))*0.45+[-3.0,0],    # 腕骨 第5掌骨底尺侧
      'SI5':  L(0)+(L(17)-L(0))*0.12+[-2.0,0],     # 阳谷 腕横纹尺侧
      # palm / wrist
      'PC8':  L.blend(9,0,0.35),                                  # 劳宫 掌心
      'HT8':  L.blend(13,17,0.5)+(W-L.blend(13,17,0.5))*0.28,     # 少府 尺侧掌
      'PC7':  np.array([W[0]+2, W[1]-4]),                         # 大陵 腕横纹中
      'HT7':  np.array([W[0]+(L(17)[0]-W[0])*0.22, W[1]-3]),      # 神门 腕横纹尺侧
    }
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- DORSUM (dorsalhand.b64, left hand, dorsal; ulnar side cropped)
def dorsal_hand():
    d = get_landmarks('dorsalhand','hand'); L = LM(d)
    bl = L.blend
    out = {
      'LI4': bl(2,5,0.5)+[0,3],                 # 合谷 虎口(1-2掌骨间)
      'LI5': bl(0,1,0.62)+[-1,2],               # 阳溪 桡侧腕(鼻烟窝)
      'LI3': L(5)+(L(0)-L(5))*0.18+[-3,0],      # 三间 2掌骨桡侧后
      'LI2': L(5)+(L(8)-L(5))*0.16+[-3,0],      # 二间 2掌骨桡侧前
      'SJ4': L(0)+(bl(9,13,0.5)-L(0))*0.16,     # 阳池 腕背中(对4指)
      'SJ3': bl(13,17,0.5)+[0,-7],              # 中渚 4-5掌骨间
      'SJ2': bl(13,17,0.5)+[0,4],               # 液门 4-5指蹼
    }
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- FRONT_HAND (palm crop, right hand, diagonal)
def fronthand_pts():
    d = get_landmarks('front_hand','hand'); L = LM(d)
    def tip(t,dip,dx):  # just beyond fingertip along finger axis + radial/ulnar nudge
        v = L(t)+(L(t)-L(dip))*0.10+np.array([dx,0.0]); return v
    out = {
      'LI1': tip(8,7,-1.0),    # 商阳 index radial nail
      'PC9': tip(12,11,0.0),   # 中冲 middle tip
      'SJ1': tip(16,15,1.0),   # 关冲 ring ulnar nail
      'HT9': tip(20,19,-1.0),  # 少冲 pinky radial nail
      'SI1': tip(20,19,1.2),   # 少泽 pinky ulnar nail
      'LI4': L.blend(2,5,0.5)+[-0.5,-2.0],   # 合谷 1-2掌骨间(虎口)
      'PC8': L.blend(9,0,0.3),               # 劳宫 掌心
      'HT8': L.blend(13,17,0.5)+ (L(0)-L.blend(13,17,0.5))*0.25,  # 少府 尺侧掌
    }
    return {k:(float(round(v[0],2)),float(round(v[1],2))) for k,v in out.items()}

# ---------------------------------------------------------------- render
def _render(key, kind, coords, out):
    from PIL import Image, ImageDraw, ImageFont
    from landmark_acu import load_asset, CJK
    im = load_asset(key).copy(); W,H = im.size
    vbh = LM(get_landmarks(key,kind)).vbh
    dr = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(CJK, max(11, W//55))
    for code,(x,y) in coords.items():
        px,py = x/100*W, y/vbh*H
        dr.ellipse([px-3,py-3,px+3,py+3], fill=(178,58,46))
        dr.text((px+5,py-7), code, fill=(20,40,160), font=fnt)
    im.save(out, quality=90); print('render ->', out, f'({len(coords)} pts)')

if __name__ == '__main__':
    _render('front','pose', body_front(), '/tmp/acu_front.jpg')
    _render('back','pose',  body_back(),  '/tmp/acu_back.jpg')
    _render('front_face','face', face_pts(), '/tmp/acu_face.jpg')
