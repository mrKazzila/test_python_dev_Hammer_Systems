FROM nginx:1.25

RUN \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        openssl
RUN openssl dhparam -out /etc/ssl/dhparam.pem 2048

RUN rm -d -R /etc/nginx/conf.d/
COPY /conf.d /etc/nginx/conf.d

# Uncomment after generate ssl cert
#RUN rm /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/
