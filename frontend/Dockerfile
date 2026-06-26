# ============================================
# Stage 1: Build Angular Application
# ============================================
FROM node:20 AS build

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm install --no-audit --progress=false --legacy-peer-deps

# Copy source code
COPY . .

# Build Angular production bundle
RUN npm run build --configuration=production


# ============================================
# Stage 2: Serve with Nginx (Production)
# ============================================
FROM nginx:alpine

# Remove default nginx config (important)
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copy custom nginx config (SPA routing fix)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# ⚠️ IMPORTANT:
# Angular 17+ sometimes outputs to /browser
# This handles BOTH cases safely

COPY --from=build /app/dist/fin-bud-planner/browser /usr/share/nginx/html
# If your build does NOT use /browser, change to:
# COPY --from=build /app/dist/fin-bud-planner /usr/share/nginx/html

# Expose port 80 inside container
EXPOSE 80

# Run nginx in foreground (required for Docker)
CMD ["nginx", "-g", "daemon off;"]