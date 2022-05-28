#!/usr/bin/env python3
import os
from os.path import dirname, join

import aws_cdk as cdk
from dotenv import load_dotenv

from stacks.network import VpcStack
# from stacks.webapp import WebAppStack

##############################
# Configration
##############################

# 環境変数の読み込み
dotenv_path = join(dirname(__file__), "./.env")
load_dotenv(dotenv_path)

# 環境
env = cdk.Environment(account=os.getenv("AWS_ACCOUNT"), region=os.getenv("AWS_REGION"))

# リソース名
sysname = os.getenv("SYS_NAME")

##############################
# Deploy stacks
##############################

app = cdk.App()

network = VpcStack(app, construct_id=f"{sysname}-network-stack", sysname=sysname)

# webapp = WebAppStack(app, construct_id=f"{sysname}-webapp-stack", vpc=network.vpc)  # 問題にする


app.synth()
