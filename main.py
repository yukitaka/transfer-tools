import argparse
from dotenv import load_dotenv
from confluence import download

def main():
    parser = argparse.ArgumentParser(
        description='Transfer confluence to growi and jira to redmine'
    )
    subparsers = parser.add_subparsers(help='confluence commands')

    confluence = subparsers.add_parser('confluence', help='see `confluence -h`')
    confluence_download_subparsers = confluence.add_subparsers(help='download from confluence')
    confluence_download = confluence_download_subparsers.add_parser('download', help='see `download -h`')
    confluence_download_pages_subparsers = confluence_download.add_subparsers(help='download pages')
    confluence_download_pages = confluence_download_pages_subparsers.add_parser('pages', help='see `pages -h`')
    confluence_download_pages.add_argument('-A', '--all', action='store_true', help='all pages')
    confluence_download_pages.add_argument('--after', action='store', help='during a certain time period')
    confluence_download_pages.set_defaults(handler=download.pages)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    load_dotenv()
    main()
