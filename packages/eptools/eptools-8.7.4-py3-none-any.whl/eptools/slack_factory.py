import logging
import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from eptools.configuration import *


# Utils
# ---

def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        after_func_new_globals = getglobals()
        # keep own globals rather than getglobals after func
        after_func_new_globals.update(globals())
        globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

loadconfigwithfile = reloadconfig(loadconfigwithfile)
loadconfigwithjson = reloadconfig(loadconfigwithjson)


# Slack Factory
# ---
# This Python module can be used to send Slack notifications
# 
# Slack Docs:           https://slack.dev/python-slack-sdk/
# Block Kit Builder:    https://app.slack.com/block-kit-builder/
# 
# Test channel ID: C0489AUFV8V
# Test channel Name: testing

class SlackFactory:
    @reloadconfig
    def __init__(self, config_path=None, logger = None) -> None:
        loadconfigwithfile(config_path)
        
        self.logger = logger
        if not self.logger:
            self.logger = logging.getLogger(__name__)
        # TODO: try to fix this to use custom logger here
        #     self.logger = logger.EasyPostLogger('SlackFactory')
        self.client = WebClient(token=globals()['C_SLACK_TOKEN'])
        self.channel_id = None
        self.channel_name = None
    
    def send_message(self, channel_id, message) -> dict:
        try:
            response = self.client.chat_postMessage(
                channel = channel_id,
                text = message
            )
            return response
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])

    def create_channel(self, channel_name, extra = 0):
        channel_name_with_postfix = channel_name + ("_new" + str(extra) if extra else "")
        try:
            response = self.client.conversations_create(name=channel_name_with_postfix,is_private=True)
            return response['channel']['id']
        except SlackApiError as e:
            assert e.response["error"]
            if e.response["error"] == "name_taken":
                return self.create_channel(channel_name,extra=extra+1)
            else:
                self.logger.error(e.response["error"])

    def invite_user_group_to_channel_id(self, channel_id, group_id, remove_other = False, keep_bot = False, retry = 0):
        users_by_group_id =  self.get_users_by_group_id(group_id)
        if users_by_group_id == [] and retry < 5:
            return self.invite_user_group_to_channel_id(channel_id,group_id,remove_other,keep_bot, retry = retry + 1)
        users_in_channel = self.get_users_by_channel_id(channel_id)
        try:
            invite_response = self.client.conversations_invite(channel=channel_id,users=','.join(users_by_group_id))
            print(f"added users {users_by_group_id}")
        except SlackApiError as e:
            assert e.response["error"]
            if e.response["error"] != 'already_in_channel':
                self.logger.error(e.response["error"])
        if remove_other:
            if users_by_group_id == []:
                self.logger.error("Not removing fetch group failed")
                return "Not removing fetch group failed"
            if keep_bot:
                users_by_group_id.append('U025M9YTWBS')
            if len(users_by_group_id) != len(users_in_channel):
                for user in users_in_channel:
                    if user not in users_by_group_id:
                        try:
                            response = self.client.conversations_kick(channel=channel_id,user=user)
                            print(f"user removed {user}")
                        except SlackApiError as e:
                            assert e.response["error"]
                            self.logger.error(e.response["error"])


    def get_users_by_group_id(self, group_id):
        try:
            response = self.client.usergroups_users_list(usergroup=group_id)
            return response['users']
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
            return []

    def get_users_by_channel_id(self, channel_id):
        try:
            response = self.client.conversations_members(channel=channel_id)
            return response['members']
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
            return []

    def get_channel_id(self,channel_name):
        if self.channel_name == channel_name:
            return self.channel_id
        channels = self.get_all_channels()
        if channels or channels == []:
            for channel in channels:
                test_name = re.sub("[_]{1}new[\d)]+$","",channel['name'])
                if channel_name == test_name:
                    self.channel_name = channel_name
                    self.channel_id = channel['id']
                    return self.channel_id
            else:
                return self.create_channel(channel_name)

    def log(self, channel_name, message = '', messages = [], error="UnknownError") -> dict:
        prefix = "error-"
        channel_prefixed = prefix + channel_name.lower()
        # get or create channel
        channel_id = self.get_channel_id(channel_prefixed)

        # add and or remove members
        it_team_group_id = 'S01LRK6B3DE'
        self.invite_user_group_to_channel_id(channel_id , it_team_group_id, keep_bot=True, remove_other=True)
        if len(str(error)) > 140:
            error = (str(error))[:140]
        if type(message) == str:
            if len(message) > 150:
                n = 150 # chunk length
                message = [message[i:i+n] for i in range(0, len(message), n)]
        if type(message) == str:

            blocks = [
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"ERROR : {error}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{message}"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        elif type(messages) == list:
            blocks = [
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"ERROR : {error}",
                        "emoji": True
                    }
                }
            ]
            
            for line in message:
                blocks.append(
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{line}"
                        }
                    }
                )

            
            blocks.append(
            {
                "type": "divider"
            })
        else:
            blocks = [
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"ERROR : {error}",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "No messages for this error"
                    }
                },
                {
                    "type": "divider"
                }
            ]
        try:
            response = self.client.chat_postMessage(
                channel = channel_id,
                text = str(error),
                blocks = blocks
            )
            return response
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
            

    def send_formatted_message(self, channel_id, blocks, short_description=None) -> dict:
        if not short_description:
            short_description = "EasyBot has something to tell you!"

        try:
            
            print(channel_id)
            print(blocks)
            print(short_description)
            
            response = self.client.chat_postMessage(
                channel = channel_id,
                text = short_description,
                blocks = blocks
            )
            return response
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
            
    def get_all_channels(self) -> list:
        try:
            response = self.client.conversations_list(types='private_channel,public_channel',limit=1000)
            return response['channels']
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
            
    def get_channel_info(self, channel_id) -> dict:
        try:
            response = self.client.conversations_info(channel=channel_id)
            return response['channel']
        except SlackApiError as e:
            assert e.response["error"]
            self.logger.error(e.response["error"])
  
if __name__ == '__main__':
    pass
    slack_factory = SlackFactory()
    # result = slack_factory.get_all_channels()
    res = slack_factory.log('eptools_maintest', ['Je kan verlaten nu',':wink:'], error="MainMessageTest")
   