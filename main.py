import os

from dotenv import load_dotenv

load_dotenv()

print(os.environ['ATLASSIAN_USER'])
print(os.environ['ATLASSIAN_TOKEN'])
