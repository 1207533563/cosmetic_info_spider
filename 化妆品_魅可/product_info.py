import requests,re

def get_macco_info():
    rsp = requests.get("https://www.maccosmetics.com.cn/our-story")
    rsp.encoding = "utf-8"
    data = rsp.text
    macco_info1 = re.search('<div class="content-4col__content"> <h5>什么成就了魅可</h5>.+?</section>',data,flags=re.S).group()
    macco_info2 = re.search('<div class="content-4col__content"> <h5>信仰的诞生：从惊叹的开始到现在！</h5>.+?</section>',data,flags=re.S).group()
    macco_info3 = re.search('<section class="content-4col__column content-4col__column--4 grid--item">.+?</section>',data,flags=re.S).group()
    macco_info1 = re.search('<p>(.+)</p>',macco_info1,re.S).group().replace("<p>","").replace("<strong>","").replace("</strong>","").replace("</p>","").strip()
    macco_info2 = re.search('<p>(.+)</p>',macco_info2,re.S).group().replace("<p>","").replace("<strong>","").replace("</strong>","").replace("</p>","").strip()
    macco_info3 = re.search('<p>(.+)</p>',macco_info3,re.S).group().replace("<p>","").replace("<strong>","").replace("</strong>","").replace("</p>","").replace("&nbsp;","").strip()
    return macco_info1 +"\n"+ macco_info2 +"\n"+ macco_info3

def get_product_channel():       
    rsp = requests.get("https://www.maccosmetics.com.cn")
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.search('眼部<div class="menu-container depth-3">(.+?)<a href="/bestsellers">热卖产品',data,flags=re.S).group()
    pd = re.findall('<a href="(/products.+?)">',wb,re.M)
    return pd




def get_product_channel_list(get_product_channel):
    product_list = []       
    rsp = requests.get("https://www.maccosmetics.com.cn"+get_product_channel)
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.findall('<div class="product_header_details">(.+?)<h3 class="product__subline">',data,flags=re.S)
    for i in wb:
        product_list.append(re.findall('href="(.+?)"',i))
    #pd = re.findall('<a href="(/products.+?)">',wb,re.M)
    if "#" in product_list:
        product_list.remove("#")
    return product_list

def get_product_info(product_data):
    print(product_data)
    try:
        rsp = requests.get("https://www.maccosmetics.com.cn" + product_data)
        rsp.encoding = "utf-8"
        data = rsp.text
        try:
            color = re.search('<div class="product__shade-column">(.+?)<div class="btn btn--big btn--full shade-picker__trigger-btn js-shade-picker__trigger">预览颜色</div>',data,re.S).group()
            color_url = re.findall('<div class="shade-picker__color-texture" data-bg-image="(.+?)" style=".+?"></div>',color)
            color_name = re.findall('<div class="shade-picker__color-chip js-shade-check--bg" style="background-color: .+?" title="(.+?)"></div>',color)
            color_info = []
            for colors in range(len(color_url)):
                color_info.append((color_name[colors],"https://www.maccosmetics.com.cn" + color_url[colors]))           
        except:
            pass
        
        info = re.search('<div class="product__detail">(.+?)<a class="product__add-to-bag',data,flags=re.S).group()
        name = re.findall('<h3 class="product__subline">(.+?)</h3>',info,re.M)[0]
        try:
            tit = re.findall('<div class="product__description-short product_rgn_name_below_subline">(.+?)</div>',info,re.M)[0]
        except:
            tit = "暂无"
        price = re.search('<footer class="product__footer">',data,re.S).group()
        price = re.findall('<span class="product__price--standard">(.+?)</span>',data)[0]

        product = re.search('<div class="product__description-column">(.*?)</header>',info,re.S).group()

        try:
            product_info = re.findall('<div class="product__description-group-body" id="expandable1">(.*?)</div>',info,re.S)[0]
        except:
            product_info = "暂无"
        try:
            product_use = re.search('使用方法</h4>(.+?)</li></ul></div>',product,re.S).group()
            product_use = re.search('<ul>(.+?)</div>',product_use,re.S).group().replace("<li>","").replace("</li>","").replace("<ul>","").replace("</ul>","").replace("</div>","").strip()
        except:
            product_use = "暂无"
        with open("product_info.txt",'a',encoding="utf-8") as w:
            w.write("产品名字："+name+"\n"+"产品标题："+tit+"\n"+"产品颜色："+str(color_info)+"\n"+"产品价格："+price+"\n"+"产品说明："+product_info+"\n"+"使用方法："+product_use+"\n")
            w.write("\n-------------------------------------------------\n")
    except:
        pass
 

with open("product_info.txt",'a',encoding="utf-8") as w:
    w.write("魅可品牌简介：\n"+get_macco_info()+"\n"+"\n-------------------------------------------------\n")
for i in get_product_channel():
    for x in get_product_channel_list(i):
        for y in x:
            get_product_info(y)

#print(get_product_info("/product/13853/40610/versicolour-stain#/shade/Forever%2C_Darling"))