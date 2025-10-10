# Bible MCP Server

A Model Context Protocol (MCP) server that provides Bible passage retrieval functionality using the `mcp-weather` core infrastructure.

This server enables AI assistants to access Bible passages from various translations, with both MCP protocol support and REST API endpoints.

## Features

The Bible MCP Server provides:

### MCP Tools (for AI assistants)
- `get_passage(passage, version)` - Retrieve Bible passages from BibleGateway.com

### REST API Endpoints
- `GET /health` - Health check
- `GET /info` - Service information
- `POST /passage` - Get Bible passage
- `GET /docs` - OpenAPI documentation (Swagger UI)

### Supported Bible Versions
- ESV (English Standard Version)
- NIV (New International Version)
- KJV (King James Version)
- NASB (New American Standard Bible)
- NKJV (New King James Version)
- NLT (New Living Translation)
- AMP (Amplified Bible)
- MSG (The Message)

## Installation

### Prerequisites
- Python 3.10+
- `uv` package manager (or `pip`)

### Step 1: Install Dependencies

```bash
# From this directory
cd mcp-bible

# Install dependencies
uv sync
```

### Step 2: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings
nano .env
```

## Usage

### Run in MCP-only Mode (stdio)

```bash
# Set transport to stdio in .env
export MCP_TRANSPORT=stdio
export MCP_ONLY=true

# Run the server
python -m mcp_bible.server
```

### Run in HTTP Mode with REST API

```bash
# Set transport to HTTP in .env
export MCP_TRANSPORT=http
export MCP_ONLY=false
export MCP_PORT=3000

# Run the server
python -m mcp_bible.server
```

The server will start at `http://localhost:3000` with:
- MCP endpoint: `http://localhost:3000/mcp`
- REST API: `http://localhost:3000/*`
- API docs: `http://localhost:3000/docs`
- Health check: `http://localhost:3000/health`

### Test the MCP Tools

You can test the MCP tools by connecting GitHub Copilot or using a test client:

```json
// .vscode/mcp.json
{
  "servers": {
    "bible": {
      "type": "http",
      "url": "http://localhost:3000/mcp"
    }
  }
}
```

Then ask Copilot:
- "Show me John 3:16"
- "What does Romans 8 say?"
- "Read Psalm 23 in NIV"

### Test the REST API

```bash
# Health check
curl http://localhost:3000/health

# Get service info
curl http://localhost:3000/info

# Get a Bible passage
curl -X POST "http://localhost:3000/passage" \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "John 3:16",
    "version": "ESV"
  }'
```

## Project Structure

```
mcp_bible/
├── __init__.py              # Package metadata
├── config.py                # Configuration management
├── bible_service.py         # Business logic (Bible API client)
├── service.py               # MCP service wrapper (with feature discovery)
├── server.py                # Server implementation
├── features/                # Feature modules (MODULAR PATTERN)
│   ├── __init__.py
│   ├── get_passage/         # Get passage feature
│   │   ├── __init__.py
│   │   ├── models.py        # Feature-specific models
│   │   ├── tool.py          # MCP tool definition
│   │   └── routes.py        # REST API endpoints
└── shared/                  # Shared models and utilities
    ├── __init__.py
    └── models.py            # Base models, error types
```

## How It Works

### Features Pattern (Automatic Discovery)

This server uses **automatic feature discovery** - just like `mcp-weather`!

**Add a new feature in 3 steps:**

1. **Create feature directory**: `features/my_feature/`
2. **Add tool.py**: With `register_tool(mcp, service)` function
3. **Add routes.py** (optional): With `create_router(service)` function

**That's it!** The service automatically:
- Discovers your feature
- Registers MCP tools from `tool.py`
- Includes REST routes from `routes.py`

No manual registration needed!

### 1. Configuration Layer (config.py)

Extends core configuration classes with service-specific settings:

```python
from core.config import BaseServerConfig

class BibleAPIConfig(BaseModel):
    base_url: str
    supported_versions: List[str]

class AppConfig(BaseModel):
    server: ServerConfig
    bible_api: BibleAPIConfig
```

### 2. Business Logic Layer (bible_service.py)

Pure business logic, independent of MCP/REST:

```python
class BibleService:
    async def fetch_passage(self, passage: str, version: str) -> dict:
        # Bible passage retrieval logic here
        ...
```

### 3. MCP Service Wrapper (service.py)

Implements `BaseService` to expose business logic via MCP:

```python
from core.server import BaseService

class BibleMCPService(BaseService):
    def register_mcp_tools(self, mcp: FastMCP) -> None:
        # Automatic feature discovery and registration
```

### 4. Server Implementation (server.py)

Extends `BaseMCPServer` to create the complete server:

```python
from core.server import BaseMCPServer

class BibleMCPServer(BaseMCPServer):
    @property
    def service_title(self) -> str:
        return "Bible MCP Server"

    def create_router(self) -> APIRouter:
        # Add REST endpoints
        ...
```

## Key Benefits of Using mcp-weather Core

By using `mcp-weather` as a dependency, you get:

✅ No boilerplate - Server infrastructure is ready to use
✅ Dual interfaces - MCP + REST API automatically
✅ Configuration - Environment variable management
✅ Error handling - Comprehensive exception handling
✅ Type safety - Full Pydantic models and type hints
✅ Async support - Async-first design throughout
✅ Logging - Structured logging built-in
✅ CORS - Configurable CORS support
✅ Health checks - Standard endpoints

## Customization

### Add New MCP Tools

Edit `mcp_bible/service.py`:

```python
def register_mcp_tools(self, mcp: FastMCP) -> None:
    @mcp.tool()
    async def my_new_tool(param: str) -> dict:
        """Tool description for AI"""
        return {"result": "value"}
```

### Add New REST Endpoints

Edit `mcp_bible/server.py`:

```python
def create_router(self) -> APIRouter:
    router = APIRouter()

    @router.get("/my-endpoint")
    async def my_endpoint():
        return {"data": "value"}

    return router
```

### Add New Configuration

Edit `mcp_bible/config.py`:

```python
class BibleAPIConfig(BaseModel):
    my_new_field: str = Field(default="value")
```

## Troubleshooting

### Import Errors

Make sure you're importing from `core`, not `mcp_weather.core`:

```python
from core.server import BaseMCPServer  # ✅ Correct
from mcp_weather.core.server import BaseMCPServer  # ❌ Wrong
```

### Module Not Found

Make sure mcp-weather is installed:

```bash
uv pip list | grep mcp-weather
```

If not installed, install it:

```bash
uv sync  # Installs from pyproject.toml
```

## Next Steps

- Add real Bible API integration (BibleGateway, ESV API, etc.)
- Add more Bible versions
- Implement passage search
- Add daily verses
- Implement caching
- Add metrics and monitoring

## Learn More

- [Using mcp-weather as Dependency](https://github.com/geosp/mcp-weather/blob/master/docs/USING_AS_DEPENDENCY.md)
- [Main mcp-weather README](https://github.com/geosp/mcp-weather/blob/master/README.md)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## License

This project is provided as-is for use and modification.