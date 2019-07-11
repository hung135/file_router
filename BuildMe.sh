docker build -t builder -f Build.Dockerfile .
docker run -v /workspace/scripts/:/Build/scripts -v /workspace/deploy-ready/:/Build/output builder \
    pip3 install -r scripts/requirements.txt && \
    pyinstaller scripts/switchboard.py -w --onefile && \
    tar -czvf switchboard.tar -C dist/ /Build/output
# debug docker --rm -it <hash> sh