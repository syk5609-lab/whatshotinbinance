# Binance Futures Indicator Dashboard

바이낸스 선물(Futures) 지표를 한 화면에서 확인할 수 있는 Streamlit 대시보드입니다.

> 코딩이 익숙하지 않은 분도 아래 순서대로 따라 하면 실행할 수 있게 작성했습니다.

## 1) 먼저 준비할 것
- **Python 3.10 이상** 설치
- 터미널(또는 명령 프롬프트) 사용

### Python 설치 확인
아래 명령어를 입력해서 버전이 보이면 준비 완료입니다.

```bash
python --version
```

> 만약 `python` 명령이 안 되면 `python3 --version`도 시도해보세요.

---

## 2) 프로젝트 폴더로 이동
`/workspace/...` 경로는 **이 문서를 만든 개발 환경 전용 경로**라서, 일반 PC/Mac에서는 동작하지 않습니다.

아래 둘 중 하나로 진행하세요.

### 방법 A) 이미 폴더를 내려받은 경우
예: `Downloads`에 압축 해제/clone 했으면

```bash
cd ~/Downloads/whatshotinbinance
```

### 방법 B) 아직 프로젝트가 없는 경우 (git으로 받기)

```bash
git clone <저장소_URL>
cd whatshotinbinance
```

---

## 3) 가상환경 만들기 (권장)

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

활성화되면 앞에 `(.venv)` 같은 표시가 붙습니다.

---

## 4) 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

설치가 끝나면 다음 단계로 넘어가세요.

---

## 5) 대시보드 실행

```bash
streamlit run app.py
```

실행하면 보통 자동으로 브라우저가 열립니다.
자동으로 안 열리면 터미널에 표시된 주소(예: `http://localhost:8501`)를 브라우저에 직접 입력하세요.

---

## 6) 화면에서 보는 방법
좌측 사이드바에서:
- **심볼**: 예) `BTCUSDT`, `ETHUSDT`
- **기간**: `5m`, `15m`, `1h`, `4h`, `1d`
- **데이터 개수**: 최근 몇 개 데이터를 볼지 선택

메인 화면에서:
- Mark Price
- Open Interest
- Net Taker Flow (순매수/순매도)
- Long/Short Ratio
를 그래프로 확인할 수 있습니다.

---

## 자주 생기는 문제

### 1) `streamlit: command not found`
아래처럼 실행해보세요.

```bash
python -m streamlit run app.py
```

### 2) 설치 중 네트워크/프록시 오류
회사/기관 네트워크에서는 설치가 막힐 수 있습니다.
- 다른 네트워크(개인 핫스팟 등)에서 재시도
- 사내 프록시 설정 확인

### 3) Binance API 오류 메시지
- 심볼이 정확한지 확인 (`BTCUSDT` 형식)
- 잠시 후 재시도 (일시적인 API 응답 문제 가능)

---

## 기능
- 선물 심볼 선택
- 기간 및 데이터 개수 선택
- 다음 지표 시각화
  - 마크 가격(Mark Price)
  - 오픈 이자(Open Interest)
  - 테이커 순매수/순매도(Net Taker Flow)
  - 테이커 매수/매도 비율(Taker Buy/Sell Ratio)
  - 글로벌 롱/숏 계정 비율(Global Long/Short Account Ratio)

## 데이터 출처
- Binance USDⓈ-M Futures API
  - `/fapi/v1/klines`
  - `/futures/data/openInterestHist`
  - `/futures/data/takerlongshortRatio`
  - `/futures/data/globalLongShortAccountRatio`

## 참고
- 공개 지표 API 특성상 일부 구간에서 데이터가 비어있을 수 있습니다.
- 실제 매매에는 추가적인 검증/리스크 관리가 필요합니다.
