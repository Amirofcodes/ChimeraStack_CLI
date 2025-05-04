# templates/stacks/frontend/react-static/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package.json and potentially package-lock.json
COPY package*.json ./

# Install dependencies quietly
RUN npm ci

# Copy the rest of the application code
COPY . .

# production build
RUN npm run build

# ---------- development ----------
ARG FRONTEND_PORT=3000
ENV FRONTEND_PORT=${FRONTEND_PORT}

# Expose the port the app runs on
EXPOSE ${FRONTEND_PORT}

# Command to run the app
CMD ["npm","run","dev","--","--host","0.0.0.0","--port","${FRONTEND_PORT}"]
