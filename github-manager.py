import os
import sys
import re
import math
import argparse
from github import Github

def parse_cli():
   parser = argparse.ArgumentParser(description='Manages release assets for a Github release')
   parser.add_argument("-k", "--key", required=True, help="Key or path to .key file")
   parser.add_argument("-r", "--repo", required=True, help="Repository name in the format of <user>/<project_name>")
   parser.add_argument("-e", "--enterprise", help="Using enterprise Github account enter the address needed to connect to")
   # delete
   parser.add_argument("-d", "--delete", help="Delete the following release name")
   # create
   parser.add_argument("-c", "--create", help="Creates release with given name")
   parser.add_argument("-m", "--message", required="-c" in sys.argv, help="Message of new release")
   args = parser.parse_args()
   return args 

def read_key(path_or_key):
    if os.access(path_or_key, os.W_OK):
        with open(path_or_key, "r") as f:
            key = f.read()
            f.close()
        return key # key from path
    return path_or_key # key

def run(args):
    key = read_key(args.key)
    gh = Github(key)
    repository = gh.get_repo(args.repo)
    releases = repository.get_releases()

    if args.create:
        tag = re.findall(".\d", releases[0].tag_name)
        tag[-1] = str("%.1f" % (float(tag[-1]) + .1))[1:]
        tag = "".join(tag)
        release = repository.create_git_release(tag, args.create, args.message, prerelease=True)
        print("Created release")

    if args.delete:
        [x.delete_release() for x in releases if x.title == args.delete or x.tag_name == args.delete]
        print("Deleted release")

if __name__ == "__main__":
    args = parse_cli()
    run(args)