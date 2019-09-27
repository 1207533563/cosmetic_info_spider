import requests,re,os
import socket
from xpinyin import Pinyin
import prettytable as pt

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.connect(("www.uzero.com.cn",80))
req = "GET /about HTTP/1.1\r\nConnection: Close\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\r\nHost: www.uzero.com.cn\r\n\r\n"
sock.send(req.encode())
data = b''
while True:
    msg = sock.recv(1024)
    if len(msg) == 0:
        break
    data += msg
sock.close()
data = data.decode('utf-8',errors="ignore")

s = re.findall('<h2>品牌概述</h2>(.+?)<h2>产品品牌</h2>(.+?)<h2>优资莱历程</h2>(.+?)<h2>品牌广告</h2>',data,re.S)
gs = re.findall('<p>(.+?)</p><p>',s[0][0])
pp = re.findall('<p>(.+?)</p>',s[0][1])

lc = re.findall('<p>(.+?)</p>',s[0][2])
for i in range(len(lc)):
    lc[i] = lc[i].replace("<strong>","")
    lc[i] = lc[i].replace("</strong>","")
while "<br/>" in lc:
    lc.remove("<br/>")

with open("uzero_info.txt","a",encoding="utf-8") as f:
    f.write("品牌概述：\n%s"%gs[1] +"\n\n")
    f.write("旗下品牌:\n")
    for i in pp[1:]:
        f.write(i +"\n\n")
    f.write("优资莱历程\n")
    for n in lc[1:]:
        f.write(n +"\n\n")

