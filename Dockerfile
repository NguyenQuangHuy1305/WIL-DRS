FROM python:lastest

WORKDIR /webpage

COPY . .
# COPY ./requirements.txt /appRUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["webpage.py"]
