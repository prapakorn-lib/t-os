#!/bin/bash
# API Testing Script
# Usage: ./test_api.sh

# Configuration
API_URL="http://localhost:8000"
API_KEY="your-secret-api-key-here"  # Change this to your actual API key

echo "=================================="
echo "FastAPI Testing Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Root endpoint
echo -e "${YELLOW}Test 1: Root Endpoint${NC}"
echo "GET /"
curl -s "${API_URL}/" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 2: Health check
echo -e "${YELLOW}Test 2: Health Check${NC}"
echo "GET /health"
curl -s "${API_URL}/health" | python3 -m json.tool
echo ""
echo "---"
echo ""

# Test 3: Get all items without API key (should fail)
echo -e "${YELLOW}Test 3: Get Items Without API Key (Expected: 403)${NC}"
echo "GET /items (no API key)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "${API_URL}/items")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d':' -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "403" ]; then
    echo -e "${GREEN}✓ PASS: Correctly rejected (403)${NC}"
else
    echo -e "${RED}✗ FAIL: Expected 403, got $http_code${NC}"
fi
echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
echo ""
echo "---"
echo ""

# Test 4: Get all items with API key
echo -e "${YELLOW}Test 4: Get All Items With API Key${NC}"
echo "GET /items (with API key)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -H "X-API-Key: ${API_KEY}" "${API_URL}/items")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d':' -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ PASS: Successfully retrieved items (200)${NC}"
else
    echo -e "${RED}✗ FAIL: Expected 200, got $http_code${NC}"
fi
echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
echo ""
echo "---"
echo ""

# Test 5: Get specific item
echo -e "${YELLOW}Test 5: Get Item by ID${NC}"
echo "GET /items/1 (with API key)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -H "X-API-Key: ${API_KEY}" "${API_URL}/items/1")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d':' -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "200" ]; then
    echo -e "${GREEN}✓ PASS: Successfully retrieved item (200)${NC}"
else
    echo -e "${RED}✗ FAIL: Expected 200, got $http_code${NC}"
fi
echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
echo ""
echo "---"
echo ""

# Test 6: Get non-existent item
echo -e "${YELLOW}Test 6: Get Non-existent Item (Expected: 404)${NC}"
echo "GET /items/999 (with API key)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -H "X-API-Key: ${API_KEY}" "${API_URL}/items/999")
http_code=$(echo "$response" | grep HTTP_CODE | cut -d':' -f2)
body=$(echo "$response" | grep -v HTTP_CODE)

if [ "$http_code" = "404" ]; then
    echo -e "${GREEN}✓ PASS: Correctly returned 404${NC}"
else
    echo -e "${RED}✗ FAIL: Expected 404, got $http_code${NC}"
fi
echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
echo ""
echo "---"
echo ""

# Test 7: Performance test
echo -e "${YELLOW}Test 7: Response Time Test${NC}"
echo "Measuring response time for GET /items..."
time_result=$( { time curl -s -H "X-API-Key: ${API_KEY}" "${API_URL}/items" > /dev/null; } 2>&1 | grep real | awk '{print $2}')
echo "Response time: $time_result"
echo ""

# Summary
echo "=================================="
echo "Test Summary"
echo "=================================="
echo "API URL: ${API_URL}"
echo "All tests completed!"
echo ""
echo "For more detailed testing, visit:"
echo "  ${API_URL}/docs (Swagger UI)"
echo "=================================="
