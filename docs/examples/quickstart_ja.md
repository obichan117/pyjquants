# PyJQuants クイックスタート

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/examples/quickstart_ja.ipynb)

このノートブックでは、PyJQuantsを使って日本株のデータを取得する方法を紹介します。

**プログラミング初心者の方へ：** 上の「Open in Colab」ボタンをクリックすると、ブラウザ上でこのノートブックを実行できます。インストールは不要です。

---

## このノートブックの内容

1. [セットアップ](#1) - ライブラリのインストールとAPIキーの設定
2. [株価データを取得する](#2) - 基本的な株価の取得方法
3. [企業情報を調べる](#3) - 会社名・業種の確認
4. [複数銘柄を比較する](#4) - 複数の株価を一括取得
5. [市場情報を確認する](#5) - 取引カレンダー・決算発表

---

## 1. セットアップ

### 1.1 ライブラリをインストール

まず、PyJQuantsをインストールします。

（すでにインストール済みの場合はスキップされます）


```python
# PyJQuantsを最新版にインストール/アップグレード
!pip install -q pyjquants --upgrade --no-cache-dir

import pyjquants
print(f'PyJQuants v{pyjquants.__version__} インストール完了')
```

### 1.2 APIキーを設定

J-Quants APIを使うには、APIキーが必要です。

**APIキーの取得方法：**
1. [J-Quants申し込みページ](https://application.jpx-jquants.com/)でアカウントを作成（無料プランあり）
2. ログイン後、ダッシュボードでAPIキーをコピー

**Colabでの設定方法（おすすめ）：**
1. 左サイドバーの鍵アイコン🔑をクリック
2. 「新しいシークレットを追加」をクリック
3. 名前: `JQUANTS_API_KEY`、値: あなたのAPIキー
4. 「ノートブックからのアクセス」をオンにする

設定できたら、下のセルを実行してください。


```python
import os

# APIキーを探す
api_key = None

# 1. 環境変数から探す
if os.environ.get('JQUANTS_API_KEY'):
    api_key = os.environ['JQUANTS_API_KEY']
    print('✅ APIキーが環境変数に設定されています')

# 2. Colabのシークレットから探す
if not api_key:
    try:
        from google.colab import userdata
        api_key = userdata.get('JQUANTS_API_KEY')
        os.environ['JQUANTS_API_KEY'] = api_key
        print('✅ APIキーをColabシークレットから読み込みました')
    except:
        pass

# 3. 手動で入力
if not api_key:
    print('=' * 50)
    print('APIキーが見つかりません。')
    print('下にAPIキーを貼り付けてEnterを押してください：')
    print('（取得先: https://application.jpx-jquants.com/）')
    print('=' * 50)
    api_key = input('APIキー: ').strip()
    
    if api_key:
        os.environ['JQUANTS_API_KEY'] = api_key
        print('✅ APIキーを設定しました')
    else:
        print('❌ APIキーが入力されませんでした')

# 確認
if os.environ.get('JQUANTS_API_KEY'):
    key = os.environ['JQUANTS_API_KEY']
    print(f"\nAPIキーの末尾: ...{key[-4:]}")
```

### 1.3 ライブラリを読み込む

`pyjquants`を`pjq`という短い名前で読み込みます。


```python
# ライブラリを読み込む
import pyjquants as pjq

print(f'PyJQuants バージョン: {pjq.__version__}')
print('準備完了！')
```

---

## 2. 株価データを取得する

### 2.1 銘柄を指定する

株価を取得するには、まず`Ticker`オブジェクトを作成します。

銘柄コード（4桁の数字）を指定してください。


```python
# トヨタ自動車（銘柄コード: 7203）を指定
ticker = pjq.Ticker("7203")

print(f"銘柄コード: {ticker.code}")
```

### 2.2 株価を取得する

`.history()` メソッドで株価データを取得できます。

期間は以下のように指定できます：
- `"30d"` - 過去30日
- `"1w"` - 過去1週間
- `"6mo"` - 過去6ヶ月
- `"1y"` - 過去1年


```python
# 過去30日の株価を取得
df = ticker.history("30d")

# 最新5日分を表示
print(f"取得したデータ: {len(df)}日分")
print()
df[["date", "open", "high", "low", "close", "volume"]].tail()
```

**データの見方：**

| 列名 | 意味 |
|------|------|
| date | 日付 |
| open | 始値（その日最初の取引価格） |
| high | 高値（その日の最高価格） |
| low | 安値（その日の最安価格） |
| close | 終値（その日最後の取引価格） |
| volume | 出来高（取引された株数） |

### 2.3 日付を指定して取得

特定の期間を指定することもできます。


```python
# 2024年1月〜6月のデータを取得
df_custom = ticker.history(start="2024-01-01", end="2024-06-30")

print(f"取得したデータ: {len(df_custom)}日分")
print(f"期間: {df_custom['date'].min()} 〜 {df_custom['date'].max()}")
```

### 2.4 株価チャートを描く

取得したデータをグラフで可視化してみましょう。


```python
import matplotlib.pyplot as plt

# 日本語フォントを有効化（Colab用）
try:
    import japanize_matplotlib
except ImportError:
    !pip install -q japanize-matplotlib
    import japanize_matplotlib

# 1年分のデータを取得
df = ticker.history("1y")

# グラフを描画
plt.figure(figsize=(12, 6))
plt.plot(df["date"], df["close"], color="blue", linewidth=2)

# タイトルと軸ラベル
plt.title(f"{ticker.info.name} ({ticker.code}) - 株価推移", fontsize=14)
plt.xlabel("日付")
plt.ylabel("終値（円）")

# 見た目を整える
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

## 3. 企業情報を調べる

`.info` プロパティで企業情報を取得できます。


```python
# トヨタ自動車の企業情報
ticker = pjq.Ticker("7203")

print("【企業情報】")
print(f"銘柄コード: {ticker.info.code}")
print(f"会社名: {ticker.info.name}")
print(f"英語名: {ticker.info.name_english}")
print(f"業種: {ticker.info.sector}")
print(f"市場: {ticker.info.market}")
```

### 3.1 銘柄を検索する

会社名で銘柄を検索できます。


```python
# 「銀行」で検索
results = pjq.search("銀行")

print(f"「銀行」で検索: {len(results)}件ヒット")
print()
print("【検索結果（上位10件）】")
for t in results[:10]:
    print(f"  {t.code}: {t.info.name}")
```

---

## 4. 複数銘柄を比較する

`pjq.download()` で複数銘柄の株価を一括取得できます。


```python
# 4銘柄を比較
codes = [
    "7203",  # トヨタ自動車
    "6758",  # ソニーグループ
    "7974",  # 任天堂
    "9984",  # ソフトバンクグループ
]

# 30日分の終値を取得
df_multi = pjq.download(codes, period="30d")

print(f"取得したデータ: {len(df_multi)}日分 × {len(codes)}銘柄")
df_multi.tail()
```


```python
# 複数銘柄の株価チャート
plt.figure(figsize=(12, 6))

for code in codes:
    plt.plot(df_multi["date"], df_multi[code], label=code, linewidth=2)

plt.title("Stock Price Comparison", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Close Price (JPY)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

---

## 5. 市場情報を確認する

### 5.1 取引カレンダー

特定の日が取引日かどうか確認できます。


```python
from datetime import date

market = pjq.Market()

# 祝日かどうか確認
test_dates = [
    date(2024, 12, 23),  # 平日
    date(2024, 12, 25),  # クリスマス
    date(2025, 1, 1),    # 元日
]

print("【取引日の確認】")
for d in test_dates:
    is_trading = market.is_trading_day(d)
    status = "取引日" if is_trading else "休場日"
    print(f"  {d}: {status}")
```


```python
# 次の取引日を調べる
new_year = date(2025, 1, 1)
next_trading = market.next_trading_day(new_year)

print(f"{new_year} の次の取引日: {next_trading}")
```

### 5.2 決算発表カレンダー

決算発表の予定を確認できます。


```python
# 2024年10月の決算発表予定
df_earnings = market.earnings_calendar(
    start=date(2024, 10, 1),
    end=date(2024, 10, 31)
)

print(f"2024年10月の決算発表: {len(df_earnings)}件")
if len(df_earnings) > 0:
    df_earnings[["code", "company_name", "announcement_date"]].head(10)
```

### 5.3 TOPIX（Light以上）

TOPIXの株価を取得できます。

※ Light以上のプランが必要です。Freeプランではエラーになります。


```python
# TOPIX（Light以上のプランで利用可能）
try:
    topix = pjq.Index.topix()
    df_topix = topix.history("30d")
    
    print(f"TOPIX: {len(df_topix)}日分取得")
    df_topix[["date", "close"]].tail()
except Exception as e:
    print(f"エラー: {e}")
    print("※ TOPIXはLight以上のプランで利用可能です")
```

---

## まとめ

このノートブックで学んだこと：

| やりたいこと | コード |
|-------------|--------|
| 銘柄を指定 | `ticker = pjq.Ticker("7203")` |
| 株価を取得 | `ticker.history("30d")` |
| 企業情報を見る | `ticker.info.name` |
| 銘柄を検索 | `pjq.search("トヨタ")` |
| 複数銘柄を取得 | `pjq.download(["7203", "6758"], period="30d")` |
| 取引日を確認 | `market.is_trading_day(date)` |
| 決算発表を確認 | `market.earnings_calendar(start, end)` |

---

## 次のステップ

- [基本的な使い方](https://obichan117.github.io/pyjquants/ja/basic-usage/) - より詳しい使い方
- [プラン別ガイド](https://obichan117.github.io/pyjquants/ja/tier-guide/) - どのプランを選ぶべきか
- [GitHubリポジトリ](https://github.com/obichan117/pyjquants) - ソースコード・Issue報告

---

## プラン別機能一覧

| 機能 | Free | Light | Standard | Premium |
|------|:----:|:-----:|:--------:|:-------:|
| 日足株価 | ✓* | ✓ | ✓ | ✓ |
| 企業情報・検索 | ✓* | ✓ | ✓ | ✓ |
| 財務情報（概要） | ✓* | ✓ | ✓ | ✓ |
| 取引カレンダー | ✓* | ✓ | ✓ | ✓ |
| 決算発表日 | ✓ | ✓ | ✓ | ✓ |
| TOPIX | - | ✓ | ✓ | ✓ |
| 投資部門別売買状況 | - | ✓ | ✓ | ✓ |
| 日経225 | - | - | ✓ | ✓ |
| 信用取引情報 | - | - | ✓ | ✓ |
| 空売り情報 | - | - | ✓ | ✓ |
| 業種分類 | - | - | ✓ | ✓ |
| 前場株価 | - | - | - | ✓ |
| 配当情報 | - | - | - | ✓ |
| 先物・オプション | - | - | - | ✓ |

*Freeプランは12週間遅延データ
