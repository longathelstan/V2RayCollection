import docx2txt
import io
import requests
import os
class GoogleDocs:
    def download_text(id_file):
        API_KEY = os.getenv("GOOGLE_API_KEY")
        r = requests.get(f"https://www.googleapis.com/drive/v3/files/{id_file}/export?mimeType=application/vnd.openxmlformats-officedocument.wordprocessingml.document&key={API_KEY}")
        return docx2txt.process(io.BytesIO(r.content))