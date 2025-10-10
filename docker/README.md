# MCP Bible Docker Setup

This directory contains Docker Compose configurations to run the MCP Bible server in different modes.

## Available Setups

### Development Setups (build locally)
- **MCP-only Mode** (`docker-compose.yml`): Pure MCP protocol with Streaming HTTP - REST API disabled
- **REST Mode** (`docker-compose.rest.yml`): Full REST API + MCP protocol support

### Production Setups (use published images)
- **MCP-only Mode** (`docker-compose.prod.yml`): Uses published GHCR image for MCP-only mode
- **REST Mode** (`docker-compose.prod.rest.yml`): Uses published GHCR image for REST mode

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning dependencies)

## Quick Start

### Development Mode (Recommended for local development)

#### MCP-only Mode (Default)
For pure MCP protocol communication:

```bash
cd docker
docker-compose up --build -d
```

#### REST Mode
For full API access with health checks and documentation:

```bash
cd docker
docker-compose -f docker-compose.rest.yml up --build -d
```

### Production Mode (Uses published images)

**Note**: Production setups use the published Docker image from GHCR and run the package directly from the GitHub repository using `uvx mcp-bible@git+https://github.com/geosp/mcp-bible.git`.

#### MCP-only Mode
For production deployment using published images:

```bash
cd docker
docker-compose -f docker-compose.prod.yml up -d
```

#### REST Mode
For production with full API access:

```bash
cd docker
docker-compose -f docker-compose.prod.rest.yml up -d
```

### Check Status
```bash
# Development MCP-only
docker-compose logs -f mcp-bible

# Development REST
docker-compose -f docker-compose.rest.yml logs -f mcp-bible

# Production MCP-only
docker-compose -f docker-compose.prod.yml logs -f mcp-bible

# Production REST
docker-compose -f docker-compose.prod.rest.yml logs -f mcp-bible
```

### Stop Services
```bash
# Development MCP-only
docker-compose down

# Development REST
docker-compose -f docker-compose.rest.yml down

# Production MCP-only
docker-compose -f docker-compose.prod.yml down

# Production REST
docker-compose -f docker-compose.prod.rest.yml down
```

## Configuration

### Development Setups (Local building)
These setups build the Docker image locally and mount the source code for live development.

#### MCP-only Mode (docker-compose.yml)
The service is configured to:
- Build from the parent directory's Dockerfile
- Mount the project directory as `/app` for live code changes
- Expose port 3000 for MCP communication
- Run in Streaming HTTP mode (`MCP_ONLY=true`) for MCP protocol - **REST API endpoints are disabled**
- Use uvx to run the local MCP Bible package

#### REST Mode (docker-compose.rest.yml)
The service is configured to:
- Build from the parent directory's Dockerfile
- Mount the project directory as `/app` for live code changes
- Expose port 3000 for MCP communication
- Run with full REST API + MCP protocol support
- Use uvx to run the local MCP Bible package

### Production Setups (Published images)
These setups use pre-built images from GitHub Container Registry for faster deployment.

#### MCP-only Mode (docker-compose.prod.yml)
The service is configured to:
- Use published image: `ghcr.io/geosp/mcp-bible:main`
- Expose port 3000 for MCP communication
- Run in Streaming HTTP mode for pure MCP protocol communication
- No source code mounting required

#### REST Mode (docker-compose.prod.rest.yml)
The service is configured to:
- Use published image: `ghcr.io/geosp/mcp-bible:main`
- Expose port 3000 for MCP communication
- Run with full REST API + MCP protocol support
- No source code mounting required

## Development

For development setups, the volume mount allows you to make changes to the code without rebuilding the container. Simply restart the service after changes:

```bash
# Development MCP-only mode
docker-compose restart mcp-bible

# Development REST mode
docker-compose -f docker-compose.rest.yml restart mcp-bible
```

**Note**: Production setups use published images and do not support live code reloading.

## Troubleshooting

