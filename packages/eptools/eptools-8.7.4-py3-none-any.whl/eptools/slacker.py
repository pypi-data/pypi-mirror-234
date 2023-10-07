import requests

# Small FYI slack structure url:
# ---
# Slack conversation API docs: 
# https://api.slack.com/docs/conversations-api
#
# Team channel and group Ids can be found when using slack on web
# ex: https://app.slack.com/client/T3JC5NEAG/G01LQJ2V73N/user_groups/S01LRK6B3DE
# ex: https://app.slack.com/client/<teamID>/<ChannelID>/user_groups/<GroupID>
# => T3JC5NEAG(teamId), G01LQJ2V73N(channelId), S01LRK6B3DE(groupId)
# => Add user to this group and they will dynamically added to all error groups

     

class Slacker:
    """
    A class used to send messages to Slack.\n
    Main purpose is to send logs to Slack to notify people.

    Attributes
    ----------
    channelId : str
        SlackChannelID which is used to send logs to.
        Is set after calling "Setup()".
    serviceName : str
        Name of the slack channel to use
        Is set after calling "Setup()".
    logs : ?
        File logger instance used.
        Is optionally set after calling "Setup()".
    slack_token : str
        API token that authenticates all Slack API calls.
        Is set in "__init__()".
    """

    def __init__(self):
        self.channelId = None
        self.serviceName = None
        self.logs = None
        self.slack_token = self.__get_slack_token()

    def setup(self, serviceName: str, logger = None):
        """
        Creates a channel if it does not yet exist\n
        Invites all of the IT Team to that channel,\n
        Sets the 'channelId' so messages can be sent via the log function
        
        params:
        ----
        * serviceName: name of Windows Python Service -> is used to create a slack channel with that name
        * logger: logger instance which can be passed. See "logging.py" file.
        """
        
        self.logs = logger
        self.serviceName = serviceName.lower()
        channelId = None
        print(self.serviceName)

        # 1. Get private channel - If channel doesn't exist create a new one.
        prefix = "error-"
        channels = self.__get_bot_private_channels()
        print(channels)
        if channels or channels == []:
            for channel in channels:
                if (prefix + self.serviceName) == channel['name']:
                    print("channel already exists")
                    self.channelId = channel['id']
                    print("set channel ID to:" + self.channelId)
                    if self.logs:
                        self.logs.debug("Channel Id: " + self.channelId)
                    break

            else:
                print("Channel doesn't exist yet - creating new channel")
                channelId = self.__create_private_channel_and_get_channelId(prefix + self.serviceName)
                if channelId:
                    self.channelId = channelId
                    print("set channel ID to:" + self.channelId)
                    if self.logs:
                        self.logs.debug("Channel Id: " + self.channelId)
                            

            # 2. Invite IT-group to channel.
            if self.channelId: 
                userIds = self.__get_it_team_userIds()
                print(userIds)
                if userIds:
                    print(userIds)
                    response = self.__invite_userIds_to_channelId(userIds, self.channelId)
                    print(response)
                    if response:
                        if self.logs:
                            self.logs.debug('invite successful')
                            print('invite success')
                    else:
                        if self.logs:
                            self.logs.debug('Bad response - No invite')
                        print('Bad response - No invite') 
                else:
                    if self.logs:
                        self.logs.debug('Bad response - UserIds')
                    print('Bad response - UserIds: ' + userIds) 
            else:
                if self.logs:
                    self.logs.debug('No channelId')
                print('No channelId') 

            # 3. Kick non-group members:
            #self.__kick_non_channel_members()

    def log(self, msg: str):
        """
        Send message to channel that has been created/found by/during 'setup()' \n
        
        params
        ----
        msg: string
            Message to send to channel.
        """

        if self.channelId == None:
            if self.logs:
                self.logs.debug('must run setup first')
            print("must run 'setup()' first")

        else:
            try:
                response = requests.post('https://slack.com/api/chat.postMessage', {
                    'token': self.slack_token,
                    'channel': self.channelId,
                    'text': msg  
                }).json()
                if response['ok']:
                    return response
                else:
                    if self.logs:
                        self.logs.error(response['error'])
                    print(response['error'])    

            except Exception as e:
                if self.logs:
                    self.logs.error(str(e))
                print('Something went wrong')
                print(str(e))    

    def __get_slack_token(self):
        """ Read slack_token from credentials """
        return "<slack-token>"

    def __create_private_channel_and_get_channelId(self, channelName: str):
        """
        Creates a private channel and returns the channelId

        params:
        ----
        channelName : string
        """

        try:
            response = requests.post('https://slack.com/api/conversations.create', {
                'token': self.slack_token,
                'name': channelName,   
                'is_private': 'true'
            }).json()
            if response['ok']:
                return response['channel']['id']
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    

        except Exception as e:
            if self.logs:
                self.logs.error(e)
            print('Something went wrong in __create_private_channel_and_get_channelId')
            print(str(e))  

    def __get_user_private_channels(self, userId: str):
        """
        Returns all private channels for given userId
        
        params
        ----
        * userId: string

        

        """
        userId = ''
        try:
            response = requests.post('https://slack.com/api/users.conversations', {
                'token': self.slack_token, 
                'user': userId,
                'types': 'private_channel'
            }).json()
            if response['ok']:
                return response['channels']
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])

        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in __get_user_private_channels')
            print(str(e))

    def __get_group_userIds(self, groupId: str) -> str: 
        """
        Returns a comma separated string of userIds for a given groupId ex.'user1,user2,user3'\n

        params:
        ----
        * group : string

        Returns:
        ----
        Return a comma-separated string of userIDs that belong to slack group.
        """

        try:
            response = requests.post('https://slack.com/api/usergroups.users.list', {
                'token': self.slack_token,
                'usergroup': groupId,
            }).json()
            print(response)
            if response['ok']:
                print("get user ids")
                userIds = response['users']
                separator = ','
                userIds = separator.join(userIds)
                return userIds
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    

        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in __get_group_userIds')
            print(str(e))        

    def __invite_userIds_to_channelId(self, userIds: str, channelId: str):
        """
        Invites a comma separated string of userIds to join a channel by channelId

        params:
        ----
        userIds: string 
            comma separated string of userIds ex. 'W1234567890,W1234567440,W12654644'
        channelId : string 
            ex. 'C1234567890'
        """

        # Add bot to userIds :
        # userIds += ',<user-id>'
        try:
            response = requests.post('https://slack.com/api/conversations.invite', {
                'token': self.slack_token,
                'channel': channelId,
                'users': userIds    
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in invite_userId_to_channelId')
            print(str(e))                   

    def __get_bot_private_channels(self):
        """ Returns all private bot channels """

        userIdBot = 'U025M9YTWBS'
        channels = self.__get_user_private_channels(userIdBot)
        return channels

    def __get_it_team_userIds(self) -> str: 
        """ 
        Returns all itTeam userId's (comma separated string) 
        
        returns:
        ----
        Return a comma-separated string of IT-team userIDs that belong to the IT slack group.
        """

        itGroupId = '<group-id>'
        userIds = self.__get_group_userIds(itGroupId)
        return userIds

    def __get_channel_users(self, channelId):
        try:
            response = requests.post('https://slack.com/api/conversations.members', {
                'token': self.slack_token,
                'channel': channelId,    
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in get_channel_users')
            print(str(e))                   

    def __kick_user_from_channel(self, userId):
        try:
            response = requests.post('https://slack.com/api/conversations.kick', {
                'token': self.slack_token,
                'channel': self.channelId,  
                'user': userId,  
            }).json()
            if response['ok'] == True:  
                return response
            else:
                if self.logs:
                    self.logs.error(response['error'])
                print(response['error'])    
        except Exception as e:
            if self.logs:
                self.logs.error(str(e))
            print('Something went wrong in kick_user_from_channel')
            print(str(e))                    

    def __kick_non_channel_members(self):
        userIdBot = 'U01KNUY6W4W'

        itTeam = self.__get_it_team_userIds().split(',')
        channelUsers = self.__get_channel_users(self.channelId)['members']   

        for user in channelUsers:
            if user in itTeam or user == userIdBot :
                print(f"{user}, OK, you can stay") 
            else:
                print(f"{user}, No longer a member, Kick")  
                self.__kick_user_from_channel(user) 

    def send_Custom_Message(self, channelId, msg):
        slack_token = self.__get_slack_token()
        response = requests.post('https://slack.com/api/chat.postMessage', {
            'token': slack_token,
            'channel': channelId,
            'text': msg  
        }).json()



if __name__ == "__main__":
    # Demo usage of 'Slacker'
    slacker = Slacker()
    # slacker.setup(serviceName="EPTools_MainTest")
    slacker.setup(serviceName="postalia_checkbarcodedoublesservice")
    slacker.log("**Piep**: Checking if slack logging still works")
