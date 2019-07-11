# rm -rf build dist switchboard.spec
# pyinstaller scripts/switchboard.py -w --onefile
# ./dist/switchboard -y scripts/switchboard.yaml

docker build -t builder -f Build.Dockerfile .
docker run -it builder 
# debug docker --rm -it <hash> sh