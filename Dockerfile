FROM python:3.11-slim-bullseye
RUN pip install future
COPY . . 
RUN python3 dev_setup.py
RUN python3 setup.py install

CMD ["python3", "-m","sqlscripter"]