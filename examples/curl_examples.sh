#!/bin/bash
"""
Example curl commands for Bible MCP Server REST API

This script demonstrates how to use the REST API endpoints.
"""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Bible MCP Server REST API Examples${NC}"
echo "=========================================="

# Start server in background for testing
echo -e "${YELLOW}Starting server...${NC}"
uv run mcp-bible --mode rest --port 4000 --no-auth &
SERVER_PID=$!

# Give server time to start
sleep 3

echo -e "\n${GREEN}1. Health Check${NC}"
curl -s http://localhost:4000/health | jq .

echo -e "\n${GREEN}2. Service Information${NC}"
curl -s http://localhost:4000/info | jq .

echo -e "\n${GREEN}3. Get Mark Chapter 2 (ESV)${NC}"
curl -X POST http://localhost:4000/passage \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "Mark 2",
    "version": "ESV"
  }' | jq .

echo -e "\n${GREEN}4. Get John 3:16 (NIV)${NC}"
curl -X POST http://localhost:4000/passage \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "John 3:16",
    "version": "NIV"
  }' | jq .

echo -e "\n${GREEN}5. Get Multiple Passages${NC}"
curl -X POST http://localhost:4000/passage \
  -H "Content-Type: application/json" \
  -d '{
    "passage": "John 3:16; Romans 8:28",
    "version": "ESV"
  }' | jq .

# Clean up
echo -e "\n${YELLOW}Stopping server...${NC}"
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo -e "\n${GREEN}Complete! Use these curl commands with your running server.${NC}"