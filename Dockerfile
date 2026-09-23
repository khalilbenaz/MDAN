# MCP server image for self-hosting (Glama builds from the spec in glama.json).
FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts && npm cache clean --force
COPY _mdan ./_mdan
COPY tools ./tools
COPY LICENSE README.md ./
ENV NODE_ENV=production MDAN_PROJECT_ROOT=/workspace
RUN mkdir -p /workspace && chown node:node /workspace
USER node
# stdio by default; `docker run -p 3100:3100 image --http --host 0.0.0.0` for Streamable HTTP.
ENTRYPOINT ["node", "tools/mcp/bin.js"]
