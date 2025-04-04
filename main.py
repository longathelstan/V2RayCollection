from flask import Flask, send_file

app = Flask(__name__)

@app.route("/v2ray_global_links")
def v2ray_global_links():
    return send_file("files/v2ray_filtered.txt")

@app.route("/v2ray_cloudflare")
def v2ray_cloudflare():
    return send_file("files/v2ray_cloudflare.txt")

if __name__ == "__main__":
    app.run()