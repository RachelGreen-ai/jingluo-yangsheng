#!/usr/bin/env python3
"""Landmark-driven acupoint locator.

Instead of eyeballing acupoint pixels, we detect anatomical landmarks with
MediaPipe (Hands 21 / Pose 33 / Face 468) on the exact base64 image embedded in
each atlas page, then compute each acupoint as a WHO bone-proportional (骨度分寸,
cun) formula relative to those landmarks.  This mirrors the method in
Frontiers 2024 "Real-time location of acupuncture points based on anatomical
landmarks and pose estimation models".

Coordinates are emitted in the atlas viewBox space: x in [0,100] = image width,
y = landmark_y * viewBoxHeight (verified: every embedded image's aspect ratio
equals its viewBox height, so this is exact).

Pipeline:  detect -> cache landmarks (json) -> apply formulas -> coords.
"""
import base64, io, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A      = os.path.join(ROOT, 'build', 'assets')
CACHE  = os.path.join(ROOT, 'build', 'data', 'landmarks')
os.makedirs(CACHE, exist_ok=True)
MODELS = {'hand':'/tmp/hand_landmarker.task',
          'pose':'/tmp/pose_landmarker.task',
          'face':'/tmp/face_landmarker.task'}
CJK = '/System/Library/Fonts/STHeiti Medium.ttc'

# viewBox height per asset (== implied aspect, verified)
VBH = {'front':150,'back':150,'hand':157,'dorsalhand':157.8,
       'footR2':182.8,'footR1':74.3,'anklelat':67.6,'sole':163.5,
       'arm':196.8,'armback':238.1,'front_face':100,
       'front_torso':191.9,'front_legfoot':116.6,'front_hand':114.5,
       'back_shu':181.3,'back_foot':139.1}

def load_asset(key):
    raw = base64.b64decode(open(os.path.join(A, key+'.b64')).read().strip())
    return Image.open(io.BytesIO(raw)).convert('RGB')

def _detect(key, kind, min_conf=0.2):
    im  = load_asset(key); W,H = im.size
    img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(im))
    if kind == 'hand':
        opt = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=MODELS['hand']),
            num_hands=1, min_hand_detection_confidence=min_conf)
        with vision.HandLandmarker.create_from_options(opt) as d:
            r = d.detect(img)
        if not r.hand_landmarks: return None
        lms = r.hand_landmarks[0]
        handed = r.handedness[0][0].category_name if r.handedness else '?'
        meta = {'handedness': handed}
    elif kind == 'pose':
        opt = vision.PoseLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=MODELS['pose']),
            num_poses=1, min_pose_detection_confidence=min_conf)
        with vision.PoseLandmarker.create_from_options(opt) as d:
            r = d.detect(img)
        if not r.pose_landmarks: return None
        lms = r.pose_landmarks[0]; meta = {}
    elif kind == 'face':
        opt = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=MODELS['face']),
            num_faces=1)
        with vision.FaceLandmarker.create_from_options(opt) as d:
            r = d.detect(img)
        if not r.face_landmarks: return None
        lms = r.face_landmarks[0]; meta = {}
    pts = [[round(l.x,5), round(l.y,5), round(getattr(l,'z',0),5)] for l in lms]
    return {'key':key,'kind':kind,'W':W,'H':H,'vbh':VBH.get(key),'n':len(pts),
            'landmarks':pts, **meta}

def get_landmarks(key, kind, refresh=False):
    cf = os.path.join(CACHE, key+'.json')
    if os.path.exists(cf) and not refresh:
        return json.load(open(cf))
    d = _detect(key, kind)
    if d is None:
        print(f'!! no {kind} detected in {key}'); return None
    json.dump(d, open(cf,'w'), ensure_ascii=False)
    print(f'detected {kind:4s} {key:12s} {d["n"]:3d} landmarks  {d.get("handedness","")}')
    return d

# ---- viewBox-space landmark accessor -------------------------------------
class LM:
    """Landmarks in atlas viewBox coords: x in [0,100], y in [0,vbh]."""
    def __init__(self, d):
        self.vbh = d['vbh']
        self.P = np.array([[p[0]*100, p[1]*self.vbh] for p in d['landmarks']])
        self.meta = d
    def __call__(self, i):        return self.P[i].copy()
    def blend(self, i, j, t):     return self.P[i]*(1-t) + self.P[j]*t
    def mid(self, i, j):          return self.blend(i, j, 0.5)

# ---- skeleton render (for eyeballing landmark quality) -------------------
def render_skeleton(key, kind, out):
    d = get_landmarks(key, kind, refresh=True)
    if d is None: return
    im = load_asset(key).copy(); W,H = im.size
    dr = ImageDraw.Draw(im)
    try: fnt = ImageFont.truetype(CJK, max(10, W//45))
    except: fnt = ImageFont.load_default()
    for i,(x,y,_z) in enumerate(d['landmarks']):
        px,py = x*W, y*H
        r = 4 if kind!='face' else 1
        dr.ellipse([px-r,py-r,px+r,py+r], fill=(220,40,40))
        if kind!='face':
            dr.text((px+5,py-6), str(i), fill=(10,60,200), font=fnt)
    im.save(out, quality=88)
    print(f'skeleton -> {out}  ({kind} on {key})')

if __name__ == '__main__':
    import sys
    jobs = sys.argv[1:] or ['front:pose','back:pose']
    for j in jobs:
        key,kind = j.split(':')
        render_skeleton(key, kind, f'/tmp/skel_{key}.jpg')
