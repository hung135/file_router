git pull origin master

echo "version_dict = {\"git_hash\":\"\"\"">scripts/version.py
git rev-parse HEAD >>scripts/version.py
echo "\"\"\",">>scripts/version.py
echo "\"build_time\":\"\"\"">>scripts/version.py
date >>scripts/version.py
echo "\"\"\"">>scripts/version.py




echo "}">>scripts/version.py
docker build -t builder -f Build.Dockerfile .
docker rm buildmecentos
#ßdocker run -it -v /tmp/deploy-ready/:/Build/output builder  
docker run -it --name buildmecentos -v /tmp/deploy-ready/:/Build/output builder /Build/tmp/switchboard --version
#docker run -it --name buildmecentos -v /tmp/deploy-ready/:/Build/output builder cp switchboard_centos_6_10.tar /Build/output/
docker cp buildmecentos:/Build/switchboard_centos_6_10.tar switchboard_centos_6_10.tar 
# debug docker --rm -it <hash> sh