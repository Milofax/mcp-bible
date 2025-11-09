#!/usr/bin/env python3
"""
Test script for Bible MCP Server mode support

This script demonstrates how to test the different server modes.
"""

import subprocess
import sys
import time
import signal
import os
import socket
from contextlib import closing

def find_free_port(start_port=4000, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('localhost', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")

def test_help():
    """Test the help message shows mode options"""
    print("Testing help message...")
    result = subprocess.run([sys.executable, "-m", "mcp_bible.server", "--help"], 
                          capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    if "mode" in result.stdout and "stdio" in result.stdout:
        print("✓ Help message includes mode options")
    else:
        print("✗ Help message missing mode options")
    print()

def test_stdio_mode():
    """Test stdio mode (this will hang waiting for input, so we'll just start and stop it)"""
    print("Testing stdio mode...")
    try:
        # Start the server in stdio mode
        process = subprocess.Popen([sys.executable, "-m", "mcp_bible.server", "--mode", "stdio"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give it a moment to start
        time.sleep(2)
        
        # Check if it's still running (good sign for stdio mode)
        if process.poll() is None:
            print("✓ Stdio mode started successfully")
            process.terminate()
            process.wait(timeout=5)
        else:
            stdout, stderr = process.communicate()
            print("✗ Stdio mode failed to start")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
    except Exception as e:
        print(f"✗ Error testing stdio mode: {e}")
    print()

def test_mcp_mode():
    """Test MCP-only HTTP mode"""
    print("Testing MCP mode...")
    try:
        # Find a free port
        port = find_free_port()
        print(f"Using port {port} for MCP mode test")
        
        # Start the server in MCP mode with --no-auth
        process = subprocess.Popen([
            sys.executable, "-m", "mcp_bible.server", 
            "--mode", "mcp", "--port", str(port), "--no-auth"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("✓ MCP mode started successfully")
            # Try to make a simple HTTP request to check if it's responding
            try:
                # Use curl instead of httpx to avoid import issues
                curl_result = subprocess.run([
                    "curl", "-s", "-w", "%{http_code}", 
                    f"http://localhost:{port}/mcp"
                ], capture_output=True, text=True, timeout=5)
                
                if curl_result.returncode == 0:
                    status_code = curl_result.stdout[-3:]  # Last 3 chars are status code
                    print(f"✓ MCP endpoint responding (status: {status_code})")
                else:
                    print(f"⚠ MCP endpoint check failed: {curl_result.stderr}")
            except Exception as e:
                print(f"⚠ MCP mode running but endpoint check failed: {e}")
            
            process.terminate()
            process.wait(timeout=5)
        else:
            stdout, stderr = process.communicate()
            print("✗ MCP mode failed to start")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
    except Exception as e:
        print(f"✗ Error testing MCP mode: {e}")
    print()

def test_rest_mode():
    """Test REST + MCP HTTP mode"""
    print("Testing REST mode...")
    try:
        # Find a free port
        port = find_free_port()
        print(f"Using port {port} for REST mode test")
        
        # Start the server in REST mode with --no-auth
        process = subprocess.Popen([
            sys.executable, "-m", "mcp_bible.server", 
            "--mode", "rest", "--port", str(port), "--no-auth"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("✓ REST mode started successfully")
            # Try to make requests to both REST and MCP endpoints using curl
            try:
                # Test health endpoint
                health_result = subprocess.run([
                    "curl", "-s", "-w", "%{http_code}", 
                    f"http://localhost:{port}/health"
                ], capture_output=True, text=True, timeout=5)
                
                if health_result.returncode == 0:
                    status_code = health_result.stdout[-3:]
                    print(f"✓ Health endpoint responding (status: {status_code})")
                
                # Test MCP endpoint
                mcp_result = subprocess.run([
                    "curl", "-s", "-w", "%{http_code}", 
                    f"http://localhost:{port}/mcp"
                ], capture_output=True, text=True, timeout=5)
                
                if mcp_result.returncode == 0:
                    status_code = mcp_result.stdout[-3:]
                    print(f"✓ MCP endpoint responding (status: {status_code})")
                
                # Test API docs
                docs_result = subprocess.run([
                    "curl", "-s", "-w", "%{http_code}", 
                    f"http://localhost:{port}/docs"
                ], capture_output=True, text=True, timeout=5)
                
                if docs_result.returncode == 0:
                    status_code = docs_result.stdout[-3:]
                    print(f"✓ API docs responding (status: {status_code})")
                
            except Exception as e:
                print(f"⚠ REST mode running but endpoint check failed: {e}")
            
            process.terminate()
            process.wait(timeout=5)
        else:
            stdout, stderr = process.communicate()
            print("✗ REST mode failed to start")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
    except Exception as e:
        print(f"✗ Error testing REST mode: {e}")
    print()

def test_rest_api():
    """Test the REST API with a sample Bible passage request"""
    print("Testing REST API functionality...")
    try:
        # Find a free port
        port = find_free_port()
        print(f"Using port {port} for REST API test")
        
        # Start the server in REST mode
        process = subprocess.Popen([
            sys.executable, "-m", "mcp_bible.server", 
            "--mode", "rest", "--port", str(port), "--no-auth"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give it time to start
        time.sleep(4)
        
        # Check if it's running
        if process.poll() is None:
            print("✓ REST API server started")
            try:
                # Test the passage endpoint with Mark 2
                curl_result = subprocess.run([
                    "curl", "-s", "-X", "POST", 
                    f"http://localhost:{port}/passage",
                    "-H", "Content-Type: application/json",
                    "-d", '{"passage": "Mark 2:1-5", "version": "ESV"}',
                    "-w", "\nHTTP_CODE:%{http_code}"
                ], capture_output=True, text=True, timeout=10)
                
                if curl_result.returncode == 0:
                    output = curl_result.stdout
                    # Split by the HTTP_CODE marker
                    parts = output.split("\nHTTP_CODE:")
                    json_part = parts[0] if len(parts) > 1 else output
                    status_code = parts[1] if len(parts) > 1 else "unknown"
                    
                    if status_code.strip() == "200" or "HTTP_CODE:200" in output:
                        print("✓ Bible passage API working correctly")
                        # Check for expected JSON fields
                        if '"success":true' in json_part and '"passage":"Mark 2:1-5"' in json_part:
                            print("✓ API returned valid Bible passage data")
                        elif '"success": true' in json_part and 'Mark' in json_part:
                            print("✓ API returned valid Bible passage data (alternate format)")
                        else:
                            print("⚠ API response format unexpected")
                            print(f"Debug - JSON response: {json_part[:200]}...")
                    else:
                        print(f"⚠ API returned non-200 status: {status_code}")
                        print(f"Debug - Full output: {output[:200]}...")
                else:
                    print(f"✗ API test failed: {curl_result.stderr}")
                    
            except Exception as e:
                print(f"⚠ API test failed with exception: {e}")
            
            process.terminate()
            process.wait(timeout=5)
        else:
            stdout, stderr = process.communicate()
            print("✗ REST API server failed to start")
            print(f"stdout: {stdout}")
            print(f"stderr: {stderr}")
    except Exception as e:
        print(f"✗ Error testing REST API: {e}")
    print()

def main():
    """Run all tests"""
    print("Bible MCP Server Mode Support Test")
    print("=" * 40)
    
    # Set minimal environment variables for testing
    os.environ["AUTH_ENABLED"] = "false"  # Disable auth for testing
    os.environ["MCP_AUTH_ENABLED"] = "false"  # Also set the MCP-specific one
    
    test_help()
    test_stdio_mode()
    test_mcp_mode() 
    test_rest_mode()
    test_rest_api()
    
    print("Testing complete!")

if __name__ == "__main__":
    main()