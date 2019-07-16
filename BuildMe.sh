git rev-parse HEAD >version.txt
docker build -t builder -f Build.Dockerfile .
#ßdocker run -it -v /tmp/deploy-ready/:/Build/output builder  

docker run --rm  -v /tmp/deploy-ready/:/Build/output builder cp switchboard.tar /Build/output/
# debug docker --rm -it <hash> sh