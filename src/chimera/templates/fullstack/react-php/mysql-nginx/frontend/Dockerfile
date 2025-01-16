FROM node:18-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy app source
COPY . .

# Environment variables
ENV NODE_ENV=development
ENV WATCHPACK_POLLING=true
ENV WDS_SOCKET_PORT=0

# Expose port
EXPOSE 3000

# Start development server
CMD ["npm", "start", "--", "--host", "0.0.0.0"]
