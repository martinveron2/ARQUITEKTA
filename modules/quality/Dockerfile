FROM node:22-bookworm-slim AS node
FROM mcr.microsoft.com/playwright/python:v1.58.0-noble
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
 && apt-get update && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /engine
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY arquitekta_quality ./arquitekta_quality
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "-m", "arquitekta_quality.server"]
CMD ["--host", "0.0.0.0", "--projects", "/config/projects.json", "--data", "/data"]
