import requests
from google.cloud import storage
from datetime import datetime, timedelta
from lgt_data.model import SlackHistoryMessageModel
from .slack_client import SlackClient


def get_file_url(blob_path):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(SlackFilesClient.bucket_name)
    blob = bucket.get_blob(blob_path)
    if not blob:
        return None
    # valid for 3 days
    return blob.generate_signed_url(timedelta(3))


class SlackMessageConvertService:
    @staticmethod
    def from_slack_response(user_email, bot_name, bot_token, dic, cookies=None):

        """
        :rtype: SlackHistoryMessageModel
        """
        result = SlackHistoryMessageModel()
        result.text = dic.get('text', '')
        result.type = dic.get('type', '')
        result.user = dic.get('user', '')
        result.ts = dic.get('ts', '')
        result.attachments = dic.get('attachments', [])
        result.files = []

        if 'files' in dic:
            for file in dic.get('files'):
                if file.get('mode', '') == "tombstone" or not file.get('url_private_download'):
                    continue
                new_file = SlackHistoryMessageModel.SlackFileModel()
                new_file.id = file.get('id')
                new_file.name = file.get('name')
                new_file.title = file.get('title')
                new_file.filetype = file.get('filetype')
                new_file.size = file.get('size')
                new_file.mimetype = file.get('mimetype')

                url_private_download = file.get('url_private_download')
                new_file.download_url = SlackFilesClient.get_file_url(user_email, bot_name, bot_token,
                                                                      new_file.id, url_private_download,
                                                                      new_file.mimetype, cookies)
                result.files.append(new_file)

        js_ticks = int(result.ts.split('.')[0] + result.ts.split('.')[1][3:])
        result.created_at = datetime.fromtimestamp(js_ticks / 1000.0)
        return result


class SlackFilesClient:
    bucket_name = 'lgt_service_file'

    # Consider to cache these file somewhere in the super-fast cache solution
    @staticmethod
    def get_file_url(user_email, bot_name, bot_token, file_id, url_private_download, mimetype, cookies=None):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(SlackFilesClient.bucket_name)
        blob_path = f'slack_files/{user_email}/{bot_name}/{file_id}'
        blob = bucket.get_blob(blob_path)

        if not blob:
            res = requests.get(url_private_download, headers={'Authorization': f'Bearer {bot_token}'}, cookies=cookies)
            if res.status_code != 200:
                raise Exception(
                    f'Failed to download file: {url_private_download} from slack due to response: '
                    f'Code: {res.status_code} Error: {res.content}')
            blob = bucket.blob(blob_path)
            blob.upload_from_string(res.content, content_type=mimetype)

        blob = bucket.get_blob(blob_path)
        # valid for 3 days
        return blob.generate_signed_url(timedelta(3))


class SlackWebClient:
    def __init__(self, token, cookies=None):
        if isinstance(cookies, list):
            cookies = {c['name']: c['value'] for c in cookies}

        self.client = SlackClient(token, cookies)

    def delete_message(self, channel: str, ts: str):
        return self.client.delete_message(channel, ts)

    def update_message(self, channel: str, ts: str, text: str, file_ids=''):
        return self.client.update_message(channel, ts, text, file_ids)

    def get_profile(self, user_id):
        return self.client.user_info(user_id)

    def get_im_list(self):
        return self.client.get_im_list()

    def chat_history(self, channel):
        return self.client.conversations_history(channel)

    def post_message(self, to, text):
        return self.client.post_message(to, text)

    def user_list(self):
        return self.client.users_list()

    def channels_list(self):
        return self.client.get_conversations_list()

    def im_open(self, sender_id):
        return self.client.im_open(sender_id)

    def update_profile(self, profile):
        return self.client.update_profile(profile)

    def channel_join(self, channels):
        return self.client.join_channels(channels)

    def channel_leave(self, channels):
        return self.client.leave_channels(channels)

    def get_reactions(self, channel, ts):
        return self.client.get_reactions(channel, ts)

    def upload_file(self, file, file_name):
        return self.client.upload_file(file, file_name)

    def download_file(self, file_url):
        return self.client.download_file(file_url)

    def delete_file(self, file_id):
        return self.client.delete_file(file_id)

    def share_files(self, files_ids: list, channel: str, text: str = None) -> dict:
        return self.client.share_files(files_ids, channel, text)

    def check_email(self, email: str, user_agent: str) -> bool:
        return self.client.check_email(email, user_agent)

    def confirm_email(self, email: str, user_agent: str, locale: str = 'en-US') -> bool:
        return self.client.confirm_email(email, user_agent, locale)

    def confirm_code(self, email: str, code: str, user_agent: str, ) -> requests.Response:
        return self.client.confirm_code(email, code, user_agent)

    def find_workspaces(self, user_agent: str, ) -> requests.Response:
        return self.client.find_workspaces(user_agent)

    def conversation_replies(self, channel: str, ts: str) -> dict:
        return self.client.conversations_replies(channel, ts)

    def create_shared_invite(self):
        return self.client.create_shared_invite()

    def send_slack_invite_to_workspace(self, email: str):
        return self.client.send_slack_invite_to_workspace(email=email)

    def test_auth(self):
        return self.client.test_auth()

    def get_team_info(self):
        return self.client.get_team_info()
