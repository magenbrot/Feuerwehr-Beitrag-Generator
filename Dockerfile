# build stage
FROM node:26-alpine AS build-stage

WORKDIR /ffpostcreator

COPY package*.json ./

RUN --mount=type=cache,target=/root/.npm npm install

COPY . .

RUN npm run build

# production stage
FROM nginx:mainline-alpine AS production-stage

RUN rm -rf /usr/share/nginx/html/*
COPY --from=build-stage /ffpostcreator/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
