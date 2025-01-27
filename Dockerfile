# Use the official Mamba image for Python 3.11
FROM mambaorg/micromamba:1.4.2

# Set working directory
WORKDIR /app

# Copy the environment.yml file first (this allows better caching)
COPY environment.yml /tmp/environment.yml

# Create the Conda environment using Mamba
RUN micromamba create -y -n spatial-extractions -f /tmp/environment.yml && \
    micromamba clean --all --yes

# Ensure the Conda environment is activated in future commands
SHELL ["micromamba", "run", "-n", "spatial-extractions", "/bin/bash", "-c"]

# Copy the rest of the app files
COPY . .

# ✅ Create writable directories inside the container
RUN mkdir -p /app/logs && chmod -R 777 /app/logs
RUN mkdir -p /app/uploads && chmod -R 777 /app/uploads

# Expose Flask port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Use ENTRYPOINT to ensure Conda is activated properly
ENTRYPOINT ["micromamba", "run", "-n", "spatial-extractions"]

# Start Flask in debug mode
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
