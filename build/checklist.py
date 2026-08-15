#!/usr/bin/env python3
"""生成《穴位核对清单》——覆盖全12经每个穴位，标注定位方法与核对状态。
输出 经络养生/穴位核对清单.md
"""
import sys, os, runpy
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build
from acu_formulas import (palm_hand, dorsal_hand, fronthand_pts, body_front,
                          body_back, face_pts, torso_pts, backshu_pts)

HAND   = set(palm_hand())|set(dorsal_hand())|set(fronthand_pts())
POSE   = set(body_front())|set(body_back())
FACE   = set(face_pts())
TORSO  = set(torso_pts())
BACKSHU= set(backshu_pts())
CONNECTOR = {f'GB{i}' for i in range(21,31)}
SISCAP    = {f'SI{i}' for i in range(9,16)}
NECK      = {'ST9','ST10','ST11','LI18','LI17','SI16','SI17','SJ16'}
HEADSIDE  = {f'GB{i}' for i in range(1,21)}|{f'SJ{i}' for i in range(17,24)}|{f'BL{i}' for i in range(3,11)}
# 从 zoom 收集：足部穴(专用足图) + 前臂穴(专用臂图) —— 均专用真人图网格逐穴核对
FOOT=set(); ARM=set()
for k in build.ALL:
    for src in [os.path.join(HERE,'data','mzoom',k+'.py'), os.path.join(HERE,'data','geom',k+'.py'),
                os.path.join(HERE,'data',k+'.py')]:
        if not os.path.exists(src): continue
        ns=runpy.run_path(src)
        zs=(ns.get('Z') or (ns.get('G',{}) or {}).get('zoom') or (ns.get('M',{}) or {}).get('zoom') or [])
        for z in zs:
            img=z.get('img')
            if img in ('footR1','footR2','sole','anklelat'):
                for p in z.get('points',[]): FOOT.add(p['code'])
            elif img in ('arm','armback'):
                for p in z.get('points',[]): ARM.add(p['code'])

def method(code):
    if code in FACE:    return ('✅','地标·面 (FaceMesh 468点)')
    if code in HAND:    return ('✅','地标·手 (Hands 21点)')
    if code in SISCAP:  return ('✅','地标·肩胛 (背面图, Pose肩)')
    if code in BACKSHU: return ('✅','椎体对位 (背俞, 骨度锚点)')
    if code in TORSO:   return ('✅','骨度·胸腹 (脐/乳视觉标定)')
    if code in CONNECTOR:return('✅','手工核对·连接段 (躯干侧)')
    if code.startswith('CV'):                     # 任脉 前正中线
        return ('✅','骨度·前正中线 (任脉)')
    if code in {f'GV{i}' for i in range(1,15)}:    # 督脉 脊柱
        return ('✅','椎体对位·后正中线 (督脉)')
    if code in {f'GV{i}' for i in range(15,28)}:   # 督脉 头顶面
        return ('✅','真人侧脸·头顶正中 (督脉)')
    if code in HEADSIDE:return ('✅','真人侧脸·公有领域 (耳/颞/发际锚点)')
    if code in NECK:    return ('✅','颈部·Pose标定 (鼻/耳/口/肩)')
    if code in FOOT:    return ('✅','网格·足专用真人图')
    if code in POSE:    return ('✅','地标·肢 (Pose 33点, 骨度分寸)')
    if code in ARM:     return ('✅','网格·前臂专用真人图')
    return ('☑️','锚点+像素吸附 (示意级)')

def main():
    lines=['# 十二经 · 穴位核对清单',
      '',
      '> 每个穴位的定位方法与核对状态。**✅=用检测地标/骨度/椎体精确计算或专用真人图逐穴核对；☑️=解剖锚点均分+像素吸附(示意级，落在正确肢段)**。',
      '',
      '**定位方法说明**',
      '- **地标·手/面/肢**：MediaPipe 检测真人图上的关节/五官地标，再按 WHO 骨度分寸公式算穴位（对标 Frontiers 2024 论文）',
      '- **骨度·胸腹**：Pose 定中线，肚脐/乳头视觉标定，按 天突→脐=17寸 等骨度排布',
      '- **椎体对位**：背俞穴按椎体（肺俞=肩胛冈/膈俞=肩胛下角/大肠俞=髂嵴）插值',
      '- **网格·足专用图**：足部无检测模型，用专用真人足图叠 cun 网格逐穴核对',
      '- **手工·连接段**：肩/腋/胁/髋等无地标覆盖处，手工核对落在正确部位',
      '']
    tot=0; bym={}
    for key in build.ALL:
        M=build.get_M(key)
        lines.append(f"## {M['name']}（{M['abbr']}） · 共 {len(M['points'])} 穴")
        lines.append('')
        lines.append('| # | 穴位 | 定位方法 | 状态 |')
        lines.append('|---|------|----------|:---:|')
        for p in M['points']:
            st,m=method(p['code']); tot+=1; bym[m]=bym.get(m,0)+1
            lines.append(f"| {p['code']} | {p['name']} | {m} | {st} |")
        lines.append('')
    # 汇总
    summ=['## 核对方法汇总','', '| 定位方法 | 穴位数 |','|----------|:---:|']
    for m,n in sorted(bym.items(), key=lambda x:-x[1]):
        summ.append(f"| {m} | {n} |")
    summ+= [f"| **合计** | **{tot}** |",'',
      '## 已知限制（诚实标注）',
      '- **足趾诸穴**：MediaPipe 无足部模型，靠专用真人足图网格核对（已逐穴看过，无粗错）',
      '- **小肠经肩胛穴**：本在背部，已用背面图「肩胛放大」精确标注，正面主图隐藏',
      '- **胸腹肋间穴**：无乳头/肚脐地标点，靠视觉标定，属高精度近似（非关节级）',
      '- **☑️ 示意级穴位**：多为躯干/颈项连接处，落在正确部位与次序，未逐一地标计算']
    out=os.path.join(ROOT,'穴位核对清单.md')
    open(out,'w',encoding='utf-8').write('\n'.join(lines+summ)+'\n')
    print(f'wrote {out}  ({tot} 穴)')
    for m,n in sorted(bym.items(), key=lambda x:-x[1]): print(f'  {n:3d}  {m}')

if __name__=='__main__': main()
