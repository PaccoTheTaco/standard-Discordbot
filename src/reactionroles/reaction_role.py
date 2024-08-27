class ReactionRole:
    def __init__(self, guild_id, message_id, role_id, emoji):
        self.guild_id = guild_id
        self.message_id = message_id
        self.role_id = role_id
        self.emoji = emoji

    def get_guild_id(self):
        return self.guild_id

    def get_message_id(self):
        return self.message_id

    def get_role_id(self):
        return self.role_id

    def get_emoji(self):
        return self.emoji
