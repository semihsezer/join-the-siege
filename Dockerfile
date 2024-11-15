FROM python:3.12

RUN mkdir -p /server

# Install tesseract, poppler
RUN apt-get update && apt-get install -y \
    python-dev-is-python3 \
    tesseract-ocr \
    poppler-utils

WORKDIR /server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src /server/src

EXPOSE 5000
CMD ["flask", "--app", "src.app", "run", "--host", "0.0.0.0"]
