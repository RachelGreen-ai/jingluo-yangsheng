# 经络内容撰写规范（供子任务使用）

你在为一套《黄帝内经·经络养生》交互网页撰写**某几条经络的文字内容**。读者是**中老年养生爱好者（用户和她妈妈）**，请用**准确、温和、生活化的大白话中文**。这是给普通人自我保健用的科普，不是医学教材。

## 你的产出
对分配给你的**每一条经络**，用 **Write** 生成一个文件：
`/Users/junyis/Desktop/personal/读书学习/经络养生/build/data/content/<key>.py`
文件内容是一个可被 Python `runpy` 加载的模块，只定义一个字典 `C`（**只写文字内容，不要写任何坐标/几何**——坐标由主控负责）。

**重要**：先用 Read 打开参考样板 `/Users/junyis/Desktop/personal/读书学习/经络养生/build/data/lung.py`，严格模仿它的**字段结构、语气、白话风格、HTML 标记用法**（`<b>`、`<br>`、用"——"解释、口诀等）。你的 `C` 就是把 lung.py 里除坐标外的所有字段照搬结构、换成你这条经络的内容。

## C 的字段结构（逐字段照 lung.py）
```python
C = {
 'key':'li','abbr':'LI','name':'手阳明大肠经','en':'Large Intestine · LI',
 'subtitle':'五行属<b>金</b> · <b>卯时</b>（5–7点）当令 · 与肺相表里 · 从手走头',
 'clockZhi':'卯',
 'intro':{
   'dirTitle':'经络走向 · 从手走头',
   'flowtext':'...一段白话走向，关键处 <b>加粗</b>；起止穴加粗...',
   'quote':'...补充说明（内行段/支脉/交接下一经），可用 <br>...',
   'badges':['方向：<b>从手 → 头</b>','当令：<b>卯时 5–7点</b>','共 <b>20</b> 穴（每侧）','五行：<b>金</b>'],
   'organTitle':'大肠是一个怎样的"腑"',    # 脏/腑一句话画像标题
   'organLead':'读懂这几句，就懂了为什么这条经能管这么多事——',
   'organ':['<b>要点</b>：白话解释。', ...],   # 6–8 条脏腑生理要点（含表里、五行应季、开窍、在志等）
   'pointsTitle':'20 个穴位 · 从食指到鼻旁',
   'flowNav':{'lead':'<b>卯时（5–7点）大肠经当令</b>，...一句流注说明...',
              'prev':'手太阴肺经（寅时）','next':'足阳明胃经（辰时）','nextFile':'足阳明胃经.html'},
 },
 'disease':{
   'title':'病候 · 大肠经不通会怎样','lead':'《灵枢·经脉》把这条经的毛病分两类，下面是大白话版。',
   'blocks':[{'h3':'一、是动病（经络气机堵了）','p':'...白话...'},
             {'h3':'二、所生病（本腑/相关功能失调）','p':'...白话，可用 <br> 分层...'}],
   'symptoms':[{'label':'牙痛 · 面痛','pts':['LI4','LI7']}, ...],   # 6–8 组常见症状→常用穴 code
 },
 'care':{
   'shi':{'title':'卯时（5–7点）大肠经当令','big':'卯时 · 晨起排便',
          'text':'...白话，这个时辰该做什么、异常提示什么...'},
   'blocks':[
     {'h2':'日常保健 · 人人可做','html':'<h3>小标题</h3><p class="lead">...</p><h3>应季/食疗</h3>','food':['...','...']},
     {'h2':'六字诀与循经保健','html':'<h3>六字诀 · "..."</h3><p class="lead">...</p><h3>循经保健 · 每天几分钟</h3><ul class="list-clean"><li>...</li>...</ul>'},
   ],
   'disclaimer':'温馨提示：本页为传统养生科普...（照 lung.py 改写，保留就医与咨询医师的提醒；涉及放血/艾灸等专业操作只提示"请医师操作"）',
 },
 'points':[
   {'code':'LI1','n':1,'name':'商阳','py':'Shāngyáng','type':['井穴·金'],'region':'finger-index-nail',
    'locate':'...在自己身上怎么找，1–2句白话...',
    'indic':'...它管什么，1–2句白话...',
    'care':'...怎么自己保健按摩，1–2句白话...'},
   ... 该经全部穴位，按经络走向从起点到终点顺序，n 从 1 递增 ...
 ],
}
```

## 准确性要求（重要）
- **穴位数目、名称、拼音、国际代码（LU/LI/ST/SP/HT/SI/BL/KI/PC/SJ/GB/LR + 序号）、顺序**必须与标准针灸学教材一致，不得漏穴或错序。三焦经代码用 **SJ**，心包用 **PC**。
- **定位**用 WHO/教科书标准，但翻成"在自己身上怎么摸"的大白话（可提"几寸""横指""某骨某筋旁的凹陷"）。
- **特定穴**在 `type` 里标注（如 `['原穴']`、`['络穴']`、`['郄穴']`、`['合穴·土','下合穴']`、`['背俞穴']`、`['八会穴·筋会']`、`['八脉交会穴·通督脉']`、`['募穴']` 等）；无则 `type:[]`。
- **主治**给该穴最常用、最有代表性的几项（大白话），别堆砌。
- **保健**只写**安全的自我按摩/艾灸提示/拍打**；放血、深刺等**写"请由专业医师操作"**。
- 每个字段**1–2 句**即可，简洁清楚；穴多的经（胃45、膀胱67、胆44）尤其保持简洁，但每穴三字段都要有。

## region 标签（帮主控在真人图上定位，务必给准）
每穴给一个 `region` 英文标签，从下表选最贴切的：
- 头面颈：`face` `forehead` `eye-inner` `eye-outer` `nose-side` `mouth-side` `cheek` `jaw` `ear-front` `ear` `head-side` `head-top` `head-back` `neck-front` `neck-side` `neck-back` `nape`
- 躯干前：`chest` `chest-lat` `epigastric` `abdomen` `lower-abdomen` `flank` `rib-side` `groin`
- 躯干后：`scapula` `back-upper` `back-mid` `back-low` `lumbar` `sacrum` `buttock`
- 上肢：`shoulder` `upper-arm-inner` `upper-arm-outer` `elbow-inner` `elbow-outer` `forearm-inner` `forearm-outer` `wrist-palm` `wrist-dorsum` `hand-palm` `hand-dorsum` `finger-thumb` `finger-index` `finger-index-nail` `finger-middle` `finger-ring` `finger-little` `finger-little-nail`
- 下肢：`hip` `thigh-front` `thigh-med` `thigh-lat` `thigh-back` `knee-front` `knee-med` `knee-lat` `knee-back` `shin` `leg-med` `leg-lat` `leg-back` `ankle-front` `ankle-med` `ankle-lat` `ankle-back` `foot-dorsum` `foot-sole` `toe-big` `toe-big-nail` `toe-2` `toe-4` `toe-4-nail` `toe-little`

## 格式硬性要求
- 文件**只含** `C = { ... }`，纯 Python 字面量；布尔用 `True/False`，空值 `None`。
- 字符串里如含英文单引号，请用双引号包字符串或转义，确保 `runpy` 能加载（写完可自查是否合法 Python）。
- 不要写 x/y/坐标/SVG 路径/图片/zoom——**只写文字**。
- 完成后简要报告：每条经写了多少穴、文件路径。
