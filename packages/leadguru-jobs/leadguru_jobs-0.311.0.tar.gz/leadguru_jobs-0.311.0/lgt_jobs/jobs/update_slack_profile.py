from abc import ABC
from lgt.common.python.lgt_logging import log
from lgt.common.python.slack_client.slack_client import SlackClient
from lgt_data.model import UserModel
from lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository
from pydantic import BaseModel
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Update Slack User profile
"""


class UpdateUserSlackProfileJobData(BaseBackgroundJobData, BaseModel):
    user_id: str


class UpdateUserSlackProfileJob(BaseBackgroundJob, ABC):

    @property
    def job_data_type(self) -> type:
        return UpdateUserSlackProfileJobData

    def exec(self, data: UpdateUserSlackProfileJobData):
        user = UserMongoRepository().get(data.user_id)
        bots = DedicatedBotRepository().get_user_bots(data.user_id)
        for bot in bots:
            if bot.invalid_creds:
                log.warning(
                    f'User: {user.email} dedicated bot: {bot.source.source_id} credentials are invalid. '
                    f'Not able to update user profile')
                continue

            slack = SlackClient(bot.token, bot.cookies)
            UpdateUserSlackProfileJob.__update_profile(user, slack)

    @staticmethod
    def __update_profile(user: UserModel, slack: SlackClient):
        profile = slack.get_team_profile()
        title_section_id = None
        title_field_id = None
        skype_section_id = None
        for field_data in profile.get('profile', {}).get('fields', []):
            if field_data.get('field_name') == 'title':
                title_section_id = field_data.get('section_id')
                title_field_id = field_data.get('id')
                break
        for section_data in profile.get('profile', {}).get('sections', []):
            if section_data.get('label') == 'About me':
                skype_section_id = section_data.get('id')
                break

        slack.update_profile(user.slack_profile.to_dic())
        auth = slack.test_auth().json()
        user_id = auth.get('user_id')
        title_element_id = title_field_id.replace(title_field_id[:2], 'Pe')
        response = slack.update_section(user_id, title_section_id, title_element_id, user.slack_profile.title)
        sections = response['result']['data']['setProfileSection']['profileSections']
        elements = []
        for section in sections:
            if section['label'] == 'About me':
                elements = section['profileElements']
                break
        skype_element_id = None
        for element in elements:
            if element['label'] == 'Skype':
                skype_element_id = element['elementId']
                break
        slack.update_section(user_id, skype_section_id, skype_element_id, user.slack_profile.title)
        # try to update user photo
        if user.photo_url:
            slack.update_profile_photo(user.photo_url)
