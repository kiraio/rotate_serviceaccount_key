
# 概要
- Googleが提唱している[サービス アカウントキーの作成と管理](https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=JA)に従い、ユーザーが作成したサービアカウントの鍵をローテーションするためのCloud Functionsのプログラムになります

# コードについて
## バージョン
- v0.1

## コード
- python 3.8

## 提供機能
- 指定のサービスアカウントでユーザーが作成した鍵を「削除」→「新規作成」→「GCSへアップロード」する

## 現行仕様
- Cloud Functionsのデフォルトサービスアカウントに対して以下のIAMロールを付与する必要あり
  - 「サービス アカウント ユーザー」
  - 「Storage オブジェクト作成者」

## 定期バッチ処理を行いたい場合
- Cloud SchedulerにてCloud Funtionsで作成した関数を定期実行するように設定すれば可能

## 利用方法
1. cloud functionsの管理コンソールにて「関数作成」をクリック
2. 以下の設定を行い、「次へ」ボタンをクリック  
    2.1 関数名の設定： 特に要件がなければ「RotateSaKey」
    2.2 リージョンを設定： 特に要件がなければ「asia-northeast01」
    2.3 トリガーを設定： 特に要件がなければ「HTTP」
3. 関数が作成されたら「main.py」と「requirements.txt」を本リポジトリーのコードに書き換える
4. 「デプロイ」ボタンをクリック
5. 正しく実行出来ているか”テスト”タブを開き、「関数をテスト」ボタンをクリック
6. 正常に実行が完了されると `{"message":"success"}` と表示される
