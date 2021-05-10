FROM node:13.7-alpine

WORKDIR /frontend

COPY . /frontend/

RUN apk add -U --no-cache git python3 make g++ \
  # && npm install -g yarn@latest \
  && yarn install \
  && yarn build \
  && apk del --no-cache git make g++
