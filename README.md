# bill-fetcher

## money-forward
- https://moneyforward.com に自動的にログインして、指定したURLのHTMLソースを取得して保存する。
- 出力先は、コンテナ内の `/data/latest/＜各種ページ＞
- 取得したいリンクと、必要に応じて金融機関連携の「更新」ボタンの XPATH を環境変数で渡す。

## sbi
- https://site1.sbisec.co.jp/ETGate/ に自動的にログインして、ポートフォリオの表ごとに保存する。
- 出力先は、コンテナ内の `/data/YYYYMMDD/YYYYMMDD_x.csv`
    - `x`: 連番

## データ取り込み例
- [mf-importer](https://github.com/azuki774/mf-importer)

### それ以外はおまけ
