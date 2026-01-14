# セットアップ

PyJQuantsを使うには、J-Quants APIの「APIキー」が必要です。

## APIキーとは？

APIキーは、J-Quantsのサービスにアクセスするための「パスワード」のようなものです。
アカウントを作成すると、自分専用のAPIキーが発行されます。

!!! warning "APIキーは秘密にしてください"
    APIキーは他人に教えないでください。悪用されると、あなたのアカウントで不正なアクセスが行われる可能性があります。

## ステップ1: J-Quantsアカウントを作成

1. [J-Quants申し込みページ](https://application.jpx-jquants.com/)にアクセス
2. 「新規登録」をクリック
3. メールアドレスとパスワードを入力
4. 利用規約に同意して登録

!!! note "Freeプランは無料"
    まずはFreeプラン（無料）で試すことができます。12週間遅延データですが、学習には十分です。

## ステップ2: APIキーを取得

1. [J-Quantsダッシュボード](https://application.jpx-jquants.com/)にログイン
2. 「APIキー」のセクションを探す
3. APIキーをコピー（`xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`のような文字列）

## ステップ3: APIキーを設定

### 方法A: 環境変数で設定（おすすめ）

ターミナル（コマンドプロンプト）で以下を実行：

=== "Mac / Linux"
    ```bash
    export JQUANTS_API_KEY="あなたのAPIキー"
    ```

=== "Windows (PowerShell)"
    ```powershell
    $env:JQUANTS_API_KEY = "あなたのAPIキー"
    ```

=== "Windows (コマンドプロンプト)"
    ```cmd
    set JQUANTS_API_KEY=あなたのAPIキー
    ```

### 方法B: Google Colabで設定

Colabを使う場合は、「シークレット」機能を使うと便利です：

1. Colabノートブックの左サイドバーで鍵アイコンをクリック
2. 「新しいシークレットを追加」をクリック
3. 名前: `JQUANTS_API_KEY`、値: あなたのAPIキー
4. 「ノートブックからのアクセス」をオンにする

## ステップ4: 動作確認

Pythonで以下を実行して、正しく設定できたか確認します：

```python
import pyjquants as pjq

# トヨタ自動車の情報を取得
ticker = pjq.Ticker("7203")
print(ticker.info.name)  # → トヨタ自動車
```

「トヨタ自動車」と表示されれば成功です！

## よくあるエラー

### 「JQUANTS_API_KEY not set」と表示される

APIキーが設定されていません。ステップ3を再確認してください。

### 「401 Unauthorized」と表示される

APIキーが間違っています。コピーミスがないか確認してください。

### 「403 Forbidden」と表示される

その機能はあなたのプランでは使えません。[プラン別ガイド](tier-guide.md)で、どの機能がどのプランで使えるか確認してください。

## 次のステップ

- [基本的な使い方](basic-usage.md) - 実際にデータを取得してみる
- [プラン別ガイド](tier-guide.md) - プランのアップグレードを検討する
