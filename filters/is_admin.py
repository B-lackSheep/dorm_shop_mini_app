from config import ADMINS


def is_admin(message):
    username = message.from_user.username
    if not username:
        return False
    return username in ADMINS
