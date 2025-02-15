FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .

ENV VITE_API_URL=https://api.jobcafe.lk/v1

# Install dependencies with explicit CI=false to avoid treating warnings as errors
RUN npm ci --no-audit --no-fund --loglevel=error
COPY . .
RUN npm run build

# --- Production stage ---
FROM nginx:alpine
# Copy the built static files to Nginx's public folder.
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for HTTP traffic.
EXPOSE 80

# Start Nginx in the foreground.
CMD ["nginx", "-g", "daemon off;"]