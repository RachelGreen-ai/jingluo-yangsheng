#!/usr/bin/env python3
# Meridian atlas page builder.
# Each meridian = content (text) + geom (coordinates on the photo), merged into one M.
# Lung is a standalone combined file (data/lung.py). Others: data/content/<key>.py (C)
# + data/geom/<key>.py (G) merged by code.
# Usage: python3 build/build.py all   |   python3 build/build.py li st ...
import json, sys, os, runpy

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
    return apply_mzoom(M, key)

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
