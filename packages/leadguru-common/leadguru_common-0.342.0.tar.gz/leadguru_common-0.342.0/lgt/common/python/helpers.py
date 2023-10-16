import re


def update_credentials(credentials, token, cookies):
    credentials.token = token
    credentials.cookies = cookies
    credentials.invalid_creds = False
    return credentials


def get_formatted_bot_name(name):
    bot_name = name
    bot_name.replace(" ", "_") \
        .replace(".", "dot_") \
        .replace("#", "") \
        .replace("+", "_plus")

    return re.sub(r'[^A-Za-z0-9]', "", bot_name).lower()
