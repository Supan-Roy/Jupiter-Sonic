# Base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install dependencies first (leverage docker layer cache)
COPY package.json package-lock.json* ./
RUN npm install

# Copy application files
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start development server with host configuration
CMD ["npm", "run", "dev", "--", "--host"]
