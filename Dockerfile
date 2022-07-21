FROM python:3

ADD main.py /
ADD occupancy /occupancy
ADD pricing /pricing
ADD reviews /reviews
ADD scraper_base /scraper_base
ADD config/constants.py /config/constants.py
ADD requirements.txt /

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

CMD ["curl", "169.254.170.2\$AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]
CMD ["python", "main.py"]

# docker buildx build --platform=linux/amd64 -t scraper-1 .
