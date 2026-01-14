# PyJQuants

[![PyPI](https://img.shields.io/pypi/v/pyjquants.svg)](https://pypi.org/project/pyjquants/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/obichan117/pyjquants/blob/main/docs/ja/examples/quickstart_ja.ipynb)

**J-Quants APIを簡単に使えるPythonライブラリです。**

プログラミング初心者でも、数行のコードで日本株のデータを取得できます。

## PyJQuantsでできること

- 株価データの取得（日足・期間指定）
- 企業情報の検索（銘柄コード・会社名）
- 財務データの取得（決算情報）
- 市場情報の取得（TOPIX・日経225・取引カレンダー）
- 先物・オプションデータの取得（プレミアムプラン）

## 使用例

```python
import pyjquants as pjq

# トヨタ自動車の株価を取得
ticker = pjq.Ticker("7203")

# 会社名を表示
print(ticker.info.name)  # → トヨタ自動車

# 過去30日の株価を取得
df = ticker.history("30d")
print(df)
```

## プラン別機能一覧

J-Quants APIには複数のプランがあります。プランによって使える機能が異なります。

| 機能 | Free | Light | Standard | Premium |
|------|:----:|:-----:|:--------:|:-------:|
| 日足株価 | ✓* | ✓ | ✓ | ✓ |
| 企業情報・検索 | ✓* | ✓ | ✓ | ✓ |
| 財務情報（概要） | ✓* | ✓ | ✓ | ✓ |
| 取引カレンダー | ✓* | ✓ | ✓ | ✓ |
| 決算発表日 | ✓ | ✓ | ✓ | ✓ |
| 投資部門別売買状況 | - | ✓ | ✓ | ✓ |
| TOPIX | - | ✓ | ✓ | ✓ |
| 日経225 | - | - | ✓ | ✓ |
| 信用取引情報 | - | - | ✓ | ✓ |
| 空売り情報 | - | - | ✓ | ✓ |
| 業種分類 | - | - | ✓ | ✓ |
| 前場株価 | - | - | - | ✓ |
| 配当情報 | - | - | - | ✓ |
| 詳細財務情報 | - | - | - | ✓ |
| 先物・オプション | - | - | - | ✓ |

*Freeプランは12週間遅延データ

## インストール

```bash
pip install pyjquants
```

## 次のステップ

- [セットアップ](setup.md) - APIキーの取得と設定
- [基本的な使い方](basic-usage.md) - コピペで動くサンプルコード
- [プラン別ガイド](tier-guide.md) - どのプランを選ぶべきか
- [クイックスタート（Colab）](examples/quickstart_ja.ipynb) - ブラウザですぐに試せる

!!! tip "プログラミング初心者の方へ"
    [クイックスタート（Colab）](examples/quickstart_ja.ipynb)を開けば、インストール不要でブラウザ上ですぐに試せます。
