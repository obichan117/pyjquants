# 基本的な使い方

このページでは、PyJQuantsの基本的な使い方を紹介します。
コードはそのままコピー＆ペーストで動きます。

## 株価データを取得する

### 単一銘柄の株価

```python
import pyjquants as pjq

# トヨタ自動車（銘柄コード: 7203）
ticker = pjq.Ticker("7203")

# 過去30日の株価を取得
df = ticker.history("30d")
print(df)
```

出力例：
```
        date     open     high      low    close    volume
0 2024-12-01  2850.0   2875.0   2840.0   2860.0   5000000
1 2024-12-02  2865.0   2890.0   2855.0   2880.0   4500000
...
```

### 期間を指定して取得

```python
# いろいろな期間指定
df = ticker.history("30d")   # 過去30日
df = ticker.history("1w")    # 過去1週間
df = ticker.history("6mo")   # 過去6ヶ月
df = ticker.history("1y")    # 過去1年
```

### 日付を指定して取得

```python
from datetime import date

# 2024年1月1日〜6月30日のデータ
df = ticker.history(start="2024-01-01", end="2024-06-30")

# dateオブジェクトでも指定可能
df = ticker.history(
    start=date(2024, 1, 1),
    end=date(2024, 6, 30)
)
```

## 企業情報を取得する

```python
ticker = pjq.Ticker("7203")

# 会社名
print(ticker.info.name)           # → トヨタ自動車
print(ticker.info.name_english)   # → Toyota Motor Corporation

# 業種・市場
print(ticker.info.sector)         # → 輸送用機器
print(ticker.info.market)         # → プライム
```

## 銘柄を検索する

```python
# 会社名で検索
results = pjq.search("トヨタ")
for t in results[:5]:
    print(f"{t.code}: {t.info.name}")

# 出力例：
# 7203: トヨタ自動車
# 7262: ダイハツ工業
# ...
```

## 複数銘柄を一括取得

```python
# 複数銘柄の終値を一括取得
codes = ["7203", "6758", "7974", "9984"]  # トヨタ、ソニー、任天堂、ソフトバンク

df = pjq.download(codes, period="30d")
print(df)
```

出力例：
```
        date     7203     6758     7974     9984
0 2024-12-01  2860.0  13500.0   8200.0   9100.0
1 2024-12-02  2880.0  13600.0   8250.0   9150.0
...
```

## 財務情報を取得する

```python
ticker = pjq.Ticker("7203")

# 財務諸表（決算情報）
df = ticker.financials
print(df[["disclosure_date", "net_sales", "operating_profit"]])
```

## 市場情報を取得する

### 取引カレンダー

```python
from datetime import date

market = pjq.Market()

# 特定の日が取引日かどうか確認
print(market.is_trading_day(date(2024, 12, 25)))  # → False（祝日）

# 次の取引日を取得
next_day = market.next_trading_day(date(2025, 1, 1))
print(next_day)  # → 2025-01-06
```

### 決算発表カレンダー

```python
from datetime import date

market = pjq.Market()

# 10月の決算発表予定を取得
df = market.earnings_calendar(
    start=date(2024, 10, 1),
    end=date(2024, 10, 31)
)
print(df[["code", "company_name", "announcement_date"]])
```

## TOPIX・日経225

```python
# TOPIX（Light以上のプランで利用可能）
topix = pjq.Index.topix()
df = topix.history("30d")
print(df)

# 日経225（Standard以上のプランで利用可能）
nikkei = pjq.Index.nikkei225()
df = nikkei.history("30d")
print(df)
```

## 株価チャートを描く

```python
import matplotlib.pyplot as plt

ticker = pjq.Ticker("7203")
df = ticker.history("1y")

# 日本語フォント設定（Mac）
plt.rcParams['font.family'] = 'Hiragino Sans'

plt.figure(figsize=(12, 6))
plt.plot(df["date"], df["close"])
plt.title(f"{ticker.info.name}（{ticker.code}）株価推移")
plt.xlabel("日付")
plt.ylabel("終値（円）")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## 次のステップ

- [プラン別ガイド](tier-guide.md) - より多くの機能を使うには
- [クイックスタート（Colab）](examples/quickstart_ja.ipynb) - ブラウザで実際に試す
