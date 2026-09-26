#!/usr/bin/env python3
# Meridian atlas page builder.
# Each meridian = content (text) + geom (coordinates on the photo), merged into one M.
# Lung is a standalone combined file (data/lung.py). Others: data/content/<key>.py (C)
# + data/geom/<key>.py (G) merged by code.
# Usage: python3 build/build.py all   |   python3 build/build.py li st ...
import json, re, sys, os, runpy

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 经络养生/
BUILD = os.path.join(ROOT, 'build')
sys.path.insert(0, os.path.join(BUILD, 'data', 'geom'))  # for _util.place

def load_img(key):
    return "data:image/jpeg;base64," + open(os.path.join(BUILD,'assets',key+'.b64')).read().strip()

def merge(C, G):
    M = dict(C)
    for k in ('img','viewBox','qi','overlay','zoom','clockZhi'):
        if k in G: M[k] = G[k]
    coords = G.get('coords', {})
    for p in M['points']:
        c = coords.get(p['code'])
        if not c:
            p['onMain'] = False; p['x'] = None; p['y'] = None; continue
        p['x'] = c.get('x'); p['y'] = c.get('y')
        if c.get('k'): p['k'] = 1
        if c.get('lab'): p['lab'] = c['lab']
        p['onMain'] = c.get('onMain', True)
    return M

def apply_mzoom(M, key):
    """Overlay hand-verified dedicated-photo zooms (build/data/mzoom/<key>.py)."""
    mf = os.path.join(BUILD,'data','mzoom',key+'.py')
    if not os.path.exists(mf): return M
    ns = runpy.run_path(mf)
    Z = ns.get('Z',[]); DROP=set(ns.get('DROP',[])); CLU=ns.get('CLUSTERS',[]); HIDE=set(ns.get('HIDE',[]))
    byc={p['code']:p for p in M['points']}
    for code in HIDE:                        # approximate on main -> hide, keep only in dedicated zoom + list
        if code in byc: byc[code]['onMain']=False; byc[code].pop('k',None)
    M.setdefault('zoom',[])
    z_codes={zp['code'] for z in Z for zp in z.get('points',[])}
    dropped_codes={zp['code'] for z in M['zoom'] if z['id'] in DROP for zp in z.get('points',[])}
    for code in z_codes:                     # shown in dedicated zoom -> no main label
        if code in byc: byc[code].pop('k',None)
    for code in dropped_codes - z_codes:     # was in a dropped auto-zoom, not re-zoomed -> label on main
        p=byc.get(code)
        if p and p.get('onMain',True): p['k']=1
    M['zoom']=[z for z in M['zoom'] if z['id'] not in DROP]+Z
    ov=M.setdefault('overlay',{})
    cl=[c for c in ov.get('clusters',[]) if c.get('zoom') not in DROP]
    ov['clusters']=cl+CLU
    return M


FRONT_CROPS = {
    'front_hand': (14, 58, 42, 90),
    'front_face': (36, 3, 58, 25),
    'front_headside': (37, 3, 51, 23),
    'front_earhead': (38, 8, 52, 22),
    'front_torso': (34, 26, 58, 72),
    'front_legfoot': (33, 99, 57, 127),
}


def remap_front_point(x, y):
    """Map original 100x150 front-photo coordinates to the repaired image."""
    px, py = x * 8.2, y * 8.2
    center = 410.0
    if py <= 218:
        out_y, scale = py - 8, 0.94
    elif py < 250:
        out_y = 210 + (py - 218) * 40 / 32
        scale = 0.94 + 0.06 * ((out_y - 210) / 40)
    else:
        out_y, scale = py, 1.0
    out_x = center + (px - center) * scale
    return round(out_x / 8.2, 2), round(out_y / 8.2, 2)


def remap_path(path):
    if not path:
        return path

    def repl(match):
        x, y = remap_front_point(float(match.group(1)), float(match.group(2)))
        return f'{x:g},{y:g}'

    return re.sub(r'(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)', repl, path)


