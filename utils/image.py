from dotenv import load_dotenv
load_dotenv()
import cv2
import numpy as np
import requests
import os

class Image:
    def crop_image(data: bytes):
        img_np = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(img_np, flags=1)
        image = cv2.resize(image, (0, 0), fx=0.4, fy=0.4)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        table_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(table_contour)
        table = image[y:y + h, x:x + w]
        
        return cv2.imencode('.jpg', table)[1].tobytes()
    
    def upload_image(data: bytes):
        r = requests.post(f"https://freeimage.host/json", data={
            "auth_token": os.getenv("FREEIMAGEHOSTING_TOKEN"),
            "action": "upload",
            "type": "file",
            "nsfw": "0"
        }, files={"source": data})
        return r.json()["image"]["url"]