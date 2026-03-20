FROM node:22-alpine AS build

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend ./
RUN npm run build

FROM caddy:2-alpine

COPY frontend/Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/frontend/build /usr/share/caddy

CMD ["sh", "-c", "printf 'window.__APP_CONFIG__ = { PUBLIC_API_BASE_URL: \"%s\" };\\n' \"$PUBLIC_API_BASE_URL\" > /usr/share/caddy/runtime-config.js && exec caddy run --config /etc/caddy/Caddyfile --adapter caddyfile"]
