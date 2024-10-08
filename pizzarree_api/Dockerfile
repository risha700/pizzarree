# FROM python:3.10-slim as builder
FROM python:3.11-alpine3.18 as builder
ENV VENV=/opt/venv
RUN python3 -m venv VENV
ENV PATH="$VENV/bin:$PATH"


ARG TARGETOS
ARG TARGETARCH

RUN echo "Building for $TARGETOS/$TARGETARCH"

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --update alpine-sdk \
    && apk add --virtual build-deps build-base gcc python3-dev musl-dev libffi-dev pcre-dev pcre graphviz graphviz-dev pkgconfig \
    && apk add postgresql \
    && apk add postgresql-dev git netcat-openbsd \
    && pip install --upgrade pip setuptools wheel \
    && apk add jpeg-dev zlib-dev libjpeg mailcap

RUN mkdir -p /code
RUN mkdir -p /code/app
#RUN mkdir -p /code/GeoLite/
VOLUME /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
RUN apk del build-deps


FROM python:3.11-alpine3.18
ENV VENV=/opt/venv
RUN python3 -m venv VENV
ENV PATH="$VENV/bin:$PATH"

RUN apk update && apk add libpq jpeg-dev zlib-dev libjpeg pcre-dev pcre graphviz graphviz-dev pkgconfig
RUN mkdir -p /wheels
RUN mkdir -p /code
RUN mkdir -p /code/app
#RUN mkdir -p /code/GeoLite/
VOLUME /code
WORKDIR /code
COPY requirements.txt /code/

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /etc/mime.types /etc/mime.types 
RUN pip install --upgrade pip setuptools wheel && pip install --no-input --no-deps --no-cache /wheels/*
#RUN pip install -U python-dotenv
COPY . /code/app/
#COPY ./GeoLite /code/GeoLite/
WORKDIR /code/app
RUN python manage.py collectstatic --noinput
#RUN python manage.py migrate
# RUN python loaddata fixtures.json
RUN addgroup --system django \
    && adduser --system --no-create-home django --ingroup django

EXPOSE 8008

RUN chown -R django:django /code/app
#RUN #/bin/sh
USER django

CMD /bin/sh
#ENTRYPOINT python manage.py migrate && python manage.py loaddata fixtures.json && uwsgi --https 0.0.0.0:8000,cert/server.crt,cert/server.key --wsgi-file pizzarree_api/wsgi.py --master --processes 2 --threads 2 --static-map /static=/code/app/static --static-map /media=/code/app/media --check-static=/code/app/dist --python-auto-reload=1
#ENTRYPOINT uwsgi --https 0.0.0.0:8000,cert/server.crt,cert/server.key --wsgi-file pizzarree_api/wsgi.py --master --processes 4 --threads 2 --static-map /static=/code/app/static
