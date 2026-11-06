"""
ST 소싱 툴 포털 (K8s 배포용)
입고계획 대시보드 + EAN 자동생성기를 탭으로 통합
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ST 소싱 툴")

INBOUND_URL = "https://dcsai.fnf.co.kr/apps/st-26f-inbound"
INBOUND_27S_URL = INBOUND_URL + "?s=27s"  # 27S·27N 시즌 (같은 앱, 쿼리로 구분)
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

  /* 입고계획 탭 활성 시에만 보이는 시즌 선택 */
  .season-bar {
    display: none;
    align-items: center;
    gap: 6px;
    margin-left: auto;
    align-self: center;
  }
  .season-bar.show { display: flex; }
  .season-bar .lbl { color: #aaa; font-size: 12px; margin-right: 2px; }
  .season-btn {
    padding: 5px 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,.3);
    background: transparent;
    color: #ccc;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
  }
  .season-btn:hover { color: #fff; border-color: #fff; }
  .season-btn.active { background: #f4f6f9; color: #1a1a2e; border-color: #f4f6f9; }
</style>
</head>
<body>
<div class="tab-bar">
  <div class="tab active" onclick="switchTab(0)">입고계획 대시보드</div>
  <div class="tab" onclick="switchTab(1)">EAN 자동생성기</div>
  <div class="season-bar show" id="seasonBar">
    <span class="lbl">시즌</span>
    <button class="season-btn active" data-url="INBOUND_URL_PLACEHOLDER" onclick="switchSeason(this)">26F</button>
    <button class="season-btn" data-url="INBOUND_27S_URL_PLACEHOLDER" onclick="switchSeason(this)">27S·27N</button>
  </div>
</div>
<div class="frame-wrap">
  <iframe id="frame0" class="active" src="INBOUND_URL_PLACEHOLDER" title="입고계획 대시보드"></iframe>
  <iframe id="frame1" src="EAN_URL_PLACEHOLDER" title="EAN 자동생성기"></iframe>
</div>

<script>
function switchTab(idx) {
  document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('iframe').forEach((f, i) => f.classList.toggle('active', i === idx));
  document.getElementById('seasonBar').classList.toggle('show', idx === 0);
}
function switchSeason(btn) {
  document.querySelectorAll('.season-btn').forEach(b => b.classList.toggle('active', b === btn));
  var f = document.getElementById('frame0');
  if (f.getAttribute('src') !== btn.dataset.url) f.src = btn.dataset.url;
}
</script>
</body>
</html>""".replace("INBOUND_27S_URL_PLACEHOLDER", INBOUND_27S_URL).replace("INBOUND_URL_PLACEHOLDER", INBOUND_URL).replace("EAN_URL_PLACEHOLDER", EAN_URL)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.get("/health")
async def health():
    return {"status": "ok"}
