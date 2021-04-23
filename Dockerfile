FROM public.ecr.aws/bitnami/python:latest

COPY schedule-containers.py .

RUN python -m pip install boto3


CMD [ "schedule--containers.py" ]
ENTRYPOINT [ "python3" ]
