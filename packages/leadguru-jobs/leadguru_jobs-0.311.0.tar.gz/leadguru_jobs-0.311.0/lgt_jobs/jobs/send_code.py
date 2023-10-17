from abc import ABC
from typing import Optional
from loguru import logger as log
from lgt.common.python.slack_client.web_client import SlackWebClient
from pydantic import BaseModel

from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Code
"""


class SendSlackEmailJobData(BaseBackgroundJobData, BaseModel):
    email: str
    user_agent: str
    locale: Optional[str]


class SendSlackEmailJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendSlackEmailJobData

    def exec(self, data: SendSlackEmailJobData):
        client = SlackWebClient('')
        code_sent = client.confirm_email(data.email, data.user_agent, data.locale)
        if not code_sent:
            log.warning(f'Unable to confirm code due to error: {code_sent}')
            return
