import yfinance as yf
import pandas as pd

# Ticker ETF + aziende tech USA
tickers = {
    "SPY": "S&P 500 (New York)",
    "EWI": "FTSE MIB (Italia via ETF)",
    "EWJ": "Nikkei 225 (Giappone via ETF)",
    "EWH": "Hang Seng (HK via ETF)",
    "EWU": "FTSE 100 (UK via ETF)",
    "DAX": "DAX (Francoforte)",
    "CAC": "CAC 40 (Parigi)",
    "FIX": "Cina (generico)",
    "AAPL": "Apple",
    "AMZN": "Amazon",
    "MSFT": "Microsoft",
    "META": "Meta Platforms",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google)",
    "TSLA": "Tesla"
}

# Intervallo di date
start_date = "2025-01-01"
end_date = "2025-04-07"

# Lista per salvare i dati
dati = []

for symbol, nome in tickers.items():
    print(f"⏳ Scaricando {nome} ({symbol})...")
    df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=False)

    if not df.empty:
        df = df[["Open", "High", "Low", "Close", "Volume"]]  # Forziamo solo le colonne che ci servono
        for date, row in df.iterrows():
            try:
                open_val = float(row["Open"])
                close_val = float(row["Close"])
                if pd.notnull(open_val) and pd.notnull(close_val) and open_val != 0:
                    giornaliero = ((close_val - open_val) / open_val) * 100
                    dati.append({
                        "borsa": nome,
                        "ticker": symbol,
                        "data": date.strftime('%Y-%m-%d'),
                        "open": open_val,
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": close_val,
                        "volume": float(row["Volume"]),
                        "Giornaliero": giornaliero
                    })
            except Exception as e:
                print(f"⚠️ Errore in {symbol} il {date.strftime('%Y-%m-%d')}: {e}")
    else:
        print(f"⚠️ Nessun dato trovato per {symbol}")

# Costruiamo DataFrame
df_finale = pd.DataFrame(dati)

# Pulizia dati numerici (ridondante ma sicura)
numerici = ["open", "high", "low", "close", "volume", "Giornaliero"]
for col in numerici:
    df_finale[col] = pd.to_numeric(df_finale[col], errors="coerce")
df_finale.dropna(subset=numerici, inplace=True)

# Salva CSV
output_file = "dati_yahoo_puliti.csv"
df_finale.to_csv(output_file, index=False)
print(f"\n✅ File pulito salvato: {output_file}")
print(f"📊 Totale righe valide: {len(df_finale)}")