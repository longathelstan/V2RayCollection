import requests

class Global1V2Ray:
    
    def update(self):
        r = requests.get("https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt")
        # remove all comment
        array_links = [x for x in r.text.split("\n")[5:] if x]
        result = "\n".join(array_links)
        
        with open("files/raw/v2ray_global_1.txt", "w", encoding="utf-8") as f:
            f.write(result)