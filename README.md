# bill-fetcher

## money-forward
- https://moneyforward.com に自動的にログインして、指定したURLのHTMLソースを取得して保存する。
### Usage
- `deploymments/compose.yml` と `money-forward.yml` の要領で、コンテナ `bill-fetcher-money-forward` を起動させる。
- 取得したいリンクと、必要に応じて金融機関連携の「更新」ボタンの XPATH を環境変数で渡す。

## データ取り込み例
- [mf-importer](https://github.com/azuki774/mf-importer)

### それ以外はおまけ
