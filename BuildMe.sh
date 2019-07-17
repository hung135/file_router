echo "version_dict = {\"git_hash\":\"\"\"">scripts/version.py
git rev-parse HEAD >>scripts/version.py
echo "\"\"\",">>scripts/version.py
echo "\"build_time\":\"\"\"">>scripts/version.py
date >>scripts/version.py
echo "\"\"\"">>scripts/version.py




echo "}">>scripts/version.py
docker build -t builder -f Build.Dockerfile .
#ßdocker run -it -v /tmp/deploy-ready/:/Build/output builder  
docker run -it --rm  -v /tmp/deploy-ready/:/Build/output builder /Build/tmp/switchboard --version
docker run -it --rm  -v /tmp/deploy-ready/:/Build/output builder cp switchboard_centos_6_10.tar /Build/output/
# debug docker --rm -it <hash> sh