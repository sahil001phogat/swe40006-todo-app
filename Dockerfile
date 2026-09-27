# ---- Stage 1: build dependencies in an isolated layer ----
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
# Install into a local user-site directory so we can copy just this into the final image
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Stage 2: minimal runtime image ----
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user to run the app (Docker security best practice)
RUN useradd --create-home --shell /bin/bash appuser

# Bring in only the installed packages from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY app.py .
COPY templates/ templates/

# Make sure the non-root user's local pip packages are on PATH
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Ensure appuser owns the app directory
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Use gunicorn (production WSGI server) instead of Flask's dev server.
# Respects $PORT if the hosting platform injects one (e.g. Render), else defaults to 5000.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 app:app"]
