import os
import argparse
from github import Github

# ADD NEW RELEASE, DELETE OLD RELEASE

def _delete_release(asset):
    asset.delete_asset()

def _create_asset(release, name, asset_file):
    release_asset.upload_asset(content_type="application/binary", name="", asset=open("", "rb"))

def parse_cli():
   parser = argparse.ArgumentParser(description='Manages release assets for a Github release')
   parser.add_argument("-k", "--key", required=True, help="Key or path to .key file")
   praser.add_argument("-r", "--repo", help="Repository name in the format of <user>/<project_name>")
   parser.add_argument("-rn", "-repoName", help="")
   parser.add_argument("")
#    parser.add_argument("-y","-yaml","--yaml", help="Location of the yaml file")
#    parser.add_argument("-s", "-skeleton", "--skeleton", help="Generates a skeleton.yaml file to the directory specified")
#    parser.add_argument("-v", "-verbose", help="Enable verbose mode", action="store_true")
   args = parser.parse_args()
   return args 

def read_key():


def run(args):
    key = read_key(args.key)
    gh = Github(key)


if __name__ == "__main__":
    args = parse_cli()
    gh = Github("5da2d598210df42d4f4f318b7822b78db8cb2436")
    repo = gh.repo("hung135/file_router")
    release = repo.get_latest_release()
