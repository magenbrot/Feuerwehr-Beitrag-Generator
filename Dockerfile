# build stage
FROM node:lts-alpine as build-stage

WORKDIR /ffpostcreator

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage

RUN rm -rf /usr/share/nginx/html/*
COPY --from=build-stage /ffpostcreator/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
