import datetime as dt
from typing import Dict

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BASE_URL = "https://fapi.binance.com"
FUTURES_DATA_URL = "https://fapi.binance.com/futures/data"

INTERVAL_TO_PERIOD = {
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
}


@st.cache_data(ttl=60)
def get_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    raw = response.json()
    frame = pd.DataFrame(
        raw,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )
    frame["timestamp"] = pd.to_datetime(frame["close_time"], unit="ms", utc=True)
    frame["mark_price"] = pd.to_numeric(frame["close"], errors="coerce")
    return frame[["timestamp", "mark_price"]]


@st.cache_data(ttl=60)
def get_open_interest(symbol: str, period: str, limit: int) -> pd.DataFrame:
    url = f"{BASE_URL}/futures/data/openInterestHist"
    params = {"symbol": symbol, "period": period, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    raw = response.json()
    frame = pd.DataFrame(raw)
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", "open_interest"])

    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
    frame["open_interest"] = pd.to_numeric(frame["sumOpenInterest"], errors="coerce")
    return frame[["timestamp", "open_interest"]]


@st.cache_data(ttl=60)
def get_taker_flow(symbol: str, period: str, limit: int) -> pd.DataFrame:
    url = f"{FUTURES_DATA_URL}/takerlongshortRatio"
    params = {"symbol": symbol, "period": period, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    raw = response.json()
    frame = pd.DataFrame(raw)
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", "buy_sell_ratio", "buy_volume", "sell_volume", "net_flow"])

    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
    frame["buy_sell_ratio"] = pd.to_numeric(frame["buySellRatio"], errors="coerce")
    frame["buy_volume"] = pd.to_numeric(frame["buyVol"], errors="coerce")
    frame["sell_volume"] = pd.to_numeric(frame["sellVol"], errors="coerce")
    frame["net_flow"] = frame["buy_volume"] - frame["sell_volume"]
    return frame[["timestamp", "buy_sell_ratio", "buy_volume", "sell_volume", "net_flow"]]


@st.cache_data(ttl=60)
def get_global_long_short_ratio(symbol: str, period: str, limit: int) -> pd.DataFrame:
    url = f"{FUTURES_DATA_URL}/globalLongShortAccountRatio"
    params = {"symbol": symbol, "period": period, "limit": limit}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    raw = response.json()
    frame = pd.DataFrame(raw)
    if frame.empty:
        return pd.DataFrame(columns=["timestamp", "long_short_ratio"])

    frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
    frame["long_short_ratio"] = pd.to_numeric(frame["longShortRatio"], errors="coerce")
    return frame[["timestamp", "long_short_ratio"]]


def merge_frames(frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    valid_frames = [f for f in frames.values() if not f.empty]
    if not valid_frames:
        return pd.DataFrame()

    merged = valid_frames[0]
    for frame in valid_frames[1:]:
        merged = merged.merge(frame, on="timestamp", how="outer")

    return merged.sort_values("timestamp")


def main() -> None:
    st.set_page_config(page_title="Binance Futures Dashboard", layout="wide")
    st.title("📊 Binance Futures Indicator Dashboard")
    st.caption("선물 시장 지표 + 순매수/순매도 흐름을 한눈에 확인합니다.")

    with st.sidebar:
        st.header("설정")
        symbol = st.text_input("심볼", "BTCUSDT").upper().strip()
        interval = st.selectbox("기간", list(INTERVAL_TO_PERIOD.keys()), index=2)
        limit = st.slider("데이터 개수", min_value=30, max_value=500, value=200, step=10)

    period = INTERVAL_TO_PERIOD[interval]

    try:
        mark = get_klines(symbol, interval, limit)
        oi = get_open_interest(symbol, period, limit)
        taker = get_taker_flow(symbol, period, limit)
        ratio = get_global_long_short_ratio(symbol, period, limit)
    except requests.HTTPError as exc:
        st.error(f"Binance API 요청 실패: {exc}")
        st.stop()
    except requests.RequestException as exc:
        st.error(f"네트워크 오류: {exc}")
        st.stop()

    merged = merge_frames({"mark": mark, "oi": oi, "taker": taker, "ratio": ratio})
    if merged.empty:
        st.warning("조회된 데이터가 없습니다. 심볼/기간을 변경해 주세요.")
        st.stop()

    latest = merged.dropna(how="all").iloc[-1]
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Mark Price", f"{latest.get('mark_price', float('nan')):,.2f}")
    c2.metric("Open Interest", f"{latest.get('open_interest', float('nan')):,.2f}")
    c3.metric("Net Taker Flow", f"{latest.get('net_flow', float('nan')):,.2f}")
    c4.metric("Long/Short Ratio", f"{latest.get('long_short_ratio', float('nan')):,.3f}")

    st.subheader("가격 & 오픈이자")
    fig_price = px.line(merged, x="timestamp", y=["mark_price", "open_interest"], template="plotly_white")
    st.plotly_chart(fig_price, use_container_width=True)

    st.subheader("순매수/순매도 (Net Taker Flow)")
    fig_flow = px.bar(
        merged,
        x="timestamp",
        y="net_flow",
        color="net_flow",
        color_continuous_scale=["#ef4444", "#22c55e"],
        template="plotly_white",
    )
    st.plotly_chart(fig_flow, use_container_width=True)

    st.subheader("매수/매도 비율 & 글로벌 롱/숏 비율")
    fig_ratio = px.line(
        merged,
        x="timestamp",
        y=["buy_sell_ratio", "long_short_ratio"],
        template="plotly_white",
    )
    st.plotly_chart(fig_ratio, use_container_width=True)

    st.caption(f"마지막 업데이트: {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")


if __name__ == "__main__":
    main()
