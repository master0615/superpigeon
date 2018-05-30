FROM nginx

RUN rm -f /etc/nginx/conf.d/default.conf

ADD wait-for.sh /wait-for.sh

ADD sites-enabled /etc/nginx/conf.d
