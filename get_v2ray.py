from sources import *
from dotenv import load_dotenv
load_dotenv()
import sys
import glob

v2ray_sources = {
    "global1": Global1V2Ray()
}

def main():
    args = sys.argv[1:]
    
    if len(args) <= 1:
        for clazz in v2ray_sources.values():
            clazz.update()
    else:
        for arg in args:
            lowered_arg = arg.lower()
            if lowered_arg in v2ray_sources:
                v2ray_sources[lowered_arg].update()
                
    f_raw = open("files/v2ray_raw.txt", "w", encoding="utf-8")
                
    for file_path in glob.glob("files/raw/*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            f_raw.write(f.read())
            
    f_raw.close()

if __name__ == "__main__":
    main()