import requests

class CDKMOCR:
    def get_text(url: str):
        headers = {
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryfHb9s997gPObm9e2',
            'referer': 'https://cdkm.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        data = f'------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="file"\r\n\r\n\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="fileurl"\r\n\r\n{url}\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="filelocation"\r\n\r\nonline\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="targetformat"\r\n\r\n\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="imagesize"\r\n\r\n1\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="code"\r\n\r\n80010\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="ocrsoft"\r\n\r\nocr1\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="ocrlan"\r\n\r\nscript/Vietnamese\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="ocrtar"\r\n\r\ntxt\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="randomstr"\r\n\r\nst34zcxxqrk46hi700gvun3c2bgj4jh1\r\n------WebKitFormBoundaryfHb9s997gPObm9e2\r\nContent-Disposition: form-data; name="warning"\r\n\r\nWe DO NOT allow using our PHP programs in any third-party websites, software or apps! We will report abuse to your server provider, Google Play and App store if illegal usage found!\r\n------WebKitFormBoundaryfHb9s997gPObm9e2--\r\n'

        response = requests.post('https://kirk.cdkm.com/convert/c1.php', headers=headers, data=data)
        
        filename = response.json()['filename']
        
        r = requests.get(f"https://kirk.cdkm.com/convert/file/st34zcxxqrk46hi700gvun3c2bgj4jh1/{filename}")

        return r.text