from src.connection import ConnectionHandler
from faker import Faker

class PullRequest:

    def __init__(self, organization, config_file = None):
        self.endpoint = f'/repos/{organization}/[REPO]/pulls'
        self.fake = Faker()
        self.config_file = config_file

    async def get_pull_requests(self, pat, repository):
        conn = ConnectionHandler(pat, self.config_file)
        endpoint = self.endpoint.replace('[REPO]', repository)
        pr_ids = []
        resp = await conn.get(endpoint)
        for pr in resp:
            if pr['state'] == 'open': 
                pr_ids.append(pr['number'])
        return pr_ids

    async def create_pull_request(self, pat, repository, head_branch):
        conn = ConnectionHandler(pat, self.config_file)
        endpoint = self.endpoint.replace('[REPO]', repository)
        data = {
            'head': head_branch,
            'base': 'main',
            'title': self.fake.lexify(text='Approval GitGoat fake reference ????????'),
            'body': self.fake.paragraph(nb_sentences=3)
        }
        resp = await conn.post(endpoint, json_data=data)
        return resp['number']
      
    async def merge(self, pat, repository, pull_request_number):
        conn = ConnectionHandler(pat, self.config_file)
        endpoint = self.endpoint.replace('[REPO]', repository) + f'/{str(pull_request_number)}/merge'
        data = {
            'commit_title': self.fake.lexify(text='GitGoat fake commit title ????????'),
            'merge_method': 'merge'
        }
        resp = await conn.put(endpoint, data)
        return True if 'merged' in resp else False