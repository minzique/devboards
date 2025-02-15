FROM node:20-alpine as build
WORKDIR /app
COPY package*.json .
ENV NODE_ENV=production
ENV VITE_API_URL=https://api.jobcafe.lk/v1
RUN npm install
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