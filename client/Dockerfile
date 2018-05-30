FROM node:9

RUN mkdir -p /opt/app/client

WORKDIR /opt/app/client

ADD package.json /opt/app/client

RUN useradd -d /opt/app/web app

ADD . /opt/app/client

RUN npm install

RUN chown -R app /opt/app/client

EXPOSE 8000

CMD ["/opt/app/client/entrypoint.sh"]

