FROM python:3.8-slim   
COPY ./app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5001
CMD ["python","app/app.py"]
