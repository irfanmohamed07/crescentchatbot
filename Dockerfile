# Start with the Node.js base image
FROM node:14

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip
# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json if present
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Install Python dependencies
COPY requirements.txt .  # Ensure you have a requirements.txt file in your project
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 3000

# Command to run your Node.js application
CMD ["node", "index"]
