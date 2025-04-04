from dotenv import load_dotenv
load_dotenv()
import requests
import os
import base64
import re
import json
import sys
import random

random_ips = ["extra.ht4gvpn.com", "maxvip.ht4gvpn.com", "premium.ht4gvpn.com"]

def proxy_1():
    config={'log':{'loglevel':'warning'},'inbounds':[{'port':1080,'listen':'127.0.0.1','protocol':'socks','settings':{'udp':True}},{'port':1081,'listen':'127.0.0.1','protocol':'http','settings':{'auth':'noauth','udp':True,'ip':'127.0.0.1','clients':None}}],'outbounds':[{'mux':{'enabled':False},'protocol':'trojan','settings':{'servers':[{'address':'sub9.htpn.vn','level':8,'password':'3fbfb12b-c5aa-4c95-aad7-3f4140fccbfc','port':443}]},'streamSettings':{'security':'tls','tlsSettings':{'allowInsecure':True,'serverName':'dl.kgvn.garenanow.com'}},'tag':'TROJAN'}],'policy':{'levels':{'8':{'connIdle':300,'downlinkOnly':1,'handshake':4,'uplinkOnly':1}}},'routing':{'domainStrategy':'IPOnDemand','rules':[{'type':'field','ip':['geoip:private'],'outboundTag':'direct'}]}}
    TOKEN = os.getenv("HTPN_TOKEN")
    r = requests.get(f"https://api.htpn.vn/api/v1/client/subscribe?token={TOKEN}")
    data = base64.b64decode(r.text).decode("utf-8")
    matches = list(re.finditer(r"trojan:\/\/(?P<password>.+)@(?P<ip>.+):", data, re.MULTILINE))

    data = matches[0].groupdict()
    config["outbounds"][0]["settings"]["servers"][0]["address"] = data["ip"]
    config["outbounds"][0]["settings"]["servers"][0]["password"] = data["password"]

    with open(".v2ray/config.json", "w") as f:
        json.dump(config, f)
        
def proxy_2():
    config={'policy': {'system': {'statsInboundUplink': True, 'statsInboundDownlink': True}}, 'log': {'access': '', 'error': '', 'loglevel': 'debug'}, 'inbounds': [{'tag': 'proxy', 'port': 1080, 'listen': '127.0.0.1', 'protocol': 'socks', 'sniffing': {'enabled': True, 'destOverride': ['http', 'tls']}, 'settings': {'auth': 'noauth', 'udp': True, 'ip': None, 'address': None, 'clients': None}, 'streamSettings': None}], 'outbounds': [{'tag': '🇻🇳TURBO CLOUD SERVER (LQ) turbo.ht4gvpn.com 80', 'protocol': 'vmess', 'settings': {'vnext': [{'users': [{'email': 't@t.tt', 'security': 'auto', 'id': '440296a5-09d8-4194-8b98-1f59b4132f3f', 'alterId': 0}], 'address': 'turbo.ht4gvpn.com', 'port': 80}], 'servers': None, 'response': None}, 'streamSettings': {'network': 'ws', 'security': None, 'tlsSettings': {'allowInsecure': True}, 'kcpSettings': {'mtu': 1350, 'tti': 50, 'uplinkCapacity': 12, 'downlinkCapacity': 100, 'congestion': False, 'readBufferSize': 2, 'writeBufferSize': 2, 'header': {'type': 'wechat-video'}}, 'wsSettings': {'connectionReuse': True, 'path': '/ht4gvpn.com', 'headers': {'Host': 'dl.kgvn.garenanow.com'}}, 'httpSettings': {'host': ['host.com'], 'path': '/host'}, 'quicSettings': {'security': 'none', 'key': '', 'header': {'type': 'none'}}, 'tcpSettings': {'connectionReuse': True, 'header': {'type': 'http', 'request': {'version': '1.1', 'method': 'GET', 'path': ['/'], 'headers': {'Host': [''], 'User-Agent': ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/53.0.2785.109 Mobile/14A456 Safari/601.1.46'], 'Accept-Encoding': ['gzip, deflate'], 'Connection': ['keep-alive'], 'Pragma': 'no-cache'}}}}}, 'mux': {'enabled': False}}, {'tag': 'direct', 'protocol': 'freedom', 'settings': {'vnext': None, 'servers': None, 'response': None}, 'streamSettings': None, 'mux': None}, {'tag': 'block', 'protocol': 'blackhole', 'settings': {'vnext': None, 'servers': None, 'response': {'type': 'http'}}, 'streamSettings': None, 'mux': None}], 'stats': {}, 'api': {'tag': 'api', 'services': ['StatsService']}, 'dns': None, 'routing': {'domainStrategy': 'IPIfNonMatch', 'rules': [{'type': 'field', 'port': None, 'inboundTag': 'api', 'outboundTag': 'api', 'ip': None, 'domain': None}]}}
    with open("files/sub_3.txt", "r") as f:
        data = f.readlines()
    
    random_ip = random.choice(random_ips)

    for item in data:
        if "vmess://" in item:
            item = item.replace("vmess://", "")
            data = base64.b64decode(item).decode("utf-8")
            json_data = json.loads(data)
            if random_ip in json_data["add"]:
                config["outbounds"][0]["settings"]["vnext"][0]["address"] = json_data["add"]
                config["outbounds"][0]["settings"]["vnext"][0]["users"][0]["id"] = json_data["id"]
                config["outbounds"][0]["streamSettings"]["path"] = json_data["path"]
                break
            
    with open(".v2ray/config.json", "w") as f:
        json.dump(config, f)
            
if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == "1":
        proxy_1()
    if arg == "2":
        proxy_2()