FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY store/daemon.py ./daemon.py
COPY store/configurationStore.py ./configurationStore.py
COPY store/modelsStore.py ./modelsStore.py
COPY store/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./daemon.py"]