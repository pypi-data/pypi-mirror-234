from abc import ABC
from typing import Optional
from lgt.common.python.helpers import get_formatted_bot_name
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.model import DedicatedBotModel
from lgt_data.mongo_repository import BotMongoRepository, DedicatedBotRepository
from pydantic import BaseModel
from lgt_data.analytics import get_bots_aggregated_analytics
from lgt.common.python.lgt_logging import log
from lgt.common.python.enums.slack_errors import SlackErrors
from ..basejobs import BaseBackgroundJob, BaseBackgroundJobData

"""
Update bots statistics
"""


class BotStatsUpdateJobData(BaseBackgroundJobData, BaseModel):
    bot_id: Optional[str]


class BotStatsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotStatsUpdateJobData

    def exec(self, data: BotStatsUpdateJobData):
        bots_rep = DedicatedBotRepository()
        bot = bots_rep.get_one(id=data.bot_id)
        if not bot:
            bots_rep = BotMongoRepository()
            bot = bots_rep.get_by_object_id(data.bot_id)
            if not bot:
                return

        if not bot.token or not bot.cookies:
            log.warning(f"[BotStatsUpdateJob]: Bot {bot.id} has no credentials.")
            BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)
            return

        client = SlackWebClient(bot.token, bot.cookies)
        test_auth_response = client.test_auth()
        if not test_auth_response.status_code == 200:
            log.warning(f"[BotStatsUpdateJob]: Error to auth {data.bot_id}. {test_auth_response.content}")
            return

        if not bot.invalid_creds:
            error = test_auth_response.json().get("error")
            if error == SlackErrors.INVALID_AUTH or error == SlackErrors.TWO_FACTOR_REQUIRED:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)

        user = test_auth_response.json().get('user_id')
        bot.associated_user = user
        bots_rep.add_or_update(bot)
        team_info = client.get_team_info()
        if team_info.get('ok'):
            bot.source.source_name = get_formatted_bot_name(team_info['team']['domain'])
            bot.slack_url = bot.registration_link = team_info['team']['url']
            bots_rep.add_or_update(bot)
        received_messages, filtered_messages = get_bots_aggregated_analytics(bot_ids=[bot.id])
        try:
            channels_response = client.channels_list()
        except:
            log.warning(f"[BotStatsUpdateJob]: Error to get channels list for bot {bot.id}.")
            return

        if not channels_response['ok']:
            if channels_response.get("error") == SlackErrors.INVALID_AUTH:
                BotStatsUpdateJob.__updated_invalid_creds_flag(bot, True)
            else:
                log.warning(f"[BotStatsUpdateJob]: Error during update bot {bot.id} stats. Error: {channels_response}")
            return
        channels = channels_response['channels']
        connected_channels = 0
        channels_users = {}
        active_channels = {}
        users_count = 0
        for channel in channels:
            if channel['is_member']:
                active_channels[channel['id']] = channel['name']
                connected_channels += 1
            num_members = channel.get('num_members', 0)
            channels_users[channel['id']] = num_members
            users_count += num_members

        bot.active_channels = active_channels
        bot.messages_received = received_messages.get(bot.name, 0)
        bot.messages_filtered = filtered_messages.get(bot.name, 0)
        bot.connected_channels = connected_channels
        bot.channels = len(channels)
        bot.channels_users = channels_users
        bot.users_count = users_count
        if bot.recent_messages is None:
            bot.recent_messages = []

        # save only last 50 messages
        bot.recent_messages = bot.recent_messages[-50:]
        bots_rep.add_or_update(bot)

    @staticmethod
    def __updated_invalid_creds_flag(bot: DedicatedBotModel, invalid_creds: bool):
        if bot.invalid_creds != invalid_creds:
            bot.invalid_creds = invalid_creds
            DedicatedBotRepository().add_or_update(bot)
