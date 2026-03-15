# Binance Futures Indicator Dashboard

바이낸스 선물(Futures) 지표를 한 화면에서 확인할 수 있는 Streamlit 대시보드입니다.

> 코딩이 익숙하지 않은 분도 그대로 따라 하면 실행할 수 있도록, **Mac 기준으로 아주 자세히** 설명합니다.

## 0) 지금 보신 에러의 의미
터미널에서 아래처럼 나온 경우:

```bash
cd: no such file or directory: /workspace/whatshotinbinance
```

이건 정상입니다.
`/workspace/...`는 이 문서를 만든 개발 컨테이너 경로이고, 일반 Mac에는 없는 경로입니다.

즉, 내 Mac 안에 실제로 있는 폴더 경로로 들어가야 합니다.

---

## 1) 먼저 준비할 것
- **Python 3.10 이상**
- 인터넷 연결
- 터미널 앱 (Mac 기본 앱)

### 1-1. Python 설치 확인
```bash
python3 --version
```
- 버전이 보이면 OK (예: `Python 3.11.9`)
- `command not found`면 Python 먼저 설치해야 합니다.

---

## 2) 내 Mac에 프로젝트 폴더가 있는지 먼저 확인

### 방법 A) 이미 ZIP 다운로드/압축해제 했을 가능성이 높은 경우
아래 순서로 확인:

```bash
cd ~
ls
```

`Downloads`가 보이면:

```bash
cd ~/Downloads
ls
```

`whatshotinbinance` 폴더가 보이면 이동:

```bash
cd ~/Downloads/whatshotinbinance
pwd
```

`pwd` 결과가 현재 경로입니다. (예: `/Users/kimsoohyun/Downloads/whatshotinbinance`)

### 방법 B) 폴더가 없는 경우 (git clone)
GitHub 저장소 주소를 알고 있다면:

```bash
cd ~
git clone <저장소_URL>
cd whatshotinbinance
pwd
```

> `<저장소_URL>` 자리에 실제 주소를 넣어야 합니다.
> 예: `https://github.com/yourname/whatshotinbinance.git`

---

## 3) 가상환경 만들기 (필수는 아니지만 강력 권장)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

성공하면 터미널 앞에 `(.venv)`가 붙습니다.

---

## 4) 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

에러가 나면 아래 "자주 생기는 문제"를 보세요.

---

## 5) 대시보드 실행

```bash
streamlit run app.py
```

만약 `streamlit: command not found`가 나오면:

```bash
python3 -m streamlit run app.py
```

실행되면 터미널에 보통 이런 주소가 나옵니다:
- `http://localhost:8501`

이 주소를 브라우저(Chrome/Safari)에 붙여넣으면 대시보드가 열립니다.

---

## 6) 화면에서 어떻게 보면 되는지
좌측 사이드바에서:
- **심볼**: `BTCUSDT`, `ETHUSDT` 등
- **기간**: `5m`, `15m`, `1h`, `4h`, `1d`
- **데이터 개수**: 최근 데이터 개수

메인 화면에서 확인:
- **Mark Price**: 현재 가격 흐름
- **Open Interest**: 미결제약정 흐름
- **Net Taker Flow**: 순매수/순매도 (양수면 순매수 우위, 음수면 순매도 우위)
- **Long/Short Ratio**: 롱/숏 비율

---

## 7) 자주 생기는 문제 (Mac)

### 7-1) `cd: no such file or directory`
경로가 틀린 겁니다. 아래로 실제 폴더를 먼저 찾으세요.

```bash
cd ~
find . -maxdepth 3 -type d -name "whatshotinbinance"
```

찾은 경로로 `cd` 하세요.

### 7-2) `pip install` 실패 (네트워크/프록시)
회사/기관망이면 막힐 수 있습니다.
- 개인 네트워크(핫스팟)로 재시도
- VPN/프록시 설정 확인

### 7-3) `zsh: command not found: python`
Mac에서는 `python3`를 사용하세요.

```bash
python3 --version
python3 -m venv .venv
python3 -m streamlit run app.py
```

### 7-4) 브라우저가 자동으로 안 열림
터미널에 나온 `http://localhost:8501`를 직접 복사해서 브라우저 주소창에 입력하면 됩니다.

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
