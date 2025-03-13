FROM python:3.9
#this is needed, otherwise bootstrap errors show up regarding cv2 import
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
#this is optional, but i added just to be sure
ENV PORT=8080
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python3", "app.py"]