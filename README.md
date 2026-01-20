# Bible MCP Server

A Model Context Protocol (MCP) server that provides Bible passage retrieval functionality using the `mcp-weather` core infrastructure.

This server enables AI assistants to access Bible passages from various translations, with support for multiple deployment modes:

- **`--mode stdio`** (default): MCP protocol over stdin/stdout for direct AI assistant integration
- **`--mode mcp`**: MCP protocol over HTTP for networked AI assistant access  
- **`--mode rest`**: Both REST API and MCP protocol over HTTP for maximum flexibility

## Features

The Bible MCP Server provides:

### MCP Tools (for AI assistants)
- `get_passage(passage, version)` - Retrieve Bible passages. Supports multiple passages separated by semicolons (e.g., "John 3:16; Romans 8:28").

### REST API Endpoints
- `GET /health` - Health check
- `GET /info` - Service information
- `POST /passage` - Get Bible passage
- `GET /docs` - OpenAPI documentation (Swagger UI)

### Supported Bible Versions

**English:**
- ESV (English Standard Version)
- NIV (New International Version)
- KJV (King James Version)
- NASB (New American Standard Bible)
- NKJV (New King James Version)
- NLT (New Living Translation)
- AMP (Amplified Bible)
- MSG (The Message)

**German (Deutsch):**
- HOF (Hoffnung für Alle)
- LUTH1545 (Luther Bibel 1545)
- NGU-DE (Neue Genfer Übersetzung) - NT only
- SCH1951 (Schlachter 1951)
- SCH2000 (Schlachter 2000)

## Installation

### Prerequisites
- Python 3.10+
- `uv` package manager

#### Installing uv

**On Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatively, you can install uv using pip:
```bash
pip install uv
```

After installation, restart your terminal or run `source ~/.bashrc` (Linux/macOS) or restart your command prompt (Windows).

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
vi .env
```

## Usage

The Bible MCP server supports three deployment modes via command-line arguments:

### Mode 1: stdio (Default) - Direct AI Assistant Integration

```bash
# Default mode - MCP over stdin/stdout
uv run mcp-bible

# Explicitly specify stdio mode  
uv run mcp-bible --mode stdio
```

Perfect for direct integration with AI assistants like GitHub Copilot, Claude Desktop, etc.

### Mode 2: mcp - MCP Protocol over HTTP

```bash
# MCP-only server on HTTP (no REST API)
uv run mcp-bible --mode mcp --port 3000 --no-auth
```

Provides MCP protocol over HTTP at `http://localhost:3000/mcp` for networked AI assistant access.

### Mode 3: rest - Full HTTP Server (REST + MCP)

```bash
# Full server with both REST API and MCP protocol
uv run mcp-bible --mode rest --port 3000 --no-auth
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
- "Zeige mir Johannes 3:16 auf Deutsch" (uses SCH2000 or HOF)

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

# Get multiple passages
curl -X POST "http://localhost:3000/passage" \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "John 3:16; Romans 8:28; Philippians 4:13",
    "version": "NIV"
  }'

# Get an entire chapter
curl -X POST "http://localhost:3000/passage" \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "Mark 2",
    "version": "ESV"
  }'

# Get a German passage (Schlachter 2000)
curl -X POST "http://localhost:3000/passage" \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "Johannes 3:16",
    "version": "SCH2000"
  }'

# Get a German passage (Hoffnung für Alle)
curl -X POST "http://localhost:3000/passage" \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "Psalm 23",
    "version": "HOF"
  }'
```

### CLI Help and Options

```bash
# See all available options
uv run mcp-bible --help

# Usage examples:
uv run mcp-bible                         # stdio mode (default)
uv run mcp-bible --mode stdio            # stdio mode
uv run mcp-bible --mode mcp --port 4000  # MCP-only HTTP on port 4000
uv run mcp-bible --mode rest --port 4000 # REST+MCP HTTP on port 4000
uv run mcp-bible --mode rest --no-auth   # Disable authentication
```

### Environment Variables (Alternative to CLI)

You can also configure the server using environment variables:

```bash
# Alternative: Set environment variables
export MCP_TRANSPORT=http        # stdio or http
export MCP_ONLY=false           # true for MCP-only, false for REST+MCP
export MCP_HOST=0.0.0.0         # Host to bind to
export MCP_PORT=3000            # Port number
export AUTH_ENABLED=false       # Enable/disable authentication

# Then run without arguments
uv run mcp-bible
```

### Test All Modes

Run the comprehensive test suite:

```bash
uv run tests/test_modes.py
```

