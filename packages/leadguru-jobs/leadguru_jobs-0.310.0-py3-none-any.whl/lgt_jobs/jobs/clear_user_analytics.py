from abc import ABC
from datetime import datetime
from typing import Optional
from lgt_data.engine import UserCreditStatementDocument
from lgt_data.enums import UserAction
from lgt_data.mongo_repository import client, DedicatedBotRepository, to_object_id
from pydantic import BaseModel
from .user_balance_update import UpdateUserBalanceJob, UpdateUserBalanceJobData
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob
from ..runner import BackgroundJobRunner

"""
Clear user limits
"""


class ClearUserAnalyticsJobData(BaseBackgroundJobData, BaseModel):
    user_id: Optional[str]


class ClearUserAnalyticsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return ClearUserAnalyticsJobData

    def exec(self, data: ClearUserAnalyticsJobData):
        dedicated_bots = DedicatedBotRepository().get_user_bots(data.user_id)
        if dedicated_bots:
            dedicated_bot_ids = [str(bot.id) for bot in dedicated_bots]
            client["lgt_analytics"]["dedicated_filtered_messages"].delete_many({"extra_id": {"$in": dedicated_bot_ids}})
            client["lgt_analytics"]["dedicated_received_messages"].delete_many({"extra_id": {"$in": dedicated_bot_ids}})

        client["lgt_analytics"]["user-message-processed"].delete_many({"data": data.user_id})
        client["lgt_analytics"]["user-paid-lead-save"].delete_many({"data": data.user_id})
        client["lgt_analytics"]["user-message-processed"].delete_many({"data": data.user_id})
        client["lgt_analytics"]["user-lead-extended"].delete_many({"data": data.user_id})
        client["lgt_analytics"]["user-lead-deleted"].delete_many({"data": data.user_id})
        client["lgt_analytics"]["user-contact-save"].delete_many({"data": data.user_id})

        client["lgt_admin"]["user_leads"].delete_many({"user_id": to_object_id(data.user_id)})
        client["lgt_admin"]["user_credit_statement_document"].delete_many({"user_id": to_object_id(data.user_id)})

        client["lgt_admin"]["users"].update_one({"id": to_object_id(data.user_id)},
                                                {"$set": {"leads_proceeded": 0, "leads_filtered": 0}})

        UserCreditStatementDocument(
            user_id=to_object_id(data.user_id),
            created_at=datetime.utcnow(),
            balance=1000,
            action=UserAction.INITIAL_CREDITS_SET,
            attributes=["clear-job"]
        ).save()
        BackgroundJobRunner.submit(UpdateUserBalanceJob, UpdateUserBalanceJobData(user_id=data.user_id))
