import os
import ssl
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from supabase import create_client, Client

# 🔹 SSL 환경 변수 설정
os.environ["SSL_CERT_FILE"] = r"C:\Program Files\OpenSSL-Win64\bin\cacert.pem"
os.environ["SSL_CERT_DIR"] = r"C:\Program Files\OpenSSL-Win64\certs"

# 🔹 SSL 컨텍스트 강제 적용
class SSLAdapter(HTTPAdapter):
    """SSL 설정을 강제 적용하는 requests adapter"""
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

# 🔹 Supabase 연결 설정
SUPABASE_URL = "https://rwptfzwwbwrhgmrutdeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ3cHRmend3YndyaGdtcnV0ZGVnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEwNTM0MDAsImV4cCI6MjA1NjYyOTQwMH0.hE0ldqzL87Q8s00PefTsl9q6jM6hhaFXg10xMjJNf5g"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print(f"🔍 현재 SSL 기본 경로 확인: {ssl.get_default_verify_paths()}")
print(f"🔍 현재 SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE')}")
print(f"🔍 현재 SSL_CERT_DIR: {os.environ.get('SSL_CERT_DIR')}")
print("✅ Supabase 연결 성공!")

# 🔹 API 요청 설정 (SSL 강제 적용)
session = requests.Session()
session.mount("https://", SSLAdapter())

api_url = "https://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
params = {
    "serviceKey": "nyZuwbqlRm/n1hl4I0rxkQJe8a7IGLvOY1ViYH4sAQ4VKCzs+X5Uooa7CsYPNi5+nGFvUHR2C2cgKWaAW90zhw==",
    "numOfRows": "9999",
    "pageNo": "1",
    "dataType": "XML",
    "kind": "C0",
    "kindDetail": "C001"
}

try:
    response = session.get(api_url, params=params, verify=False)
    print(f"✅ API 응답 성공: {response.status_code}")
    print(response.text)
except requests.exceptions.SSLError as e:
    print(f"🚨 SSL 오류 발생: {e}")
except requests.exceptions.RequestException as e:
    print(f"🚨 요청 오류 발생: {e}")
