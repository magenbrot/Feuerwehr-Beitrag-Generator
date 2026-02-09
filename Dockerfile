# build stage
FROM node:25-alpine3.22 AS build-stage

WORKDIR /ffpostcreator

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:1.29.5-alpine3.23 AS production-stage

RUN rm -rf /usr/share/nginx/html/*
COPY --from=build-stage /ffpostcreator/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
