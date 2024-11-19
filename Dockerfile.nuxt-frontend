# Use Node.js LTS as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy the frontend directory and its dependencies
COPY ./frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the entire frontend folder into the image
COPY ./frontend ./

# Build the frontend project
RUN npm run build

# Expose the port Nuxt will run on
EXPOSE 3000

# Start the app
CMD ["npm", "run", "start"]