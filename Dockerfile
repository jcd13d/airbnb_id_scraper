FROM python:3

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
#ENTRYPOINT ["pyaws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 033046933810.dkr.ecr.us-east-1.amazonaws.comthon", "main.py", "-n"]