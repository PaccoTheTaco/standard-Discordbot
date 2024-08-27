import json
import os
from .reaction_role import ReactionRole

class DataManager:
    def __init__(self, file_path='reaction_roles.json'):
        self.file_path = file_path
        self.reaction_roles = self.load_reaction_roles()

    def load_reaction_roles(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                reaction_roles = {}
                for message_id, roles in data.items():
                    reaction_roles[message_id] = [ReactionRole(
                        guild_id=role['guild_id'],
                        message_id=message_id,
                        role_id=role['role_id'],
                        emoji=role['emoji']
                    ) for role in roles]
                return reaction_roles
        return {}

    def save_reaction_roles(self):
        with open(self.file_path, 'w') as f:
            json.dump({
                message_id: [role.__dict__ for role in roles] for message_id, roles in self.reaction_roles.items()
            }, f, indent=4)

    def add_reaction_role(self, reaction_role):
        message_id = reaction_role.get_message_id()
        if message_id not in self.reaction_roles:
            self.reaction_roles[message_id] = []
        self.reaction_roles[message_id].append(reaction_role)
        self.save_reaction_roles()

    def get_reaction_roles(self, message_id):
        return self.reaction_roles.get(message_id, [])