def reproject_front(M):
    """Keep rendered points aligned with the deterministic head/neck image warp."""
    if M.get('img') != 'front':
        return M

    original_points = {
        p.get('code'): (p.get('x'), p.get('y'))
        for p in M.get('points', [])
        if p.get('x') is not None and p.get('y') is not None
    }
    for p in M.get('points', []):
        if p.get('x') is not None and p.get('y') is not None:
            p['x'], p['y'] = remap_front_point(p['x'], p['y'])

    qi = M.get('qi', {})
    if 'path' in qi:
        qi['path'] = [list(remap_front_point(x, y)) for x, y in qi['path']]

    overlay = M.get('overlay', {})
    for key in ('vessel', 'flow', 'vesselFaint'):
        if key in overlay:
            overlay[key] = remap_path(overlay[key])
    for cluster in overlay.get('clusters', []):
        cluster['x'], cluster['y'] = remap_front_point(cluster['x'], cluster['y'])

    for zoom in M.get('zoom', []):
        if zoom.get('img') == 'front':
            for point in zoom.get('points', []):
                if point.get('x') is not None and point.get('y') is not None:
                    point['x'], point['y'] = remap_front_point(point['x'], point['y'])
            zoom['vessel'] = remap_path(zoom.get('vessel'))
        elif zoom.get('img') in FRONT_CROPS:
            x0, y0, x1, y1 = FRONT_CROPS[zoom['img']]
            for point in zoom.get('points', []):
                original = original_points.get(point.get('code'))
                if not original:
                    continue
                gx, gy = remap_front_point(*original)
                point['x'] = round((gx - x0) / (x1 - x0) * 100, 2)
                point['y'] = round((gy - y0) / (y1 - y0) * 100, 2)
            if zoom.get('points'):
                zoom['vessel'] = 'M' + ' L'.join(
                    f"{p['x']:g},{p['y']:g}" for p in zoom['points']
                )
    return M

def get_M(key):
    combined = os.path.join(BUILD,'data',key+'.py')
    cfile = os.path.join(BUILD,'data','content',key+'.py')
    gfile = os.path.join(BUILD,'data','geom',key+'.py')
    if os.path.exists(cfile) and os.path.exists(gfile):
        C = runpy.run_path(cfile)['C']
        G = runpy.run_path(gfile)['G']
        M = merge(C, G)
    else:
        M = runpy.run_path(combined)['M']
    sysmod = runpy.run_path(os.path.join(BUILD,'data','system.py'))
    M['system'] = sysmod['get'](key)          # 系统坐标数据
    return reproject_front(apply_mzoom(M, key))

def build(key):
    M = get_M(key)
    imgs = {M['img']} | {z['img'] for z in M.get('zoom', []) if 'img' in z}
    IMGS = {k: load_img(k) for k in imgs}
    css  = open(os.path.join(BUILD,'assets','style.css'), encoding='utf-8').read()
    body = open(os.path.join(BUILD,'template_body.html'), encoding='utf-8').read()
    body = body.replace('/*__IMGS__*/', json.dumps(IMGS, ensure_ascii=False))
    body = body.replace('/*__DATA__*/', json.dumps(M, ensure_ascii=False))
    head = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s · 经络养生</title>\n<style>%s</style>\n</head>\n' % (M['name'], css))
    out = os.path.join(ROOT, M['name'] + '.html')
    open(out,'w',encoding='utf-8').write(head + body)
    npts = sum(1 for p in M['points'] if p.get('x') is not None)
    print('built %-5s -> %-10s %3dKB  %d pts (%d on figure)' % (key, M['name'], os.path.getsize(out)//1024, len(M['points']), npts))

ALL = ['lung','li','st','sp','ht','si','bl','ki','pc','sj','gb','lr','ren','du']
if __name__ == '__main__':
    keys = sys.argv[1:] or ['lung']
    if keys == ['all']: keys = ALL
    for k in keys: build(k)
