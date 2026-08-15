# 十二经"系统认知"数据 —— 五行/阴阳/六经/表里/相生母子/子午流注/季节情志五味五色五音。
# 每条经在整体系统中的坐标 + 养生逻辑链。build.py 合并进 M['system']，模板渲染「系统坐标」卡。
# 母子按五行相生(生我者为母、我生者为子)，指向该行代表脏的页面(便于虚补母/实泻子)。
F={  # key -> 页面文件名
 'lung':'手太阴肺经.html','li':'手阳明大肠经.html','st':'足阳明胃经.html','sp':'足太阴脾经.html',
 'ht':'手少阴心经.html','si':'手太阳小肠经.html','bl':'足太阳膀胱经.html','ki':'足少阴肾经.html',
 'pc':'手厥阴心包经.html','sj':'手少阳三焦经.html','gb':'足少阳胆经.html','lr':'足厥阴肝经.html'}

# 五行主题色(宣纸配色内的五色意象)
WX={'木':'#5c8a52','火':'#b23a2e','土':'#c9922b','金':'#b7a98f','水':'#3f6d86','相火':'#c0553f'}

F['ren']='任脉.html'; F['du']='督脉.html'
def L(k):  # {key,name,file} 引用
    N={'lung':'肺经','li':'大肠经','st':'胃经','sp':'脾经','ht':'心经','si':'小肠经',
       'bl':'膀胱经','ki':'肾经','pc':'心包经','sj':'三焦经','gb':'胆经','lr':'肝经',
       'ren':'任脉','du':'督脉'}
    return {'key':k,'name':N[k],'file':F[k]}

