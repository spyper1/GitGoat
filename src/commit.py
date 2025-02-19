import git, os, logging
from faker import Faker

class Commit:
    
    def __init__(self, repository: git.Repo):
        self.repo = repository
        self.repo.git.add(update=True)
        self.origin = self.repo.remote(name='origin')
        self.fake = Faker()

    # Generates commits with some flexability. The count of commits and days since last commit are mandatory, while the others have default generators. 
    # If commit_dates are provided as a list, make sure the commit_messages list is the same length. 
    def generate_commits(self, count: int, days_since_latest_commit: int, commit_dates: list = [], commit_messages: list = [], random_commit_messages: bool = True, commit_message: str = 'Random commit message', commits_filename = None):
        if len(commit_dates) == 0:
            commit_dates = self.generate_commit_dates(count, days_since_latest_commit)
        if len(commit_messages) == 0:
            commit_messages = self.generate_commit_messages(len(commit_dates), random_commit_messages, commit_message)
        for _ in range(len(commit_dates)):
            self.repo.index.add([self.generate_file_message(filename=commits_filename)])
            timestamp = commit_dates.pop(0).strftime('%Y-%m-%d %H:%M:%S')
            self.repo.index.commit(commit_messages.pop(0), commit_date=timestamp, author_date=timestamp)
        try:
            self.origin.push()
            logging.info(f'Succesully pushed code from {self.repo.common_dir}')
        except Exception:
            logging.warning(f'Unable to push code from {self.repo.common_dir}')

    # The file name and content are automatically generated if the values are not assigned.
    # The open_file_mode setting options are 'w' for overwiriting or 'a' for appending content. 
    def generate_file_message(self, filename = None, file_content = None, open_file_mode = 'w'):
        if filename is None:
            filename = f'{self.fake.lexify(text="???????")}.txt'
        filename = os.path.join(self.repo.working_dir,filename)
        content = file_content if file_content is not None else self.fake.paragraph(nb_sentences=1)
        with open(filename, open_file_mode) as f:
                f.write(content)
        return filename

    def generate_commit_messages(self, count: int, random: bool = True, message: str = 'Random commit message'):
        commit_messages = []
        text = message if random is False else message + ' ???????????????' 
        for _ in range(count):
            commit_messages.append(self.fake.lexify(text=text))
        return commit_messages

    def generate_commit_dates(self, count: int, days_since_latest_commit):
        commit_dates = []
        end_date = f'-{str(days_since_latest_commit)}d'
        for _ in range(count):
            commit_dates.append(self.fake.date_time_between(start_date='-1y', end_date=end_date, tzinfo=None))
        if days_since_latest_commit < 60:
            for _ in range(int(count/10)):
                commit_dates.append(self.fake.date_time_between(start_date='-29d', end_date=end_date, tzinfo=None))       
        return commit_dates