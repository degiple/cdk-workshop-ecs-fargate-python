
# AWS CDK コンテナ構築シリーズ WebApp開発編 with Python

AWS CDK と Python による コンテナのWebApp構築を学ぶためのコンテンツです

## ハンズオンの準備

環境準備に不安な方向け

###AWSアカウント

AWSアカウントをご準備下さい
[AWS にサインアップ](https://portal.aws.amazon.com/billing/signup?refid=ps_a134p000006gta5aae&trkcampaign=acq_paid_search_brand&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation&language=ja_jp#/start)

もし新規作成される場合、クレジットカードの登録が必要になりますが、今回のハンズオンでは無料枠の範囲となりますので、過度な操作をしない限り、支払いは不要となる見込みです。

### GitPod

このコンテンツでは、GitPodの利用を推奨しています。

以下の手順に従って、GitPodの準備を行なって下さい。

1. [GitHubアカウントを作成する](https://pengi-n.co.jp/blog/github-account/)
1. Chrome拡張機能 [Gitpod - Always ready to code](https://chrome.google.com/webstore/detail/gitpod-always-ready-to-co/dodmmooeoklaejobgleioelladacbeki) をインストールする。
1. [cdk-workshop-ecs-fargate-python](https://github.com/degiple/cdk-workshop-ecs-fargate-python) にアクセスし、表示されている Gitpod ボタンをクリックする。
1. 作成したGitHubアカウントでログインし、GitHubとGitPodの連携を承認する。
1. ブラウザでIDEが起動される。
1. [AWS CLIの手順](https://cdkworkshop.com/15-prerequisites/200-account.html)に沿って、IDEでCLIのクレデンシャルを設定する。


### AWSの動作確認

以下コマンドを実行し、それぞれ正常終了することを確認して下さい。

```shell
# aws認証情報が正しいかどうか
$ aws iam list-users
{
    "Users": [
        {
            "Path": "/",
            "UserName": "~",
            "UserId": "~",
            "Arn": "~",
            "CreateDate": "~"
        },
        ~
    ]
}

# cdkコマンドが正しく動作するかどうか
$ cdk list
cocrea-dev-network-stack
```

## ハンズオン！！

さて、これからあなたには AWS ECS fargate で、任意のコンテナを立ち上げて頂きます。

ただ、どうやらソースコードに不具合があるようなので、あなたはそれらを解決する必要があります。

### 1. AWS CDK でアクセスする

AWS CDK で あなたのAWSアカウント にアクセスしたいのですが、どうやら設定値がおかしいようです…

以下コマンドを実行し、エラー内容を確認して、何とか正常終了させて下さい！

```shell
cdk bootstrap
```

### 2. プライベートサブネットの追加

それではVPCネットワークを作成しましょう！

ただ、現在のコードではバプリックネットワークしか作成されません…

AWS ECS をデプロイするのに最適なプライベートサブネットを追加するコードを追加して、以下コマンドを実行して下さい！

```shell
# VPCネットワークのデプロイ
cdk deploy cocrea-dev-network-stack
```

### 3. WebAppStackの準備

ネットワークが準備出来たので、まずはサンプルのコンテナを AWS ECS fargate でデプロイしましょう！

ECSのコード自体は[このファイル](stacks/webapp.py)で準備されているようですが、どうやら aws cdk で認識されていないようです…

[app.py](app.py)を修正し、cdk list を実行した時に、WebApp用のスタックが表示されるようにして下さい。

```shell
# WebApp用のスタックが追加で表示されているか？
cdk list
cocrea-dev-network-stack
cocrea-dev-webapp-stack
```

### 4. WebAppStackの修正とデプロイ

さて、それでは AWS ECS fargate をデプロイしましょう！

上手くいけばよいのですが、もしかしたら何かコードに誤りがあるかもしれません…


```shell
# VPCネットワークのデプロイ
cdk deploy cocrea-dev-webapp-stack
```

もし正常にデプロイされれば、アクセスURLが発行されます！


###  5. コンテナイメージの変更

無事に AWS ECS fargate はデプロイされましたでしょうか！？

最後にお願いなのですが、表示されるWeb画面を [Nginx](https://www.nginx.co.jp/) に変更してほしいです！


# Useful commands

 * `cdk list`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
