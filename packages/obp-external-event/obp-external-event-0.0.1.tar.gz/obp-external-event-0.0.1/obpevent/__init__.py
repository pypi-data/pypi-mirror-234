import os
import json
from subprocess import check_call


class OBPEvent:
    def __init__(self, webhook_url=None, role_arn=None, obp_token=None):
        if webhook_url is not None:
            os.environ["METAFLOW_ARGO_EVENTS_WEBHOOK_URL"] = webhook_url
            os.environ["METAFLOW_ARGO_EVENTS_WEBHOOK_AUTH"] = "service"
        env = os.environ.copy()
        env.update(self._assume_role(role_arn))
        check_call(["outerbounds", "configure", "-f", obp_token], env=env)

    def _assume_role(self, role_arn):
        import boto3

        sts_client = boto3.client("sts")

        assumed_role_object = sts_client.assume_role(
            RoleArn=role_arn, RoleSessionName="send_event"
        )

        credentials = assumed_role_object["Credentials"]
        return {
            "AWS_ACCESS_KEY_ID": credentials["AccessKeyId"],
            "AWS_SECRET_ACCESS_KEY": credentials["SecretAccessKey"],
            "AWS_SESSION_TOKEN": credentials["SessionToken"],
        }

    def submit(self, event_name, payload=None):
        from metaflow.integrations import ArgoEvent

        ArgoEvent(name=event_name).publish(payload=payload)
