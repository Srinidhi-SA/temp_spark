# Nginx Dockerfile
# Pull base image.
FROM nginx

RUN groupadd -r marlabs && useradd -r -s /bin/false -g marlabs marlabs

RUN apt-get update && apt-get install vim curl -yqq
RUN rm -rf /etc/nginx/conf.d/default.conf 
ADD static.tgz /home/
ADD welcome.html /home/static/
WORKDIR /home/static/react/
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
	apt-get install nodejs -y && \
	rm -rf node_modules/ && \
	node -v && \
	apt-get install npm -y && \
	npm install && \
	npm run buildDev && \
	cd /home/static/ && \
	ln -s react/src/assets/ assets && \
        ln -s react/src/userManual/ userManual 
WORKDIR /etc/nginx
#COPY nginx.conf /etc/nginx/conf.d/nginx.conf
ADD conf.d/ /etc/nginx/conf.d/
RUN mkdir /home/config/
RUN mkdir /home/keys/
RUN touch /var/run/nginx.pid && \
  chown -R marlabs:marlabs /var/run/nginx.pid && \
  chown -R marlabs:marlabs /var/cache/nginx
#RUN chown -R marlabs:marlabs /home/config /home/static
#RUN chown -R marlabs:marlabs /home/config

EXPOSE 8081 80 443 8401 8400 8000
