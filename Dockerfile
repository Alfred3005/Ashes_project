# Use the NVIDIA PyTorch base image
FROM nvcr.io/nvidia/pytorch:23.12-py3

# Install dependencies for Kivy
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean

RUN apt-get update && apt-get install -y xclip xsel

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install transformers==4.28.0 tokenizers==0.12.1 requests beautifulsoup4 pandas numpy

# Copy the requirements.txt file into the container
COPY requirements.txt /tmp/

# Install additional Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the application code into the container
COPY . /app/

# Set the working directory
WORKDIR /app

# Expose the application port
EXPOSE 8082
