import requests,re

def get_proya_info():
    rsp = requests.get("https://www.lamer.com.cn/brand-story")
    rsp.encoding = "utf-8"
    data = rsp.text
    #proya_info = re.search('<div class="txtBox">.+?<div class="footerBox">',data,flags=re.S).group()
    proya_info = re.findall('<div class=" heading padding(.+?)</div>',data,re.S)#[0].replace("<br/>","").replace("   ","\n")
    for i in range(len(proya_info)):
        proya_info[i] = re.findall('>(.+?)\n',proya_info[i],re.S)[0].replace('<br/>','').replace('<br>','').strip()
    return proya_info[:-2]

def get_product_list():         #获取产品每个分类下商品的链接列表
    rsp = requests.get("https://www.lamer.com.cn/skincare-glowing-skin")
    rsp.encoding = "utf-8"
    data = rsp.text
    
    product_list = re.findall('<div class="product__subline"><a href="(.+)">',data)   
    return product_list


def get_product_info(product_list):
    try:
        print(product_list)
        rsp = requests.get("https://www.lamer.com.cn" + product_list)
        rsp.encoding = "utf-8"
        data = rsp.text

        name = re.findall('data-title="(.+?)">',data)[0]
        tit = re.findall('<h2 class="product-full__desc">(.+?)</h2>',data,re.S)[0]
        try:
            price = re.search('<ul class="sku-list__list">.+?</ul>',data,re.S).group()
            price = re.findall('>\n                            (.+?)\n',price,re.S)
        except:
            price = "暂无"
        
        try:
            product_msg = re.search('<div class="product-full__accordion__title js-accordion__title init--open">了解详情</div>(.+?)<div class="product-full__accordion__title js-accordion__title init--open">',data,re.S).group()
            product_info = re.findall('<div class="product-full__accordion__panel js-accordion__panel init--open">(.+?)</div>',product_msg,re.S)[0].replace("</div>",'').strip()
            product_use = re.search('使用方法</div>(.+?)</div>',product_msg,re.S).group()
            product_use = re.findall('panel init--closed">(.+?)</div>',product_use,re.S)[0].strip()
        except:
            product_info = "暂无"
            product_use = "暂无"
        with open("product_info.txt",'a',encoding="utf-8") as w:
            w.write("产品名字："+name+"\n"+"产品简介："+tit+"\n"+"产品价格："+str(price)+"\n"+"产品说明："+product_info+"\n"+"使用方法："+product_use+"\n")
            w.write("\n-------------------------------------------------\n")
    except:
        pass
with open("product_info.txt",'a',encoding="utf-8") as w:
    w.write("品牌介绍\n")
    for x in get_proya_info():
        w.write(x + "\n")
    w.write("\n-------------------------------------------------\n")
for i in get_product_list():
    get_product_info(i)
