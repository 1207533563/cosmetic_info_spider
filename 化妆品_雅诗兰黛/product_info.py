import requests,re

def get_macco_info():
    rsp = requests.get("https://www.esteelauder.com.cn/")
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
    rsp = requests.get("https://www.esteelauder.com.cn")
    rsp.encoding = "utf-8"
    data = rsp.text
    hf = re.search('<span class="menu__item-trigger js-nav-link-trigger">产品类型</span>(.+?)</div>',data,flags=re.S).group()
    hf = re.findall('href="(/products.+?)">',hf,re.M)

    cz = re.search('<span class="menu__item-trigger js-nav-link-trigger">底妆</span>(.+?)<a class="menu__item-trigger js-nav-link-trigger" href="/products/647">唇釉&唇彩</a>',data,flags=re.S).group()
    cz = re.findall('href="(/products.+?)">',cz,re.M)

    xf = re.findall('<h3 class="menu-ref__title"><span class="menu-ref__title-wrap"><a href="(/products.+?)" class="menu-ref__link">香氛</a></span></h3>',data,re.M)
    product_channel = hf + cz  + xf

    # rsp = requests.get("https://www.esteelauder.com.cn/re-nutriv#/landing")
    # rsp.encoding = "utf-8"
    # data = rsp.text
    # bj = re.search('<dt>类别</dt>(.+?)</div>',data,re.S).group()
    # bj = re.findall('<a href="(.+?)" title',bj,re.M)

    return product_channel




def get_product_channel_list(get_product_channel):
    product_list = []       
    rsp = requests.get("https://www.esteelauder.com.cn"+get_product_channel)
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.findall('<div class="product_brief__headers">(.+?)<h3',data,flags=re.S)
    for i in wb:
        product_list.append(re.findall('href="(.+?)"',i)[0])
    return product_list

def get_product_info(product_data):
    print(product_data)
    rsp = requests.get("https://www.esteelauder.com.cn" + product_data)
    rsp.encoding = "utf-8"
    data = rsp.text
    
    color = re.findall('<div itemprop="color" itemscope itemtype="http://schema.org/ProductColor">(.+?)</div>',data,re.S)
    color_url = []
    color_name = []
    color_info = []
    for i in range(len(color)):
        color_url.append(re.findall('content="(https:.+?)" />',color[i],re.M)[0])#.replace("el_sku","el_smoosh").replace("_0",""))
        color_name.append(re.findall('color" content="(.+?)" />',color[i],re.M)[0])           
    for colors in range(len(color_url)):
        color_info.append((color_name[colors],color_url[colors]))           
    # except:
    #     pass
        
    name = re.findall('class="product-full__subtitle">(.+?)</',data,re.M)[0]
    try:
        tit = re.findall('class="product-full__title">(.+?)</h',data,flags=re.M)[0]
    except:
        tit = "暂无"
    price = re.findall('<span class="product-full__price">(.+?)</span>',data,re.M)[0]

    try:
        product_info = re.findall('class="spp-product__details-description">(.+?)</div>',data,re.S)[0]
        product_info = re.sub('<.+?>','',product_info,re.S).strip()
    except:
        product_info = "暂无"
    
    try:
        product_use = re.findall('class="spp-product__details-attribute__label">功效</h5>(.+?)</div>',data,re.S)[0] 
        product_use = re.sub('<.+?>','',product_use,re.S).strip()
    except:
        product_use = "暂无"
    with open("product_info.txt",'a',encoding="utf-8") as w:
        w.write("产品名字："+name+"\n"+"产品标题："+tit+"\n"+"产品颜色："+str(color_info)+"\n"+"产品价格："+price+"\n"+"产品说明："+product_info+"\n"+"使用方法："+product_use+"\n")
        w.write("\n-------------------------------------------------\n")


for i in get_product_channel():
    for x in get_product_channel_list(i):
        get_product_info(x)

