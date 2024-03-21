# build stage
FROM node:lts-alpine3.19 as build-stage

ARG TARGETOS
ARG TARGETARCH

RUN echo "Building for $TARGETOS/$TARGETARCH"

RUN apk update --no-cache && apk add --update alpine-sdk

VOLUME /app
WORKDIR /app
COPY package*.json ./
COPY .env .
COPY . .
#RUN #npm cache clean --force
RUN npm -g install @quasar/cli@latest

RUN npm install

RUN quasar clean
RUN quasar build -m pwa
# EXPOSE 80
# ENTRYPOINT [ "quasar", "build", "--mode", "pwa", "&&", "bash", "-c" ]
# ENTRYPOINT [ "quasar serve --https --cert cert/server.crt --key cert/server.key dist/pwa" ]
# RUN quasar dev


# production stage
FROM nginx:stable-alpine as production-stage
RUN apk update --no-cache
COPY --from=build-stage /app/dist/pwa /usr/share/nginx/html
# handle reload in router history mode
RUN sed -i '/location\ \//a \\t \ try_files \$uri \$uri/ /index.html; \' /etc/nginx/conf.d/default.conf
EXPOSE 80

ENTRYPOINT nginx -g 'daemon off;'
