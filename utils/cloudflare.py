import re
class Cloudflare:
    def decode_email(data: str):
        r = int(data[:2],16)
        email = ''.join([chr(int(data[i:i+2], 16) ^ r) for i in range(2, len(data), 2)])
        return email
    
    def replace_html(html: str):
        matches = list(re.finditer(r"<a .+data-cfemail=\"(?P<data_email>.+)\" href.+<\/a>", html, re.MULTILINE))
        for item in matches:
            email_encode = item.groupdict()["data_email"]
            email_decode = Cloudflare.decode_email(email_encode)
            html = html.replace(item.group(), email_decode)
        return html