# Use Node.js as the base image
FROM node:14

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json if present
COPY package*.json ./

# Install Node.js dependencies
RUN npm install --only=production

# Copy the rest of your application code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir scikit-learn numpy

# Expose the port your app runs on
EXPOSE 3000

# Command to run your Node.js application
CMD ["node", "index.js"]
