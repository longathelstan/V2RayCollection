from urllib.parse import urlparse
import base64
import json
import requests
import os
import time

results = []
cloudflare_results = []
parsed_ip = {}

def query_ip(ip: str):
    r = requests.get(f"https://api.ipgeolocation.io/ipgeo?include=hostname&ip={ip}", headers={
        "referer": "https://ipgeolocation.io/"
    })
    
    data = r.json()
    if "ip" not in data:
        return {"ip": ""}
    
    return {
        "ip": data["ip"],
        "country": data["country_name"],
        "asn": data["asn"],
        "city": data["city"]
    }

def parse_vmess(link: str):
    base64_code = link.removeprefix("vmess://")
    json_text = base64.b64decode(base64_code).decode("utf-8")
    data = json.loads(json_text)
    
    ip = data["add"]
    ip_data = {"ip": ""}
    
    if ip not in parsed_ip:
        ip_data = query_ip(ip)
        parsed_ip[ip] = ip_data
    else:
        ip_data = parsed_ip[ip]
        
    if not ip_data["ip"]:
        return
    
    ip = ip_data["ip"]
    asn = ip_data["asn"]
    country = ip_data["country"]
    city = ip_data["city"]
    
    link_name = f"{country} - {city} - {ip} - {asn}"
    
    data["ps"] = link_name
    dumped_data = json.dumps(data).encode("utf-8")
    final_code_link = base64.b64encode(dumped_data).decode("utf-8")
    
    new_link = f"vmess://{final_code_link}"
    
    if "13335" in asn:
        cloudflare_results.append(new_link)
    else:
        results.append(new_link)
    
def parse_vless(link: str):
    path = urlparse(link)
    netloc_splited = path.netloc.split("@")
    id = netloc_splited[0]
    ip_splited = netloc_splited[1].split(":")
    ip = ip_splited[0]
    port = ip_splited[1]
    
    ip_data = {"ip": ""}
    
    if ip not in parsed_ip:
        ip_data = query_ip(ip)
        parsed_ip[ip] = ip_data
    else:
        ip_data = parsed_ip[ip]
        
    if not ip_data["ip"]:
        return
    
    ip_parsed = ip_data["ip"]
    asn = ip_data["asn"]
    country = ip_data["country"]
    city = ip_data["city"]
    
    link_name = f"{country} - {city} - {ip_parsed} - {asn}"
    
    new_link = f"vless://{id}@{ip}:{port}?{path.query}#{link_name}"
    
    if "13335" in asn:
        cloudflare_results.append(new_link)
    else:
        results.append(new_link)
    
def parse_ss(link: str):
    path = urlparse(link)
    netloc_splited = path.netloc.split("@")

    if len(netloc_splited) <= 1:
        return

    id = netloc_splited[0]
    ip_splited = netloc_splited[1].split(":")
    ip = ip_splited[0]
    port = ip_splited[1]
    
    ip_data = {"ip": ""}
    
    if ip not in parsed_ip:
        ip_data = query_ip(ip)
        parsed_ip[ip] = ip_data
    else:
        ip_data = parsed_ip[ip]
        
    if not ip_data["ip"]:
        return
    
    ip_parsed = ip_data["ip"]
    asn = ip_data["asn"]
    country = ip_data["country"]
    city = ip_data["city"]
    
    link_name = f"{country} - {city} - {ip_parsed} - {asn}"
    
    new_link = f"ss://{id}@{ip}:{port}#{link_name}"
    
    if "13335" in asn:
        cloudflare_results.append(new_link)
    else:
        results.append(new_link)
    
def parse_trojan(link: str):
    path = urlparse(link)
    
    netloc_splited = path.netloc.split("@")
    id = netloc_splited[0]
    ip_splited = netloc_splited[1].split(":")
    ip = ip_splited[0]
    port = ip_splited[1]
    
    ip_data = {"ip": ""}
    
    if ip not in parsed_ip:
        ip_data = query_ip(ip)
        parsed_ip[ip] = ip_data
    else:
        ip_data = parsed_ip[ip]
        
    if not ip_data["ip"]:
        return
    
    ip_parsed = ip_data["ip"]
    asn = ip_data["asn"]
    country = ip_data["country"]
    city = ip_data["city"]
    
    link_name = f"{country} - {city} - {ip_parsed} - {asn}"
    
    new_link = f"trojan://{id}@{ip}:{port}?{path.query}#{link_name}"
    
    if "13335" in asn:
        cloudflare_results.append(new_link)
    else:
        results.append(new_link)

def main():
    global parsed_ip
    
    if os.path.isfile("files/ips.json"):
        with open("files/ips.json", "r", encoding="utf-8") as f:
            parsed_ip = json.load(f)
    
    with open("files/v2ray_raw.txt", "r", encoding="utf-8") as f:
        links = f.readlines()
        
    i = 0
        
    for link in links:
        try:
            if link.startswith("vless://"):
                parse_vless(link)
        
            if link.startswith("vmess://"):
                parse_vmess(link)
                
            if link.startswith("trojan://"):
                parse_trojan(link)
                
            if link.startswith("ss://"):
                parse_ss(link)
        except Exception as e:
            print(link)
            
        i += 1
        print(i)
            
    with open("files/ips.json", "w", encoding="utf-8") as f:
        json.dump(parsed_ip, f, indent=4, ensure_ascii=False)
        
    with open("files/v2ray_filtered.txt", "w", encoding="utf-8") as f:
        result_string = "\n".join(results)
        f.write(result_string)
        
    with open("files/v2ray_cloudflare.txt", "w", encoding="utf-8") as f:
        result_string = "\n".join(cloudflare_results)
        f.write(result_string)
        
if __name__ == "__main__":
    main()