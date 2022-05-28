import os
import sys
from os.path import dirname, join
from typing import Optional

import aws_cdk as cdk
from constructs import Construct
from dotenv import load_dotenv


class StackProps:
    """Stack用の小道具
    全Stack用のが共通で使用する変数や関数をまとめたもの
    """

    def __init__(
        self,
        sysname: Optional[str],
        env: Optional[str],
    ):
        if not sysname:
            print("Please enter a value for SYSTEM_NAME in .env")
            sys.exit(1)
        else:
            self.__sysname = sysname

        if not env:
            print("Please enter a value for ENV in .env")
            sys.exit(1)
        else:
            self.__env = env

        """
        可変リソース名. vpcやrdsなどリソースのnameやidを取得する際の一時定義用
        各リソース名は, props.vpc().nameやprops.rds("db-app").idなどのように利用する.
        この時, vpc()では先に設定されたsysnameなどを用いてvpcのリソース名を一意に生成してnameに代入する
        """
        self.__name = ""

    @property
    def sysname(self) -> str:
        return self.__sysname

    @property
    def env(self) -> str:
        return self.__env

    @property
    def sysname_env(self) -> str:
        return f"{self.sysname}-{self.env}"

    @property
    # リソース名を取得するメソッドチェーン用Getter. リソース名はKebab型
    def name(self) -> str:
        return self.__name

    @property
    # リソースIDを取得するメソッドチェーン用Getter. リソースIDはLarge Camel型
    def id(self):
        return "".join(x.title() for x in self.__name.split("-"))

    # リソース名のうち, ハイフンで区切られた最終ブロックを除去するメソッド
    def remove_suffix(self):
        self.__name = self.__name[: self.__name.rfind("-") + 1]
        return self

    def stack(self, stack_desc: str):
        """
        スタック名を一意に生成. システム名+環境名とStackの記述(例: db-appなど)から生成.
        """
        self.__name = self.sysname_env + "-" + stack_desc + "-stack"
        return self

    def ssm_key(self, app_name: str):
        """
        SSM_Key名を一意に生成. システム名+環境名とアプリ名を利用.
        """
        self.__name = f"{self.sysname_env}-{app_name}-key"
        return self

    def vpc(self):
        """
        VPC名を一意に生成. システム名+環境名を利用.
        """
        self.__name = self.sysname_env + "-vpc"
        return self

    def subnet(self, nlayer, number=-1):
        """
        Subnet名を一意に生成. システム名+環境名, ネットワークレイヤ(例: public, private)と通し番号(なくても良い)を利用.
        """
        number_str = "-" + str(number) if number > -1 else ""
        self.__name = self.sysname_env + "-" + nlayer + "-subnet" + number_str
        return self

    def security_group(self, app_name):
        """
        Security Group名を一意に生成. システム名+環境名, SGを付与するアプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-sg"
        return self

    def s3_bucket(self, bucket_name):
        """
        S3 Bucket名を一意に生成. システム名+環境名, Bucket名を利用.
        """
        self.__name = self.sysname_env + "-" + bucket_name + "-bucket"
        return self

    def codebuild_pipeline_project(self, app_name):
        """
        CodeBuildのPipeline Project名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-codebuild-pipeline-project"
        return self

    def codepipeline(self, app_name):
        """
        CodePipeline名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-codepipeline"
        return self

    def codepipeline_source_artifact(self, app_name):
        """
        CodePipelineの生成物名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "codepipeline-source-artifact"
        return self

    def codepipeline_build_artifact(self, app_name):
        """
        CodePipelineの生成物名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-codepipeline-build-artifact"
        return self

    def secretsmanager(self, app_name):
        """
        SecretsManagerのSecrets名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-secretsmanager-secrets"
        return self

    def iam_role(self, role_name):
        """
        IamRole名を一意に生成. システム名+環境名, ロール名を付与するアプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + role_name + "-role"
        return self

    def iam_role_policy(self, policy_name):
        """
        IamRole名を一意に生成. システム名+環境名, ロール名を付与するアプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + policy_name + "-role-policy"
        return self

    def instance_profile(self, profile_name):
        """
        IamRole名を一意に生成. システム名+環境名, ロール名を付与するアプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + profile_name + "-instance-profile"
        return self

    def ecs_cluster(self):
        """
        ECS Cluster名(Fargateも)を一意に生成. システム名+環境名を利用.
        """
        self.__name = self.sysname_env + "-ecs-cluster"
        return self

    def ecr_repository(self, app_name):
        """
        ECS レポジトリ 名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-ecr-repository"
        return self

    def ecs_service(self, app_name):
        """
        ECS Service名を一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-ecs-service"
        return self

    def ecs_task_definition(self, definition_name):
        """
        ECR Task定義名を一意に生成. システム名+環境名, 定義名を利用.
        """
        self.__name = self.sysname_env + "-" + definition_name + "-ecs-task-definition"
        return self

    def ecs_container_name(self, app_name, container_name):
        """
        ECS コンテナ名を一意に生成. システム名+環境名, アプリ名, コンテナ種(appやdbなど)を付与するアプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-" + container_name + "-container"
        return self

    def log_prefix(self, app_name):
        """
        Logに付与するPrefixを一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = self.sysname_env + "-" + app_name + "-"
        return self

    def log_group(self, app_name, sub_name):
        """
        Logに付与するPrefixを一意に生成. システム名+環境名, アプリ名を利用.
        """
        self.__name = f"{self.sysname_env}-{app_name}-{sub_name}"
        return self

    def rds(self, db_name):
        """
        RDSのインスタンス名(≠ Clusterを構成するEC2インスタンス)を一意に生成. システム名+環境名, DB名を利用. Classmethodの規則と異なる点に留意.
        """
        self.__name = self.sysname_env + "-" + db_name + "-rds"
        return self

    def rds_cluster(self, db_name):
        """
        RDSクラスタ名を一意に生成. システム名+環境名, DB名を利用.
        """
        self.__name = self.sysname_env + "-" + db_name + "-cluster"
        return self

    def add_common_tags(self, scope: Construct):
        """
        スタック内のリソースに、システム名・サービス名・環境(test/stg/prd等)のタグを追加する
        """
        cdk.Tags.of(scope).add("SystemName", self.sysname)
        cdk.Tags.of(scope).add("Env", self.env)

    def add_tag(self, scope: Construct, key: str, value: str):
        """
        スタック内のリソースに、任意のタグを追加する
        """
        cdk.Tags.of(scope).add(key, value)


"""
リソース名生成処理の単体テスト用関数
"""
if __name__ == "__main__":
    dotenv_path = join(dirname(__file__), "../.env")
    load_dotenv(dotenv_path)
    props = StackProps(
        sysname=os.getenv("SYS_NAME"),
        env=os.getenv("ENV"),
    )
    stack_desc = "network"
    db_name = "db-app"
    print(props.stack(stack_desc).name)
    print(props.stack(stack_desc).id)
    print(props.ssm_key(db_name).name)
    print(props.security_group(db_name).name)
    print(props.rds(db_name).name)
    print(props.rds_cluster(db_name).name)
    print(props.rds_cluster(db_name).remove_suffix().name)
    print(props.vpc().name)
    print(props.subnet("protected").name)
    print(props.subnet("protected", 0).id)
    print(props.s3_bucket(db_name + "-pipeline").name)
    print(props.codebuild_pipeline_project(db_name).name)
    print(props.codepipeline(db_name).name)
    print(props.codepipeline_source_artifact(db_name).name)
    print(props.codepipeline_build_artifact(db_name).name)
    print(props.ecr_repository(db_name).name)
    print(props.secretsmanager(db_name).name)
    print(props.iam_role(db_name + "-full-access").name)
    print(props.ecs_cluster().name)
    print(props.ecs_service(db_name).name)
    print(props.ecs_task_definition(db_name + "-pipeline").name)
    print(props.ecs_container_name(db_name, "app").name)
    print(props.log_prefix(db_name).name)
