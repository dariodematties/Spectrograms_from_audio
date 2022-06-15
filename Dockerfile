# Build from Python latest
FROM python:latest

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends libsndfile1 && rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN pip install numpy scipy librosa future Pillow noisereduce

# Import all scripts
COPY . ./

# Add entry point to run the script
ENTRYPOINT [ "python3", "./analyze.py" ]
