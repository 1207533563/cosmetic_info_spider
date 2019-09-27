import requests,re,time,os

def get_product_channel():       
    #获得品牌下化妆品分类链接,返回该分类的每个数字代号，是一个列表，列表中每个元素为代号，分类名
    rsp = requests.get("http://www.uzero.com.cn/product_channel")
    rsp.encoding = "utf-8"
    data = rsp.text
    wb = re.search('<div class="product-channel-list">(.+?)<div class="hd">',data,flags=re.S).group()
    pd = re.findall('<a href="http://www.uzero.com.cn/product_channel/index/(.+?)">.+?<div class="font">(.+?)</div>',wb,re.S)
    return pd
#get_product_channel()
def get_product_list(get_product_channel):
    #获得品牌下某一化妆品分类下的所有产品名字和链接,返回该分类下的每个产品链接，是一个列表，列表中每个元素为链接，产品名字
    #print(get_product_channel)
    url = "http://www.uzero.com.cn/product_channel/index/"+get_product_channel
    rsp = requests.get(url)
    rsp.encoding = "utf-8"
    data = rsp.text
    hf = re.search('<div class="product-channel-con">(.+?)<div class="w1180">',data,flags=re.S).group()
    hf_info = re.findall('<a href="(.+?)" class="list">.+?<div class="font">(.+?)</div>',hf,re.S)
    return hf_info

def get_product_info(get_product_list):
    #获得产品信息，包括产品名字，价格，容量，使用方法，简介
    url = get_product_list
    rsp = requests.get(url)
    rsp.encoding = "utf-8"
    data = rsp.text
    prd_info = re.search('<div class="right">(.+?)<div class="link-box f-cb"',data,re.S).group()

    name = re.search('<h2>(.+?)</h2>',prd_info,re.M).group().replace("<h2>",'').replace("</h2>","")
    price = re.findall('<div class="price"><span>(.+?)</span>(.+?)</div>',prd_info,re.M)
    try:
        size = re.search('<p>(.+?)</p>',prd_info,re.M).group().replace("<p>",'').replace("</p>","")
        
    except:
        size = "无"

    prd_use = re.search('<div class="classification">(.+?)<div class="product-info-bot w1180">',data,re.S).group()
    prd_info = re.search('<div class="identical explain">(.*?)</div>',prd_use,re.S).group().replace('<div class="identical explain">','').replace("</div>","").replace("<p>","").replace("</p>","").replace("<br/>","\n").strip()
    if len(prd_info) == 0:
        prd_info = "暂无"
    prd_use = re.search('<div class="identical method">(.*?)</div>',prd_use,re.S).group().replace('<div class="identical method">','').replace("</div>","").replace("<p>","").replace("</p>","").replace("<br/>","\n").strip()
    if prd_use == 0:
        prd_use = "暂无"
        
    with open("product_info.txt","a",encoding="utf-8") as w:
        w.write("产品名字："+ name + "\n" +"价格："+ price[0][0]+price[0][1]+ "\n"+"规格:"+size+ "\n"+"产品信息:"+prd_info+ "\n"+"使用方法:"+prd_use+ "\n\n")

print("正在爬取")
start_time = time.time()
for n in get_product_channel():

    for i in get_product_list(n[0]):

        get_product_info(i[0])
end_time = time.time()
os.path.getsize("product_info.txt")
time = start_time - end_time
print("写入完毕,耗时",time)
