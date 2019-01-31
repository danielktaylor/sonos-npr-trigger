FROM python:3
ADD app.py /
RUN pip install beautifulsoup4 Flask soco requests python-dateutil
EXPOSE 5000
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
