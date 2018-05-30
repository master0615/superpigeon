FROM python:3.5-onbuild

RUN mkdir -p /opt/app/web

ADD . /opt/app/web

RUN useradd -d /opt/app/web app

WORKDIR /opt/app/web

EXPOSE 8001

RUN pip install -r requirements.txt

USER app

CMD ["/opt/app/web/entrypoint.sh"]
