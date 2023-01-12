FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
EXPOSE 8000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
