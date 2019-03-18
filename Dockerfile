FROM python
ADD . .
RUN apt-get update
RUN apt-get install python3.5-dev -y
RUN python -m pip install --upgrade pip
RUN pip install grpcio dill redis
RUN pip install grpcio-tools pika uuid
EXPOSE 50051
CMD ["python3", "daemon.py"]