# 每经：element五行, phase脏/腑, yy阴/阳, six六经, limb手/足, organ, biao表里,
#        mother母(五行生我), child子(五行我生), prev/next流注, zhi时辰,
#        season季, emotion情志, taste五味, color五色, sound五音, liu六字诀,
#        logic养生逻辑一句(该经养生的"为什么")
SYS={
 'lung':dict(element='金',phase='脏',yy='阴',six='太阴',limb='手',organ='肺',
   biao=L('li'),mother=L('sp'),child=L('ki'),prev=L('lr'),nxt=L('li'),zhi='寅 3–5点',
   season='秋',emotion='悲·忧',taste='辛',color='白',sound='商',liu='呬 sī',
   logic='肺属金、应秋，秋燥最伤肺 → 润燥少辛、早卧早起；悲忧伤肺 → 宽胸调息；白色入肺 → 梨百合银耳；配呬字诀清肺、揉太渊补肺气。'),
 'li':dict(element='金',phase='腑',yy='阳',six='阳明',limb='手',organ='大肠',
   biao=L('lung'),mother=L('sp'),child=L('ki'),prev=L('lung'),nxt=L('st'),zhi='卯 5–7点',
   season='秋',emotion='悲·忧',taste='辛',color='白',sound='商',liu='呬 sī',
   logic='大肠与肺相表里、同属金 → 肺气肃降则大肠传导通畅。卯时当令 → 晨起一杯温水、按时排便；便秘/牙痛揉合谷，鼻塞按迎香。'),
 'st':dict(element='土',phase='腑',yy='阳',six='阳明',limb='足',organ='胃',
   biao=L('sp'),mother=L('ht'),child=L('lung'),prev=L('li'),nxt=L('sp'),zhi='辰 7–9点',
   season='长夏',emotion='思',taste='甘',color='黄',sound='宫',liu='呼 hū',
   logic='胃属土、主受纳，辰时当令 → 早餐要温热营养、最养气血；胃喜温怕生冷 → 定时定量细嚼慢咽；常揉足三里健脾和胃、强身。'),
 'sp':dict(element='土',phase='脏',yy='阴',six='太阴',limb='足',organ='脾',
   biao=L('st'),mother=L('ht'),child=L('lung'),prev=L('st'),nxt=L('ht'),zhi='巳 9–11点',
   season='长夏',emotion='思',taste='甘',color='黄',sound='宫',liu='呼 hū',
   logic='脾属土、主运化、统血，是气血生化之源。思虑过度伤脾 → 少操心；长夏湿困脾 → 少贪凉甜腻；健脾祛湿揉三阴交、公孙。'),
 'ht':dict(element='火',phase='脏',yy='阴',six='少阴',limb='手',organ='心',
   biao=L('si'),mother=L('lr'),child=L('sp'),prev=L('sp'),nxt=L('si'),zhi='午 11–13点',
   season='夏',emotion='喜',taste='苦',color='赤',sound='徵',liu='呵 hē',
   logic='心属火、主血脉藏神，午时当令 → 小憩养心（子午觉）；喜则气缓、过喜伤心 → 心平；夏养心 → 少熬夜、清心火，揉神门安神。'),
 'si':dict(element='火',phase='腑',yy='阳',six='太阳',limb='手',organ='小肠',
   biao=L('ht'),mother=L('lr'),child=L('sp'),prev=L('ht'),nxt=L('bl'),zhi='未 13–15点',
   season='夏',emotion='喜',taste='苦',color='赤',sound='徵',liu='呵 hē',
   logic='小肠与心相表里、主"受盛化物、泌别清浊"。未时当令 → 午饭营养、饭后别马上躺；心火可移热小肠 → 心烦尿黄时清心利小肠，落枕肩痛用后溪。'),
 'bl':dict(element='水',phase='腑',yy='阳',six='太阳',limb='足',organ='膀胱',
   biao=L('ki'),mother=L('lung'),child=L('lr'),prev=L('si'),nxt=L('ki'),zhi='申 15–17点',
   season='冬',emotion='恐',taste='咸',color='黑',sound='羽',liu='吹 chuī',
   logic='膀胱主一身之表、背部背俞连通五脏，申时当令 → 多喝水、下午办事效率高；受寒易感 → 护住颈背，"腰背委中求"，感冒揉风门。'),
 'ki':dict(element='水',phase='脏',yy='阴',six='少阴',limb='足',organ='肾',
   biao=L('bl'),mother=L('lung'),child=L('lr'),prev=L('bl'),nxt=L('pc'),zhi='酉 17–19点',
   season='冬',emotion='恐',taste='咸',color='黑',sound='羽',liu='吹 chuī',
   logic='肾属水、藏精、为先天之本，酉时当令 → 此时补肾最宜、宜静养；恐则伤肾 → 心安；冬藏 → 早睡、少耗精，揉太溪、涌泉滋肾。'),
 'pc':dict(element='相火',phase='脏',yy='阴',six='厥阴',limb='手',organ='心包',
   biao=L('sj'),mother=L('lr'),child=L('sp'),prev=L('ki'),nxt=L('sj'),zhi='戌 19–21点',
   season='—',emotion='喜',taste='苦',color='赤',sound='徵',liu='嘻 xī',
   logic='心包为"心之外卫"、代心受邪，戌时当令 → 晚饭后散步、放松愉悦护心；情志舒畅则心安，胸闷心悸揉内关（心包要穴）。'),
 'sj':dict(element='相火',phase='腑',yy='阳',six='少阳',limb='手',organ='三焦',
   biao=L('pc'),mother=L('lr'),child=L('sp'),prev=L('pc'),nxt=L('gb'),zhi='亥 21–23点',
   season='—',emotion='喜',taste='苦',color='赤',sound='徵',liu='嘻 xī',
   logic='三焦是全身气与水的大通道、总司气化。亥时当令 → 此时安睡、百脉修养（"亥子觉"最养元气）；睡前静心、勿扰，通调三焦揉外关、支沟。'),
 'gb':dict(element='木',phase='腑',yy='阳',six='少阳',limb='足',organ='胆',
   biao=L('lr'),mother=L('ki'),child=L('ht'),prev=L('sj'),nxt=L('lr'),zhi='子 23–1点',
   season='春',emotion='怒',taste='酸',color='青',sound='角',liu='嘘 xū',
   logic='胆主决断、"凡十一脏取决于胆"，子时当令 → 此时必须入睡、胆气得养（熬夜最伤胆气）；春宜生发 → 舒畅少怒，头侧痛揉风池。'),
 'lr':dict(element='木',phase='脏',yy='阴',six='厥阴',limb='足',organ='肝',
   biao=L('gb'),mother=L('ki'),child=L('ht'),prev=L('gb'),nxt=L('lung'),zhi='丑 1–3点',
   season='春',emotion='怒',taste='酸',color='青',sound='角',liu='嘘 xū',
   logic='肝属木、主疏泄藏血，丑时当令 → 此时熟睡、血归于肝而藏（"人卧血归肝"）；怒则伤肝 → 心平气和；春养肝 → 舒展情志，揉太冲疏肝解郁。'),
}

# ---- 奇经八脉之任督二脉(无五行/时辰/表里流注, 用阴阳配对) ----
QIJING={
 'ren':dict(qijing=True,name='任脉',nature='阴脉之海',yy='阴',color_hex='#4a7a6a',
   line='前正中线(胸腹)',gov='主胞胎 · 总任一身之阴',pair=L('du'),n='24',
   logic='任脉行于胸腹前正中，为"阴脉之海"，总领一身阴经、主胞胎生殖。养生重在温养小腹：常灸关元/气海培元固本、揉中脘和胃、按膻中宽胸理气；与督脉一阴一阳、共调周身。'),
 'du':dict(qijing=True,name='督脉',nature='阳脉之海',yy='阳',color_hex='#9c5a3a',
   line='后正中线(脊柱)→头面',gov='络脑通脊 · 总督一身之阳',pair=L('ren'),n='28',
   logic='督脉行于脊柱后正中、上头面，为"阳脉之海"，总督一身阳经、络脑通脊。养生重在护阳通督：晒背、捏脊、灸大椎/命门振奋阳气，揉百会提神醒脑；与任脉一阳一阴、共调周身。'),
}
def get(key):
    if key in QIJING: return dict(QIJING[key])
    s=SYS.get(key)
    if not s: return None
    s=dict(s); s['color_hex']=WX[s['element']]
    return s
