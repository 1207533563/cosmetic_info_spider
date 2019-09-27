import requests,re

def get_proya_info():
    rsp = requests.get("https://www.bobbibrown.com.cn")
    rsp.encoding = "utf-8"
    data = rsp.text
    proya_info = re.search('<div class="txtBox">.+?<div class="footerBox">',data,flags=re.S).group()
    proya_info = re.findall('<div class="txt">(.+?)</div>',proya_info,re.S)[0].replace("<br>","").replace("   ","\n")
    return proya_info

def get_product_channel_list(channel_list):         #获取产品每个分类下商品的链接列表
    rsp = requests.get("https://www.bobbibrown.com.cn" + channel_list)
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.search('<div class="product-brief__abstract">(.+)<footer class="site-footer">',data,flags=re.S).group() 
    pd = re.findall('<a href="(.+?)" class="product-brief__headline-link js-spp-link">',wb)

    return pd

def get_product_channel():     #获取产品分类列表
    channel_list = []
    rsp = requests.get("https://www.bobbibrown.com.cn")
    rsp.encoding = "utf-8"
    data = rsp.text
    hf = re.search('<span class="gnav-section__link-wrapper__inner">底妆</span>.+?<a href="/products/14006/skincare" class="gnav-section__link gnav-section__link--top js-nav-category-trigger js-nav-category-trigger--top">护肤</a>',data,flags=re.S).group()
    hf = re.findall('<div class="gnav-link gnav-link--subcategory-link">(.+?)</div>',hf,flags=re.S)
    for i in hf:
        channel_list.append(i)

    mm = re.search('<a href="/products/14006/skincare" class="gnav-section__link js-nav-category-trigger">.+?<a href="/products/18510/skincare/skin-type" class="js-menu-shop-all">全部商品</a>',data,flags=re.S).group()
    mm = re.findall('<div class="gnav-link gnav-link--subcategory-link">(.+?)</div>',mm,flags=re.S)
    for j in mm:
        channel_list.append(j)

    for k in range(len(channel_list)):
        channel_list[k] = re.findall('<a href="(.+?)" class',channel_list[k])
    
    return channel_list

def get_product_info(product_data):
    try:
        print(product_data)
        rsp = requests.get("https://www.bobbibrown.com.cn" + product_data)
        rsp.encoding = "utf-8"
        data = rsp.text
        info = re.search('<div class="site-content" id="main-focus-content">(.+?)<div class="product-full__social-share">',data,flags=re.S).group()
        name = re.findall('<h3 class="product-full__sub-line">(.+?)</h3>',info,re.M)[0]
        tit = re.findall('<h2 class="product-full__short-desc">(.+?)</h2>',info,re.M)
        tit = tit[0]
        price = re.findall('<span class="price">(.+?)</span>',info,re.M)[0]
        try:
            product_info = re.search('<div class="product-full__data-content product-full__data-content--what" id="what" aria-hidden="true">.+?</section>',info,re.S).group()
            product_info = re.findall('aria-hidden="true">(.+)</div>',product_info,re.S)[0].replace("<br>",'').replace("<div>",'').replace("</div>",'').replace('<P>','').replace("</P>",'').replace("&nbsp;",'').replace('<p>','').replace("</p>",'').replace('<strong>','').replace("</strong>",'').replace('<STRONG>','').replace("</STRONG>",'').replace("<BR>",'').strip()
            product_info = re.sub('<.*?style.*?>','',product_info)
        except:
            product_info = "无"

        try:
            product_why = re.search('<div class="product-full__data-content product-full__data-content--why" id="why" aria-hidden="true">.+?</section>',info,re.S).group()
            product_why = re.findall('aria-hidden="true">(.+)</div>',product_why,re.S)[0].replace("<br>",'').replace("<div>",'').replace("</div>",'').replace('<P>','').replace("</P>",'').replace("&nbsp;",'').replace('<p>','').replace("</p>",'').replace('<strong>','').replace("</strong>",'').replace('<STRONG>','').replace("</STRONG>",'').replace("<BR>",'').strip()
        except:
            product_why = "无"
        try:
            product_use = re.search('<div class="product-full__data-content product-full__data-content--usage" id="usage" aria-hidden="true">.+?</section>',info,re.S).group()
            product_use = re.findall('aria-hidden="true">(.+)</div>',product_use,re.S)[0].replace("<br>",'').replace("<div>",'').replace("</div>",'').replace('<P>','').replace("</P>",'').replace("&nbsp;",'').replace('<p>','').replace("</p>",'').replace('<strong>','').replace("</strong>",'').replace('<STRONG>','').replace("</STRONG>",'').replace("<BR>",'').strip()
        except:
            product_use = "无"    
        with open("product_info.txt",'a',encoding="utf-8") as w:
            w.write("产品名字："+name+"\n"+"产品简介："+tit+"\n"+"产品价格："+price+"\n"+"产品说明："+product_info+"\n"+"为何拥有:"+ product_why+"\n"+"使用方法："+product_use+"\n")
            w.write("\n-------------------------------------------------\n")

    except:
        pass

for x in get_product_channel():
    for y in x:
        for z in get_product_channel_list(y):
                get_product_info(z)
