FROM python:3.13
LABEL authors="dmitriipetlin"

WORKDIR /TheShop
COPY requirements.txt /TheShop
RUN pip install -r requirements.txt

COPY . /TheShop

RUN python manage.py makemigrations

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=TheShop.settings

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]