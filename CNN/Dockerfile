FROM python:2.7.15-jessie
RUN mkdir -p usr/src/app
COPY . usr/src/app
WORKDIR usr/src/app
RUN which python
RUN apt-get update && apt-get install -y
RUN pip install flask flask_uploads Werkzeug opencv-python numpy tensorflow
CMD ["flask", "run", "--host=0.0.0.0", "--port=1333"]