- If you encounter permission issues, ensure Docker is running and you have proper permissions
- Check the logs with `docker-compose logs mcp-bible` (or `docker-compose -f docker-compose.rest.yml logs mcp-bible`) for detailed error messages
- The container uses uv for Python package management, which handles dependencies automatically
- **MCP-only mode**: When `MCP_ONLY=true`, REST API endpoints like `/health` are disabled. Only the `/mcp` endpoint is available for MCP protocol communication
- **REST mode**: Full API access available including `/health`, `/docs`, and `/mcp` endpoints
- **Production mode**: Uses `uvx` to run the package directly from the GitHub repository (`git+https://github.com/geosp/mcp-bible.git`)

## Environment Variables

You can add environment variables in the `docker-compose.yml` files under the `environment` section if needed for configuration.

- `MCP_ONLY=true`: Enables Streaming HTTP mode for MCP protocol communication (used in default `docker-compose.yml`)
- `UV_CACHE_DIR=/tmp/uv-cache`: Sets the cache directory for uv package manager

## Advanced: LXC Environment Setup

If you're running in an LXC container (advanced users), you may need special configuration:

### Prerequisites for LXC
- Podman with podman-compose installed
- LXC container configured for privileged operations

### LXC Configuration
Add these lines to your LXC config file:

```
lxc.cap.drop =
lxc.mount.auto = proc:rw sys:rw
```

### Running in LXC
Use `sudo` with podman-compose commands:

```bash
# Development MCP-only mode
sudo podman-compose up --build -d
sudo podman-compose logs -f mcp-bible
sudo podman-compose down

# Development REST mode
sudo podman-compose -f docker-compose.rest.yml up --build -d
sudo podman-compose -f docker-compose.rest.yml logs -f mcp-bible
sudo podman-compose -f docker-compose.rest.yml down

# Production MCP-only mode
sudo podman-compose -f docker-compose.prod.yml up -d
sudo podman-compose -f docker-compose.prod.yml logs -f mcp-bible
sudo podman-compose -f docker-compose.prod.yml down

# Production REST mode
sudo podman-compose -f docker-compose.prod.rest.yml up -d
sudo podman-compose -f docker-compose.prod.rest.yml logs -f mcp-bible
sudo podman-compose -f docker-compose.prod.rest.yml down
```

If you encounter container build failures in LXC, the privileged configuration above should resolve the `/proc` mount permission errors.

## Claude Desktop Integration

To use the MCP Bible server with Claude Desktop, you'll need to install and configure [MCP Bridge](https://github.com/geosp/mcp-bridge), which allows Claude Desktop to connect to remote MCP servers over HTTP/SSE.

### Prerequisites

- Claude Desktop installed
- MCP Bridge installed from GitHub:
  ```bash
  uv pip install git+https://github.com/geosp/mcp-bridge.git
  ```

### Setup Steps

1. **Start your MCP Bible server** using one of the Docker configurations above
2. **Initialize MCP Bridge configuration**:
   ```bash
   mcp-bridge init --name bible
   ```
3. **Edit the configuration file** at `~/.config/mcp-bridge/bible.json`:
   ```json
   {
     "url": "http://localhost:3000/mcp"
   }
   ```
   Adjust the URL if your server is running on a different host/port.

4. **Configure Claude Desktop** by editing the configuration file:

   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

   Add the MCP server configuration:
   ```json
   {
     "mcpServers": {
       "bible": {
         "command": "mcp-bridge",
         "args": ["--config", "bible.json"]
       }
     }
   }
   ```

5. **Restart Claude Desktop**

### Testing the Integration

You can test the bridge connection before configuring Claude Desktop:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | mcp-bridge --config bible.json
```

This should return a JSON response from your MCP Bible server.

### Troubleshooting

- **Bridge not connecting**: Verify your MCP Bible server is running and accessible at the configured URL
- **Claude Desktop not finding tools**: Check that the bridge configuration is correct and Claude Desktop has been restarted

Once configured, Claude Desktop will have access to all Bible passage retrieval tools provided by your MCP server!