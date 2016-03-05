# ツイッターコーパス
## Requirements
* Python 3.4.3
* requests 2.9.1
* requests_oauthlib 0.6.1  

上記の依存モジュールは以下でインストールできます。  
`pip install -r requirements.txt`

## Downloads
 1. このリポジトリをクローン
 2. ツイッターの開発者登録（https://dev.twitter.com/）を行い、認証キーを入手する（参考：http://hello-apis.blogspot.jp/2013/03/twitterapi.html）
 3. OAuthKey.ini内のアスタリスクを取得した認証キー４種類に書き換える  
    CK: Consumer key, CS: Consumer secret, AT: Access Token, AS: Access Token Secret  
 4. init.pyを実行
 
上記手順で出力された`annotated.txt`がアノテーションされたツイッターコーパスです。
