# Lundao frontend — Vue 3 SPA served by Nginx.
# Stage 1: Vite build. Stage 2: Nginx runtime.

# ================================
# Stage 1: Build
# ================================
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Build-time configuration.
# By default the SPA talks to the backend through Nginx's /api reverse proxy
# on the same host, so VITE_API_BASE_URL is a relative path. Override only
# when deploying the frontend separately from the backend.
ARG VITE_USE_MOCK_DATA=false
ARG VITE_API_BASE_URL=/api
ARG VITE_WATERMARK_ENABLED=true
ARG VITE_WATERMARK_TEXT="论导Lite"
ARG VITE_WATERMARK_OPACITY=0.08

ENV VITE_USE_MOCK_DATA=$VITE_USE_MOCK_DATA
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_WATERMARK_ENABLED=$VITE_WATERMARK_ENABLED
ENV VITE_WATERMARK_TEXT=$VITE_WATERMARK_TEXT
ENV VITE_WATERMARK_OPACITY=$VITE_WATERMARK_OPACITY

RUN npm run build

# ================================
# Stage 2: Production
# ================================
FROM nginx:1.29-alpine

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
