"""
ST 소싱 툴 포털 (K8s 배포용)
입고계획 대시보드 + EAN 자동생성기를 탭으로 통합
"""
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ST 소싱 툴")

INBOUND_URL = "https://dcsai.fnf.co.kr/apps/st-26f-inbound"
# 27S·27N 시즌 (같은 앱, 쿼리로 구분). dcsai.fnf.co.kr/apps/... 셸은 쿼리/하위경로를 앱에 넘기지 않으므로 앱 도메인을 직접 사용
INBOUND_27S_URL = "https://st-26f-inbound.apps.dcsai.fnf.co.kr/?s=27s"
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

  body { display: flex; flex-direction: column; }
  .frame-wrap {
    flex: 1;
    min-height: 0;
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

  /* 입고계획 탭 활성 시에만 보이는 시즌 선택 (탭 바로 아래 한 줄) */
  .season-bar {
    display: none;
    align-items: center;
    gap: 10px;
    padding: 0 20px;
    height: 54px;
    flex-shrink: 0;
    background: #f4f6f9;
    border-bottom: 1px solid #ddd;
  }
  .season-bar.show { display: flex; }
  .season-bar .lbl { color: #555; font-size: 15px; font-weight: 700; margin-right: 4px; }
  .season-btn {
    min-width: 96px;
    padding: 9px 28px;
    border-radius: 22px;
    border: 2px solid #1a1a2e;
    background: #fff;
    color: #1a1a2e;
    font-size: 17px;
    font-weight: 800;
    cursor: pointer;
    font-family: inherit;
    transition: all .15s;
  }
  .season-btn:hover { background: #e8eaf2; }
  .season-btn.active { background: #1a1a2e; color: #fff; box-shadow: 0 2px 6px rgba(26,26,46,.35); }
</style>
</head>
<body>
<div class="tab-bar">
  <div class="tab active" onclick="switchTab(0)">입고계획 대시보드</div>
  <div class="tab" onclick="switchTab(1)">EAN 자동생성기</div>
</div>
<div class="season-bar show" id="seasonBar">
  <span class="lbl">시즌 선택</span>
  <button class="season-btn active" data-url="INBOUND_URL_PLACEHOLDER" onclick="switchSeason(this)">26F</button>
  <button class="season-btn" data-url="INBOUND_27S_URL_PLACEHOLDER" onclick="switchSeason(this)">27S</button>
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
