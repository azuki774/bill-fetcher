# bill-fetcher

## money-forward
- https://moneyforward.com に自動的にログインして、指定したURLのHTMLソースを取得して保存する。
### Usage
- `deploymments/compose.yml` と `money-forward.yml` の要領で、コンテナ `bill-fetcher-money-forward` を起動させる。
- 取得したいリンクと、必要に応じて金融機関連携の「更新」ボタンの XPATH を環境変数で渡す。

## money-forward API
- https://moneyforward.com に自動的にログインして、APIサーバを起動させる(:8080)。下のエンドポイントを叩くと、自動的にサイトからデータを取得・操作する
    - `GET /moneyforaward/cf`
       - 入出金の家計簿ページで今月のデータを返す
    - `GET /moneyforaward/cf/lastmonth`
       - 入出金の家計簿ページで先月のデータを返す
    - `GET /moneyforaward/cf/status`
       - 金融機関連携のステータスを返す
    - `PUT  /moneyforaward/cf/status`
       - 金融機関連携の「更新」ボタンを押す
     
- driver が1つしかないため、データ取得中にさらにAPIアクセスがあると、503が返るようになっているはず。

### Usage
- `deploymments/compose.yml` と `api.yml` の要領で、コンテナ `bill-fetcher-api` を起動させる。

## データ取り込み例
- [mf-importer](https://github.com/azuki774/mf-importer)

### それ以外はおまけ
