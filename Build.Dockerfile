FROM centos:6.10

RUN yum -y update && \
    yum -y install yum-utils && \
    yum -y groupinstall development && \
    yum -y install https://centos6.iuscommunity.org/ius-release.rpm && \
    yum -y install python36u && \
    yum -y install python36u-devel && \ 
    yum -y install python36u-setuptools

RUN easy_install-3.6 pip && \
    pip3 install pyinstaller

RUN mkdir -p Build/
WORKDIR Build/

COPY scripts/ /Build/scripts/
ENV PYTHONPATH="/Build/scripts/"
RUN pip3 install -r scripts/requirements.txt
RUN head -n -1 /Build/scripts/version.py >/Build/scripts/version2.py
RUN mv /Build/scripts/version2.py /Build/scripts/version.py

#inject distro into version.py
RUN echo ",\"distro\":\"\"\"">>scripts/version.py
RUN cat /etc/redhat-release >>scripts/version.py
RUN echo "\"\"\"">>scripts/version.py

#inject libs into version.py
RUN echo ",\"python_libs\":\"\"\"" >>/Build/scripts/version.py
RUN pip freeze >>/Build/scripts/version.py
RUN echo "\"\"\"}" >>/Build/scripts/version.py
#RUN pyinstaller scripts/switchboard.py  --add-data /Build/scripts/version.txt:.  --onefile
RUN pyinstaller scripts/switchboard.py  --onefile --paths $PYTHONPATH
RUN mkdir tmp 
RUN tar -czvf switchboard_centos_6_10.tar -C /Build/dist/ . 
RUN tar -xvf ./switchboard_centos_6_10.tar -C ./tmp/
# RUN pip3 install -r scripts/requirements.txt
# RUN pyinstaller scripts/switchboard.py -w --onefile
# RUN tar -czvf switchboard.tar -C dist/ .

#for testing
ENV PGHOST=db
ENV PGDATABASE=postgres
ENV PGUSER=postgres
ENV PGPASSWORD=docker
ENV PGPORT=5432 