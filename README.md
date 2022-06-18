
# AWS CDK コンテナ構築シリーズ WebApp開発編 with Python

AWS CDK と Python による コンテナのWebApp構築を学ぶためのコンテンツです

# ハンズオンの準備

環境準備に不安な方向け

## AWSアカウント

AWSアカウントをご準備下さい
[AWS にサインアップ](https://portal.aws.amazon.com/billing/signup?refid=ps_a134p000006gta5aae&trkcampaign=acq_paid_search_brand&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation&language=ja_jp#/start)

もし新規作成される場合、クレジットカードの登録が必要になりますが、今回のハンズオンでは無料枠の範囲となりますので、過度な操作をしない限り、支払いは不要となる見込みです。

## GitPod

このコンテンツでは、GitPodの利用を推奨しています。

以下の手順に従って、GitPodの準備を行なって下さい。

1. [GitHubアカウントを作成する](https://pengi-n.co.jp/blog/github-account/)
1. Chrome拡張機能 [Gitpod - Always ready to code](https://chrome.google.com/webstore/detail/gitpod-always-ready-to-co/dodmmooeoklaejobgleioelladacbeki) をインストールする。
1. [cdk-workshop-ecs-fargate-python](https://github.com/degiple/cdk-workshop-ecs-fargate-python) にアクセスし、表示されている Gitpod ボタンをクリックする。
1. 作成したGitHubアカウントでログインし、GitHubとGitPodの連携を承認する。
1. ブラウザでIDEが起動される。
1. [AWS CLIの手順](https://cdkworkshop.com/15-prerequisites/200-account.html)に沿って、IDEでCLIのクレデンシャルを設定する。


## AWS CDK の動作確認

以下コマンドを実行し、正常終了することを確認して下さい。

```shell
$ cdk bootstrap
```

# Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
