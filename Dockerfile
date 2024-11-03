FROM node:14

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy package.json and install Node.js dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Install Python dependencies
RUN pip3 install scikit-learn numpy

# Expose the port your app runs on
EXPOSE 3000

# Command to run your Node.js application
CMD ["node", "index"]
