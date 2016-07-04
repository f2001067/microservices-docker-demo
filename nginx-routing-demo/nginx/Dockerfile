FROM nginx
MAINTAINER Uday.Jandhyala@cariboutech.com

# Remove default files we don't need
RUN rm /etc/nginx/conf.d/default.conf

# Add default configuration
COPY conf/routing.conf /etc/nginx/conf.d/routing.conf
COPY conf/nginx.conf /etc/nginx/nginx.conf

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

VOLUME ["/var/cache/nginx"]

EXPOSE 80 443

CMD ["nginx"]
