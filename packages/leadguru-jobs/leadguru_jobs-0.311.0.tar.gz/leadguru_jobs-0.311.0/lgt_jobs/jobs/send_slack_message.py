import datetime
from abc import ABC
from typing import Optional
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.web_client import SlackWebClient, SlackMessageConvertService
from lgt_data.mongo_repository import (UserMongoRepository, UserLeadMongoRepository,
                                       DedicatedBotRepository, UserContactsRepository)
from pydantic import BaseModel
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Message
"""


class SendSlackMessageJobData(BaseBackgroundJobData, BaseModel):
    lead_id: str
    user_id: str
    text: Optional[str]
    files_ids: Optional[list]


class SendSlackMessageJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendSlackMessageJobData

    def exec(self, data: SendSlackMessageJobData):
        user_leads_repository = UserLeadMongoRepository()
        user = UserMongoRepository().get(data.user_id)
        lead = user_leads_repository.get_lead(user_id=data.user_id, lead_id=data.lead_id)
        if not lead:
            return

        bot = DedicatedBotRepository().get_by_user_and_source_id(user.id, lead.message.source.source_id)
        if not bot or bot.invalid_creds:
            return

        slack_client = SlackWebClient(bot.token, bot.cookies)
        resp = slack_client.im_open(lead.message.sender_id)
        if not resp['ok']:
            log.warning(f"Unable to open im with user: {resp}")
            return

        channel_id = resp['channel']['id']
        if data.files_ids:
            resp = slack_client.share_files(data.files_ids, channel_id, data.text)
        else:
            resp = slack_client.post_message(channel_id, data.text)

        if not resp['ok']:
            return log.warning(f"Unable to send message: {resp}")

        message = resp.get('message') if 'message' in resp \
            else slack_client.conversation_replies(channel_id, resp['file_msg_ts'])['messages'][0]

        message_model = SlackMessageConvertService.from_slack_response(user.email, "slack_files", bot.token, message,
                                                                       slack_client.client.cookies)
        lead.chat_history.append(message_model)
        chat_history = [message.to_dic() for message in lead.chat_history]
        user_leads_repository.update_lead(user.id, lead.id, slack_channel=channel_id,
                                          chat_history=chat_history, last_action_at=datetime.datetime.utcnow())

        UserContactsRepository().update(user.id, lead.message.sender_id,
                                        chat_id=channel_id, chat_history=chat_history)
