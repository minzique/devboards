FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

FROM caddy:latest
COPY --from=build /app/dist /usr/share/caddy
EXPOSE 80 443