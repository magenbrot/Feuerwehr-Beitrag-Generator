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

# Copy built app
COPY --from=build-stage /ffpostcreator/dist /usr/share/nginx/html

# Copy default assets to /defaults (used to seed the volume on first run)
COPY --from=build-stage /ffpostcreator/dist/assets /defaults

# Entrypoint script seeds the volume on first start
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
