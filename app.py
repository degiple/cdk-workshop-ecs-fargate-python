#!/usr/bin/env python3

import aws_cdk as cdk

from stacks.common import StackProps
from stacks.network import VpcStack

# コンストラクト生成
app = cdk.App()

##############################
# Configration
##############################

# 外部パラメータの取得（cdk.jsonに記載したパラメータを参照）
props = StackProps(
    sysname=app.node.try_get_context("sysname"),
    stage=app.node.try_get_context("stage"),
)

account = app.node.try_get_context("account")
region = app.node.try_get_context("region")
env = cdk.Environment(account=account, region=region)


##############################
# Deploy stacks
##############################

# ネットワークのデプロイ
network = VpcStack(
    app, construct_id=f"{props.sys_stage}-network-stack", props=props, env=env
)


app.synth()
