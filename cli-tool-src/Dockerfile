# Minimal base image — no web framework needed, so alpine keeps this very small
FROM python:3.12-alpine

WORKDIR /app

# Create a non-root user (Docker security best practice)
RUN adduser -D -h /home/clitool clitool

# Copy the script in (no external dependencies required — stdlib only)
COPY main.py .

# Declare mount points for input/output data.
# These are documentation of intent; actual host paths are supplied at `docker run` time with -v
VOLUME ["/data/input", "/data/output"]

# Default environment values (can be overridden with -e at runtime)
ENV INPUT_DIR=/data/input \
    OUTPUT_DIR=/data/output \
    TOP_N=15 \
    PYTHONUNBUFFERED=1

# Ensure the app directory and future output dir are writable by the non-root user
RUN chown -R clitool:clitool /app
USER clitool

# This is a run-to-completion CLI tool, not a long-lived server — no EXPOSE needed
ENTRYPOINT ["python", "main.py"]