Or try the interactive curl examples:

```bash
./examples/curl_examples.sh
```

## Project Structure

```
mcp_bible/
├── __init__.py              # Package metadata
├── config.py                # Configuration management (extends mcp-weather core)
├── bible_service.py         # Business logic (Bible API client)
├── service.py               # MCP service wrapper (with automatic feature discovery)
├── server.py                # Server implementation (CLI mode support)
├── features/                # Feature modules (MODULAR PATTERN)
│   ├── __init__.py
│   └── get_passage/         # Get passage feature
│       ├── __init__.py
│       ├── instructions.md  # 📝 Comprehensive documentation (core.utils)
│       ├── models.py        # Feature-specific models
│       ├── tool.py          # MCP tool definition (uses @inject_docstring)
│       └── routes.py        # REST API endpoints (uses load_instruction)
├── shared/                  # Shared models and utilities
│   ├── __init__.py
│   └── models.py            # Base models, error types
├── tests/                   # Test suite
│   └── test_modes.py        # Mode support testing
└── examples/                # Usage examples
    └── curl_examples.sh     # Interactive REST API examples
```

### Core.utils Integration

This project uses the **core.utils pattern** from mcp-weather for dynamic documentation:

- **`instructions.md`**: Comprehensive feature documentation in markdown
- **`@inject_docstring`**: Dynamically injects markdown into MCP tool docstrings
- **`load_instruction`**: Loads markdown for REST API documentation
- **Single source of truth**: Same documentation for both MCP tools and REST endpoints

## How It Works

### Features Pattern (Automatic Discovery)

This server uses **automatic feature discovery** - just like `mcp-weather`!

**Add a new feature in 4 steps:**

1. **Create feature directory**: `features/my_feature/`
2. **Add instructions.md**: Comprehensive documentation in markdown
3. **Add tool.py**: With `register_tool(mcp, service)` function using `@inject_docstring`
4. **Add routes.py** (optional): With `create_router(service)` function using `load_instruction`

**Example feature structure:**

```python
# features/my_feature/tool.py
from core.utils import inject_docstring, load_instruction

@mcp.tool()
@inject_docstring(lambda: load_instruction("instructions.md", __file__))
async def my_tool(param: str) -> dict:
    """Documentation loaded from instructions.md"""
    return {"result": param}

# features/my_feature/routes.py  
from core.utils import load_instruction

@router.post("/endpoint", description=load_instruction("instructions.md", __file__))
async def endpoint():
    """Same documentation for REST API"""
    return {"data": "value"}
```

**That's it!** The service automatically:
- Discovers your feature
- Registers MCP tools from `tool.py` 
- Includes REST routes from `routes.py`
- Loads documentation from `instructions.md`

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

✅ **No boilerplate** - Server infrastructure is ready to use  
✅ **Multiple deployment modes** - stdio, MCP-only HTTP, REST+MCP HTTP via CLI  
✅ **Dynamic documentation** - Markdown-based docs via core.utils  
✅ **Dual interfaces** - MCP + REST API automatically  
✅ **Configuration** - Environment variable management  
✅ **Error handling** - Comprehensive exception handling  
✅ **Type safety** - Full Pydantic models and type hints  
✅ **Async support** - Async-first design throughout  
✅ **Logging** - Structured logging built-in  
✅ **CORS** - Configurable CORS support  
✅ **Health checks** - Standard endpoints  
✅ **Testing** - Comprehensive test suite included

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

## Features Implemented ✅

✅ **Multiple deployment modes** (stdio, mcp, rest)  
✅ **CLI interface** with comprehensive help  
✅ **Dynamic documentation** using core.utils  
✅ **Bible passage retrieval** from BibleGateway.com  
✅ **13 Bible translations** supported (8 English + 5 German)  
✅ **Multiple passage support** (semicolon-separated)  
✅ **Comprehensive test suite** with mode testing  
✅ **REST API examples** and curl scripts  
✅ **Auto-discovery** of features  
✅ **Structured logging** throughout  

## Next Steps

- Add authentication providers (Authentik integration)
- Add more Bible API sources (Bible API, ESV API) 
- Implement passage search and concordance
- Add daily verses and reading plans
- Add Redis caching for performance
- Add metrics and monitoring
- Add Docker deployment examples

## Learn More

- [Using mcp-weather as Dependency](https://github.com/geosp/mcp-weather/blob/master/docs/USING_AS_DEPENDENCY.md)
- [Main mcp-weather README](https://github.com/geosp/mcp-weather/blob/master/README.md)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## License

This project is provided as-is for use and modification.