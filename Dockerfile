FROM python:3

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

# docker buildx build --platform=linux/amd64 -t testrepo .
