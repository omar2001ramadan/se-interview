FROM node:22-alpine AS build

WORKDIR /app/presentation/slides-src

COPY presentation/slides-src/package.json presentation/slides-src/package-lock.json ./
RUN npm ci

COPY presentation/slides-src ./
RUN npm run build

FROM caddy:2-alpine

COPY presentation/slides-src/Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/presentation/slides-dist /usr/share/caddy
