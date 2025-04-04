import requests

class OCRSpace:
    def get_text(url: str):
        headers = {
            'apikey': 'donotstealthiskey8589',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryRXlujeqzoYEENrzP',
            'referer': 'https://ocr.space/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        data = f'------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="url"\r\n\r\n{url}\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="language"\r\n\r\nvie\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="isOverlayRequired"\r\n\r\ntrue\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="FileType"\r\n\r\n.Auto\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="IsCreateSearchablePDF"\r\n\r\nfalse\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="isSearchablePdfHideTextLayer"\r\n\r\ntrue\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="detectOrientation"\r\n\r\nfalse\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="isTable"\r\n\r\nfalse\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="scale"\r\n\r\ntrue\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="OCREngine"\r\n\r\n3\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="detectCheckbox"\r\n\r\nfalse\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP\r\nContent-Disposition: form-data; name="checkboxTemplate"\r\n\r\n0\r\n------WebKitFormBoundaryRXlujeqzoYEENrzP--\r\n'
        response = requests.post('https://api8.ocr.space/parse/image', headers=headers, data=data)
        return response.json()["ParsedResults"][0]["ParsedText"]
    
if __name__ == "__main__":
    print(OCRSpace.get_text("https://iili.io/JJQe2e4.jpg"))