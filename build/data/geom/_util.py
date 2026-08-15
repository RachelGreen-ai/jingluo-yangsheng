# Geometry helpers: distribute acupoints along an anatomical polyline by arc-length.
import math

def _cum(wp):
    d=[0.0]
    for i in range(1,len(wp)):
        d.append(d[-1]+math.hypot(wp[i][0]-wp[i-1][0], wp[i][1]-wp[i-1][1]))
    return d

def at(wp, t):
    """point at fraction t (0..1) of the polyline by arc length"""
    d=_cum(wp); total=d[-1]
    if total==0: return (wp[0][0], wp[0][1])
    target=t*total
    for i in range(1,len(wp)):
        if d[i]>=target:
            seg=d[i]-d[i-1]; f=0 if seg==0 else (target-d[i-1])/seg
            return (round(wp[i-1][0]+(wp[i][0]-wp[i-1][0])*f,2),
                    round(wp[i-1][1]+(wp[i][1]-wp[i-1][1])*f,2))
    return (wp[-1][0], wp[-1][1])

def place(wp, codes, fracs=None, key=(), onMain=True, offset=(0,0)):
    """Return {code:{x,y,k,onMain}}. Even arc-length spacing unless fracs given."""
    n=len(codes); out={}
    if fracs is None:
        fracs=[0.0] if n==1 else [i/(n-1) for i in range(n)]
    for c,t in zip(codes,fracs):
        x,y=at(wp,t)
        d={'x':round(x+offset[0],2),'y':round(y+offset[1],2),'onMain':onMain}
        if c in key: d['k']=1
        out[c]=d
    return out

def pts(d):
    """dict {code:(x,y)} -> {code:{x,y,onMain}}"""
    return {c:{'x':xy[0],'y':xy[1],'onMain':True} for c,xy in d.items()}

def mirror(x): return round(99-x,2)

def place_anchored(anchors, codes, key=(), onMain=True):
    """anchors: [(code,x,y),...] a subset of codes (must include first & last);
    intervening codes are distributed evenly by index between consecutive anchors."""
    idx={c:i for i,c in enumerate(codes)}
    A=sorted(anchors, key=lambda a: idx[a[0]])
    out={}
    # clamp head/tail to nearest anchor if first/last not anchored
    if idx[A[0][0]]>0:  A=[(codes[0],A[0][1],A[0][2])]+A
    if idx[A[-1][0]]<len(codes)-1: A=A+[(codes[-1],A[-1][1],A[-1][2])]
    for j in range(len(A)-1):
        c0,x0,y0=A[j]; c1,x1,y1=A[j+1]; i0=idx[c0]; i1=idx[c1]
        span=i1-i0
        for i in range(i0, i1+1):
            f=(i-i0)/span if span else 0
            c=codes[i]
            out[c]={'x':round(x0+(x1-x0)*f,2),'y':round(y0+(y1-y0)*f,2),'onMain':onMain}
            if c in key: out[c]['k']=1
    return out

def dpath(anchors):
    """anchors [(code,x,y),...] in order -> SVG polyline 'M..L..' string"""
    ps=[(a[1],a[2]) for a in anchors]
    return 'M'+' L'.join('%g,%g'%(x,y) for x,y in ps)

def dpath_mirror(anchors):
    ps=[(mirror(a[1]),a[2]) for a in anchors]
    return 'M'+' L'.join('%g,%g'%(x,y) for x,y in ps)

def qipath(anchors):
    return [[a[1],a[2]] for a in anchors]
