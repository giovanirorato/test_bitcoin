import argparse
import pandas as pd
import requests
import yfinance as yf


def fetch_available_tickers() -> list[str]:
    """Retrieve all B3 tickers using the brapi.dev API."""
    url = "https://brapi.dev/api/available"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("stocks", [])


def fetch_dividends(ticker: str) -> pd.DataFrame:
    """Fetch dividend history for a ticker from Yahoo Finance."""
    data = yf.Ticker(ticker)
    dividends = data.dividends
    df = dividends.to_frame(name="dividend")
    df.index.name = "date"
    df.reset_index(inplace=True)
    df.insert(0, "ticker", ticker)
    return df

def filter_tickers(
    tickers: list[str],
    min_yield: float,
    max_pe: float | None = None,
    max_payout: float | None = None,
) -> list[str]:
    """Return tickers that satisfy the given financial filters."""
    selected: list[str] = []
    for t in tickers:
        try:
            info = yf.Ticker(f"{t}.SA").info
            dy = info.get("trailingAnnualDividendYield")
            if dy is None or dy < min_yield:
                continue
            if max_pe is not None:
                pe = info.get("trailingPE")
                if pe is None or pe > max_pe:
                    continue
            if max_payout is not None:
                payout = info.get("payoutRatio")
                if payout is None or payout > max_payout:
                    continue
            selected.append(f"{t}.SA")
        except Exception as e:
            print(f"Erro ao obter info de {t}: {e}")
    return selected


def main(
    output: str,
    min_yield: float = 0.06,
    max_pe: float | None = None,
    max_payout: float | None = None,
) -> None:
    tickers = fetch_available_tickers()
    filtered = filter_tickers(tickers, min_yield, max_pe, max_payout)
    frames = []
    for t in filtered:
        try:
            df = fetch_dividends(t)
            frames.append(df)
        except Exception as e:
            print(f"Erro ao baixar dados de {t}: {e}")
    if frames:
        result = pd.concat(frames)
        result.to_csv(output, index=False)
        print(f"Dados salvos em {output}")
    else:
        print("Nenhum dado coletado.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Baixa dividendos de ações da B3 com filtro de dividend yield"
    )
    parser.add_argument(
        "--output",
        default="dividends.csv",
        help="Arquivo CSV de saída",
    )
    parser.add_argument(
        "--min-yield",
        type=float,
        default=0.06,
        help="Dividend yield mínimo (ex.: 0.06 = 6%)",
    )
    parser.add_argument(
        "--max-pe",
        type=float,
        default=None,
        help="PE máximo opcional",
    )
    parser.add_argument(
        "--max-payout",
        type=float,
        default=None,
        help="Payout ratio máximo opcional",
    )
    args = parser.parse_args()
    main(args.output, args.min_yield, args.max_pe, args.max_payout)
