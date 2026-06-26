# ============================================
# Stage 1: Build Angular Application
# ============================================
# Use Node.js 20 as the build environment
FROM node:20 as build

# Set working directory to /app inside the container
WORKDIR /app

# Copy package.json and package-lock.json files first
# This leverages Docker layer caching for faster rebuilds
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy all frontend source code to container
COPY . .

# Build Angular application for production
# --configuration=production: Optimizes build for production (minification, tree-shaking)
RUN npm run build --configuration=production

# ============================================
# Stage 2: Serve with Nginx (Production)
# ============================================
# Use lightweight Nginx Alpine image for serving static files
FROM nginx:alpine

# Copy built Angular app from Stage 1 to Nginx html directory
# /app/dist/fin-bud-planner: Output directory from Angular build (from angular.json)
# /usr/share/nginx/html: Default Nginx static file directory
COPY --from=build /app/dist/fin-bud-planner /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Nginx in foreground mode
# -g "daemon off;": Run Nginx in foreground (required for Docker containers)
CMD ["nginx", "-g", "daemon off;"]
