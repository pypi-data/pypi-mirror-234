from abc import ABC
from typing import Optional
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.slack_client import SlackClient
from pydantic import BaseModel
from lgt_data.mongo_repository import LeadMongoRepository, UserLeadMongoRepository, GarbageLeadsMongoRepository, \
    SpamLeadsMongoRepository, DedicatedBotRepository
from lgt_data.model import SlackReplyModel
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Update messages conversations
"""


class ConversationRepliedJobData(BaseBackgroundJobData, BaseModel):
    channel_id: Optional[str]
    ts: str


class ConversationRepliedJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return ConversationRepliedJobData

    def exec(self, data: ConversationRepliedJobData):
        lead = LeadMongoRepository().get(timestamp=data.ts, channel_id=data.channel_id)
        if not lead:
            return

        bot = DedicatedBotRepository().get_one(only_valid=True, source_id=lead.message.source.source_id)
        if not bot or bot.invalid_creds:
            log.warning(f"Lead: {lead.id}, no bot with valid creds to load replies")
            return

        client = SlackClient(bot.token, bot.cookies)
        resp = client.conversations_replies(lead.message.channel_id, data.ts)
        if not resp["ok"]:
            return

        if not resp.get("messages"):
            return

        replies = []
        for slack_reply in resp["messages"][1:]:
            reply = SlackReplyModel.from_slack_response(slack_reply)
            user_response = client.user_info(reply.user)
            if user_response["ok"]:
                reply.username = user_response.get("user").get("real_name")
            if not reply.attachments and lead.message.urls_in_message:
                for attachment in lead.message.urls_in_message:
                    if attachment:
                        attachments = client.get_attachments(lead.message.channel_id,
                                                             lead.message.message_id,
                                                             attachment)
                        if attachments:
                            reply.attachments.append(attachments)
            replies.append(reply.to_dic())

        set_dict = {
            "replies": replies,
        }
        pipeline = {"message.timestamp": data.ts}
        if data.channel_id:
            pipeline['message.channel_id'] = data.channel_id
        LeadMongoRepository().collection().update_many(pipeline, {"$set": set_dict})
        UserLeadMongoRepository().collection().update_many(pipeline, {"$set": set_dict})
        GarbageLeadsMongoRepository().collection().update_many(pipeline, {"$set": set_dict})
        SpamLeadsMongoRepository().collection().update_many(pipeline, {"$set": set_dict})
