# build stage
FROM node:lts-alpine as build-stage

ARG TARGETOS
ARG TARGETARCH
RUN echo "Building for $TARGETOS/$TARGETARCH"

RUN apk update && apk add --update alpine-sdk

WORKDIR /app
COPY package*.json ./
COPY . .
RUN npm -g install @quasar/cli@latest
RUN npm install
#RUN quasar build -m pwa


# production stage
#FROM nginx:stable-alpine as production-stage
#COPY --from=build-stage /app/dist/pwa /usr/share/nginx/html
## handle reload in router history mode
#RUN sed -i '/location\ \//a \\t \ try_files \$uri \$uri/ /index.html; \' /etc/nginx/conf.d/default.conf
#EXPOSE 80

#ENTRYPOINT nginx -g 'daemon off;'
