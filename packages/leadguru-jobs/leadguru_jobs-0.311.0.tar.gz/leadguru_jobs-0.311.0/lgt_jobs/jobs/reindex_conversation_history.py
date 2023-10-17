from abc import ABC
from typing import List
from lgt_data.model import UserLeadModel
from lgt_data.mongo_repository import UserLeadMongoRepository
from pydantic import BaseModel
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
User Leads reindex conversation history
"""


class ReIndexUserLeadsConversationHistoryJobData(BaseBackgroundJobData, BaseModel):
    user_id: str


class ReIndexUserLeadsConversationHistoryJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return ReIndexUserLeadsConversationHistoryJobData

    def exec(self, data: ReIndexUserLeadsConversationHistoryJobData):
        leads: List[UserLeadModel] = UserLeadMongoRepository().get_leads(user_id=data.user_id, skip=0, limit=10000)
        leads = [lead for lead in leads if hasattr(lead, "chat_history") and lead.chat_history]
        for lead in leads:
            index = "\n".join([message.text for message in lead.chat_history])
            UserLeadMongoRepository().update_lead(data.user_id, lead.id, full_message_text=index)
