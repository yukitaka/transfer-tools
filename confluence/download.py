import os

def pages(args):
    print(args)
    print(os.environ['CONFLUENCE_DOMAIN'])
    print(os.environ['ATLASSIAN_USER'])
    print(os.environ['ATLASSIAN_TOKEN'])
