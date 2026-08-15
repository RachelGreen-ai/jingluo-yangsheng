# 胆经足部(专用图) + 头侧真人图(公有领域·爱迪生侧脸, 手工按解剖锚点标温部/耳周/枕部诸穴)
GBH=[('GB1',33,50),('GB2',62,60),('GB3',60,54),('GB4',49,38),('GB5',51,43),('GB6',53,47),
     ('GB7',59,45),('GB8',62,35),('GB9',68,33),('GB10',72,45),('GB11',74,54),('GB12',73,64),
     ('GB13',43,26),('GB14',34,40),('GB15',41,29),('GB16',48,23),('GB17',55,20),('GB18',63,20),
     ('GB19',78,37),('GB20',80,54)]
_HV='M'+' L'.join('%g,%g'%(x,y) for _,x,y in GBH)
Z=[{'id':'head','chip':'⊕ 头侧放大','title':'头侧 · 瞳子髎→风池','sub':'公有领域真人侧脸(爱迪生, PD)· 按耳/颞/发际解剖锚点标注',
    'viewBox':'0 0 100 99.8','img':'headside','vessel':_HV,
    'points':[{'code':c,'x':x,'y':y} for (c,x,y) in GBH]},
   {'id':'ftD','chip':'⊕ 足背放大','title':'足背 · 临泣·侠溪·窍阴','sub':'真人足背图（Wikimedia, 公有领域）',
    'viewBox':'0 0 100 182.8','img':'footR2','vessel':'M56,62 L58,55 L61,49 L63,39',
    'points':[{'code':'GB41','x':56,'y':62},{'code':'GB42','x':58,'y':55},{'code':'GB43','x':61,'y':49},{'code':'GB44','x':63,'y':39}]},
   {'id':'ankL','chip':'⊕ 外踝放大','title':'外踝 · 丘墟·悬钟','sub':'真人外踝图（Wikimedia, 公有领域）',
    'viewBox':'0 0 100 67.6','img':'anklelat','vessel':'M71,12 L67,46',
    'points':[{'code':'GB40','x':67,'y':46},{'code':'GB39','x':71,'y':12}]}]
DROP=['head']   # 删掉 geom 里的 front_headside 头zoom，换成上面公有领域真人侧脸
HIDE=[c for (c,_,_) in GBH]
CLUSTERS=[{'x':43,'y':13,'label':'头','zoom':'head'},{'x':43,'y':134,'label':'足','zoom':'ftD'},{'x':44,'y':125,'label':'踝','zoom':'ankL'}]
