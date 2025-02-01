FROM python3.10-buster

WORKDIR /screener
COPY . /screener

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
