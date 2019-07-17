import os
import sys
import re
import math
import argparse
from github import Github

def _error_out(msg):
    print(msg)
    sys.exit(1)

def _file_exist(path):
    return os.access(path, os.W_OK)

def create_release(repository, releases, name, message, tag=None):
    if not tag:
        tag = re.findall(".\d", releases[0].tag_name)
        tag[-1] = str("%.1f" % (float(tag[-1]) + .1))[1:]
        tag = "".join(tag)

    release = repository.create_git_release(tag, name, message, prerelease=True)
    return release

def upload_asset(filep, tag=None, release=None, releases=None):
    if not _file_exist(filep):
        _error_out("File not found")
    if not release:
        release = [release for release in releases if release.tag_name == tag][0]
        if not release:
            _error_out("Release tag %s does not exists" % args.tag)
    release.upload_asset(filep)


def parse_cli():
   parser = argparse.ArgumentParser(description='Manages release assets for a Github release')

   required_groups = parser.add_argument_group("Required")
   required_groups.add_argument("-k", "--key", required=True, help="Key or path to .key file")
   required_groups.add_argument("-r", "--repo", required=True, help="Repository name in the format of <user>/<project_name>")

   # delete
   delete_group =parser.add_argument_group("Delete")
   delete_group.add_argument("-d", "--delete", help="Delete the following release name")

   # create`
   create_group = parser.add_argument_group("Create")
   create_group.add_argument("-c", "--create", help="Creates release with given name")
   create_group.add_argument("-m", "--message", required="-c" in sys.argv, help="Message of new release")

   # add an asset
   asset_group = parser.add_argument_group("Assets")
   asset_group.add_argument("-u", "--update", help="Update a release by adding another asset", action="store_true")
   asset_group.add_argument("-a", "--asset", required="-u" in sys.argv, help="Path to asset to upload")

   # optionals
   extras_group = parser.add_argument_group("Optional")
   extras_group.add_argument("-p", "--print", help="Print all release tags", action="store_true")
   extras_group.add_argument("-e", "--enterprise", help="Using enterprise Github account enter the address needed to connect to; provide a url like so: https://github.com/")
   extras_group.add_argument("-t", "--tag", required="-u" in sys.argv, help="Target tag")

   args = parser.parse_args()
   return args 

def read_key(path_or_key):
    if _file_exist(path_or_key):
        with open(path_or_key, "r") as f:
            key = f.read()
            f.close()
        return key # key from path
    return path_or_key # key

def run(args):
    key = read_key(args.key)
    gh = Github(base_url=args.e + "/api/v3", login_or_token=key) if args.enterprise else Github(key)
    repository = gh.get_repo(args.repo)
    releases = repository.get_releases()

    if args.create:
        release = create_release(repository, releases, args.create, args.message, args.tag)
        print("Created release: %s" % args.create)
        if args.asset:
            upload_asset(args.asset, release=release)
            print("Added asset to release")

    if args.update:
        upload_asset(args.asset, tag=args.tag, releases=releases)
        print("Uploaded asset")
        
    if args.delete:
        [x.delete_release() for x in releases if x.title == args.delete or x.tag_name == args.delete]
        print("Deleted release")

    if args.print:
        [print("%s | %s" %(release.title, release.tag_name)) for release in releases]

if __name__ == "__main__":
    args = parse_cli()
    run(args)