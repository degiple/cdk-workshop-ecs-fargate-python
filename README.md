# AWS CDK コンテナ構築シリーズ WebApp 開発編 with Python

AWS CDK と Python による コンテナの WebApp 構築を学ぶためのコンテンツです

- [AWS CDK コンテナ構築シリーズ WebApp 開発編 with Python](#aws-cdk-コンテナ構築シリーズ-webapp開発編-with-python)
  - [ハンズオンの準備](#ハンズオンの準備)
    - [AWS アカウント](#awsアカウント)
    - [GitPod](#gitpod)
    - [動作確認](#動作確認)
  - [ハンズオン！！](#ハンズオン)
    - [1. AWS CDK でアクセスする](#1-aws-cdk-でアクセスする)
    - [2. プライベートサブネットの追加](#2-プライベートサブネットの追加)
    - [3. WebAppStack の準備](#3-webappstackの準備)
    - [4. WebAppStack の修正とデプロイ](#4-webappstackの修正とデプロイ)
    - [5. コンテナイメージの変更](#5-コンテナイメージの変更)
  - [ハンズオンの終了](#ハンズオンの終了)
    - [CDK でデプロイしたリソースの削除](#cdkでデプロイしたリソースの削除)
    - [CloudFormation](#cloudformation)
    - [Dynamodb](#dynamodb)
    - [IAM](#iam)
  - [CDK help](#cdk-help)

## ハンズオンの準備

環境準備に不安な方向け

### AWS アカウント

AWS アカウントをご準備下さい
[AWS にサインアップ](https://portal.aws.amazon.com/billing/signup?refid=ps_a134p000006gta5aae&trkcampaign=acq_paid_search_brand&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation&language=ja_jp#/start)

もし新規作成される場合、クレジットカードの登録が必要になりますが、今回のハンズオンでは無料枠の範囲となりますので、過度な操作をしない限り、支払いは不要となる見込みです。

### GitPod

このコンテンツでは、GitPod の利用を推奨しています。

以下の手順に従って、GitPod の準備を行なって下さい。

1. [GitHub アカウントを作成する](https://pengi-n.co.jp/blog/github-account/)
1. Chrome 拡張機能 [Gitpod - Always ready to code](https://chrome.google.com/webstore/detail/gitpod-always-ready-to-co/dodmmooeoklaejobgleioelladacbeki) をインストールする。
1. [cdk-workshop-ecs-fargate-python](https://github.com/degiple/cdk-workshop-ecs-fargate-python) にアクセスし、表示されている Gitpod ボタンをクリックする。
1. 作成した GitHub アカウントでログインし、GitHub と GitPod の連携を承認する。
1. ブラウザで IDE が起動される。
1. [AWS CLI の手順](https://cdkworkshop.com/15-prerequisites/200-account.html)に沿って、IDE で CLI のクレデンシャルを設定する。

### 動作確認

以下コマンドを実行し、それぞれ正常終了することを確認して下さい。

- aws 認証情報が正しいかどうか

```shell
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
```

- cdk コマンドが正しく動作するかどうか

```shell
$ cdk list
cocrea-dev-network-stack
```

## ハンズオン！！

さて、これからあなたには AWS ECS fargate で、任意のコンテナを立ち上げて頂きます。

ただ、どうやらソースコードに不具合があるようなので、あなたはそれらを解決する必要があります。

### 1. AWS CDK でアクセスする

AWS CDK で あなたの AWS アカウント にアクセスしたいのですが、どうやら設定値がおかしいようです…

- 以下コマンドを実行し、エラー内容を確認して、何とか正常終了させて下さい

```shell
$ cdk bootstrap
```

### 2. プライベートサブネットの追加

それでは VPC ネットワークを作成しましょう！

ただ、現在のコードではバプリックネットワークしか作成されません…

- AWS ECS fargate をデプロイするために、プライベートサブネットを作成するコードを追加し、以下コマンドでデプロイして下さい
- サブネットの名前にも注意して下さいね！

```shell
$ cdk deploy cocrea-dev-network-stack
```

### 3. WebAppStack の準備

ネットワークは正常に作成できましたでしょうか？

次に、サンプルのコンテナを AWS ECS fargate でデプロイしましょう！

ただ、ECS fargate 用のスタックは[このファイル](stacks/webapp.py)で準備されているようですが、どうやら aws cdk で認識されていないようです…

- [app.py](app.py)を修正し、cdk list を実行した時に、以下２つのスタックが表示されるようにして下さい

```shell
$ cdk list
cocrea-dev-network-stack
cocrea-dev-webapp-stack
```

### 4. WebAppStack の修正とデプロイ

さて、それでは AWS ECS fargate をデプロイしましょう！

上手くいけばよいのですが、もしかしたら何かコードに誤りがあるかもしれません…

```shell
$ cdk deploy cocrea-dev-webapp-stack
```

正常にデプロイされれば10分程度で完了し、アクセス URL が発行されます！（なかなか完了しない場合は、ECSでコンテナが作成・廃棄され続けてるかも…）

<img width="1171" alt="image" src="https://user-images.githubusercontent.com/65447508/174446575-be92c314-00c8-45fb-a8bf-dba84aeb5932.png">

### 5. コンテナイメージの変更

無事に AWS ECS fargate はデプロイされましたでしょうか！？

上手く出来た方は、少し構成を変えてみましょう！

- 表示される Web 画面を [Nginx](https://www.nginx.co.jp/) に変更してください

<img width="529" alt="image" src="https://user-images.githubusercontent.com/65447508/174446860-13d1b2f9-29d3-4238-9524-ae47226a404a.png">

## ハンズオンの終了

お疲れ様でした！

最後に、AWS リソースの削除を忘れないようにして下さいね！

### CDK でデプロイしたリソースの削除

```shell
$ cdk destroy --all
```

### CloudFormation

[スタック](https://ap-northeast-1.console.aws.amazon.com/cloudformation/home)にて、CDK Toolkit を削除して下さい。
（もし今後作業する予定がある方は、そのままで大丈夫です）

<img width="898" alt="image" src="https://user-images.githubusercontent.com/65447508/174463081-0337e064-a020-44c7-936a-0a5c97597adb.png">

### Dynamodb

もし[テーブル](https://ap-northeast-1.console.aws.amazon.com/dynamodbv2/home)が残った場合、以下の手順で削除可能です。

<img width="911" alt="image" src="https://user-images.githubusercontent.com/65447508/174463077-2c59088b-c338-4e67-8f6a-080c510530be.png">

### IAM

ユーザー（[cdk-workshop](https://console.aws.amazon.com/iam/home#/users/cdk-workshop)）は削除されませんので、不要な方は削除お願いします。

## CDK help

シンプルですが、タブ補完も実装しています！

```shell
Usage: cdk -a <cdk-app> COMMAND

Commands:
  cdk list [STACKS..]             Lists all stacks in the app      [aliases: ls]
  cdk synthesize [STACKS..]       Synthesizes and prints the CloudFormation
                                  template for this stack       [aliases: synth]
  cdk bootstrap [ENVIRONMENTS..]  Deploys the CDK toolkit stack into an AWS
                                  environment
  cdk deploy [STACKS..]           Deploys the stack(s) named STACKS into your
                                  AWS account
  cdk import [STACK]              Import existing resource(s) into the given
                                  STACK
  cdk watch [STACKS..]            Shortcut for 'deploy --watch'
  cdk destroy [STACKS..]          Destroy the stack(s) named STACKS
  cdk diff [STACKS..]             Compares the specified stack with the deployed
                                  stack or a local template file, and returns
                                  with status 1 if any difference is found
  cdk metadata [STACK]            Returns all metadata associated with this
                                  stack
  cdk acknowledge [ID]            Acknowledge a notice so that it does not show
                                  up anymore                      [aliases: ack]
  cdk notices                     Returns a list of relevant notices
  cdk init [TEMPLATE]             Create a new, empty CDK project from a
                                  template.
  cdk context                     Manage cached context values
  cdk docs                        Opens the reference documentation in a browser
                                                                  [aliases: doc]
  cdk doctor                      Check your set-up for potential problems
```
