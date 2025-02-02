# Use the official Mamba image
FROM mambaorg/micromamba:1.4.2

# Set working directory
WORKDIR /app

# Switch to root to manage permissions
USER root

# Copy environment file
COPY environment.yml /tmp/environment.yml

# Create Conda environment
RUN micromamba create -y -n spatial-extractions -f /tmp/environment.yml && \
    micromamba clean --all --yes

# ✅ Fix permissions: Create logs/uploads with full access
RUN mkdir -p /app/logs /app/uploads && \
    chown -R mambauser:mambauser /app && \
    chmod -R 775 /app/logs /app/uploads

# Switch back to the default user (mambauser)
USER mambauser

# Ensure the environment is activated
SHELL ["micromamba", "run", "-n", "spatial-extractions", "/bin/bash", "-c"]

# Copy the rest of the app files
COPY . .

EXPOSE 5000

# Environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Run the app
ENTRYPOINT ["micromamba", "run", "-n", "spatial-extractions"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug", "--reload"]
