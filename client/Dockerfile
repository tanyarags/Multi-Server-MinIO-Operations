FROM python:3.9-slim

# Basic environment setup
ENV PYTHONUNBUFFERED=1
ENV TERM=xterm-256color

# Working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    iputils-ping \
    net-tools \
    tmux \
    less \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /app/demo_files /app/scripts

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy client code
COPY minio_wrapper.py .
COPY minio_demo.py .
COPY entrypoint.sh .

# Copy all folders
COPY ./scripts /app/scripts
COPY ./config /app/config
COPY ./demo_files /app/demo_files

# Make scripts executable
RUN chmod +x /app/scripts/*.py

# Optional: Copy tmux configuration for better defaults
RUN echo "set -g mouse on" > /root/.tmux.conf && \
    echo "set -g history-limit 10000" >> /root/.tmux.conf && \
    echo "set -g default-terminal \"screen-256color\"" >> /root/.tmux.conf && \
    echo "set -g status-bg black" >> /root/.tmux.conf && \
    echo "set -g status-fg white" >> /root/.tmux.conf

# Make entrypoint executable
# RUN chmod +x entrypoint.sh

# # Set entrypoint
# ENTRYPOINT ["/app/entrypoint.sh"]

# Keep container running
CMD ["tail", "-f", "/dev/null"]