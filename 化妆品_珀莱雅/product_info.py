import requests,re

def get_proya_info():
    rsp = requests.get("https://www.proya.com/about")
    rsp.encoding = "utf-8"
    data = rsp.text
    proya_info = re.search('<div class="txtBox">.+?<div class="footerBox">',data,flags=re.S).group()
    proya_info = re.findall('<div class="txt">(.+?)</div>',proya_info,re.S)[0].replace("<br>","").replace("   ","\n")
    return proya_info

def get_product_channel_list(channel_list):       
    rsp = requests.get("https://www.proya.com" + channel_list)
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.search('<ul class="f-cb" id="ListItem">(.+?)<div class="loading"></div>',data,flags=re.S).group()
    pd = re.findall('<a href="(.+?)" class="shop"><span>查看更多</span></a>',wb,re.M)
    return pd

def get_product_channel():
    channel_list = []
    rsp = requests.get("https://www.proya.com")
    rsp.encoding = "utf-8"
    data = rsp.text
    hf = re.search('class="tits">护肤<i>.+?系列分类',data,flags=re.S).group()
    hf = re.search('>产品分类</a></dt>.+?</dl>',hf,re.S).group()
    hf = re.findall('<a href="(.+?)"',hf,re.S)
    for i in hf:
        channel_list.append(i)

    mm = re.search('class="tits">面膜<i>.+?</dl>',data,flags=re.S).group()
    mm = re.search('系列.+?</dl>',mm,flags=re.S).group()
    mm = re.findall('<a href="(.+?)"',mm,re.S)
    for j in mm:
        channel_list.append(j)

    cz = re.search('class="tits">彩妆<i></i></a>.+?</div>',data,flags=re.S).group()
    cz = re.findall('<dd><a href="(.+?)">.+?</a></dd>',cz,re.S)
    for k in cz:
        channel_list.append(k)

    xh = re.search('卸妆液</a></dd>.+?<div class="mnav none" style="display:none;">',data,flags=re.S).group()
    xh = re.findall('<a href="(.+?)" class="tits">洗护</a>',xh)
    for l in xh:
        channel_list.append(l)

    ns = re.search('class="tits">男士<i></i></a>.+?</div>',data,flags=re.S).group()
    ns = re.search('产品分类</a></dt>.+?<dl>',ns,flags=re.S).group()
    ns = re.findall('<dd><a href="(.+?)">.+?</a></dd>',ns)
    for m in ns:
        channel_list.append(m)
    return channel_list
#print(len(get_product_channel_list()))
#print(get_product_channel())
def get_product_info(product_data):
    print(product_data)
    rsp = requests.get("https://www.proya.com" + product_data)
    rsp.encoding = "utf-8"
    data = rsp.text
    info = re.search('<div class="table t2">(.+?)<div class="footerBox">',data,flags=re.S).group()
    name = re.findall('class="tits">(.+?)</h1>',info,re.M)[0]
    tit = re.findall('<div class="tit">(.+?)</div>',info,re.M)
    tit = tit[0]
    price = re.findall('<div class="price f-cb"><span>价格：</span><i>(.+?)</i></div>',info,re.M)[0]
    size = re.search('<span>规格：</span>.+?</a>',info,re.S).group()
    size = re.findall('class=\'on\'>(.+?)</a>',size)
    size = size[0]
    try:
        product_info = re.search('<div class="txt">.+?</div>',info,re.S).group()
        product_info = re.search('<p.+?</p>',product_info,re.S).group().replace("&nbsp",'').replace("<br />",'').replace('<p>','').replace("</p>",'').strip()
    except:
        product_info = "无"
    try:
        product_use = re.search('<div class="picList">.+?</div>',info,re.S).group()
        product_use = re.search('<p>.+?</p>',product_use,re.S).group().replace("<br />",'').replace('<p>','').replace("</p>",'').strip()
    except:
        product_use = "无"    
    with open("product_info.txt",'a',encoding="utf-8") as w:
        w.write("产品名字："+name+"\n"+"产品简介："+tit+"\n"+"产品价格："+price+"\n"+"产品规格："+size+"\n"+"产品说明："+product_info+"\n"+"使用方法："+product_use+"\n")
        w.write("\n-------------------------------------------------\n")


with open("product_info.txt",'a',encoding="utf-8") as w:
    w.write("珀莱雅品牌简介：\n"+get_proya_info()+"\n"+"\n-------------------------------------------------\n")
for x in get_product_channel():
    for y in get_product_channel_list(x):
        get_product_info(y)
