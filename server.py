"""
ST 소싱 툴 포털 (K8s 배포용)
입고계획 대시보드 + EAN 자동생성기를 탭으로 통합
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ST 소싱 툴")

INBOUND_URL = "https://dcsai.fnf.co.kr/apps/st-26f-inbound"
EAN_URL = "https://dcsai.fnf.co.kr/apps/st-ean-barcode"

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ST 소싱 툴</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; overflow: hidden; font-family: 'Malgun Gothic', sans-serif; }

  .tab-bar {
    display: flex;
    align-items: flex-end;
    background: #1a1a2e;
    padding: 0 20px;
    height: 50px;
    gap: 4px;
    flex-shrink: 0;
  }
  .tab {
    padding: 10px 22px;
    color: #aaa;
    cursor: pointer;
    border-radius: 8px 8px 0 0;
    font-size: 14px;
    font-weight: 600;
    transition: all .2s;
    user-select: none;
    border: 1px solid transparent;
    border-bottom: none;
  }
  .tab:hover { color: #fff; background: rgba(255,255,255,.1); }
  .tab.active {
    background: #f4f6f9;
    color: #1a1a2e;
    border-color: #ddd;
  }

  .frame-wrap {
    height: calc(100vh - 50px);
    position: relative;
    background: #f4f6f9;
  }
  iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
    display: none;
  }
  iframe.active { display: block; }
</style>
</head>
<body>
<div class="tab-bar">
  <div class="tab active" onclick="switchTab(0)">입고계획 대시보드</div>
  <div class="tab" onclick="switchTab(1)">EAN 자동생성기</div>
</div>
<div class="frame-wrap">
  <iframe id="frame0" class="active" src="INBOUND_URL_PLACEHOLDER" title="입고계획 대시보드"></iframe>
  <iframe id="frame1" src="EAN_URL_PLACEHOLDER" title="EAN 자동생성기"></iframe>
</div>

<script>
function switchTab(idx) {
  document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('iframe').forEach((f, i) => f.classList.toggle('active', i === idx));
}
</script>
</body>
</html>""".replace("INBOUND_URL_PLACEHOLDER", INBOUND_URL).replace("EAN_URL_PLACEHOLDER", EAN_URL)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.get("/health")
async def health():
    return {"status": "ok"}
