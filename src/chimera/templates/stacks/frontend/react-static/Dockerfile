# templates/stacks/frontend/react-static/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package.json and potentially package-lock.json
COPY package.json package-lock.json* ./

# Install dependencies quietly
RUN npm install --quiet

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the app
CMD ["npm", "start"]
