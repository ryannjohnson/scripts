from dotenv import load_dotenv
from github import Github
import os


load_dotenv() # Important to do before accessing env vars.


GITHUB_ORGANIZATION_NAME = os.getenv('GITHUB_ORGANIZATION_NAME')
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')


github_session = Github(GITHUB_PERSONAL_ACCESS_TOKEN)
