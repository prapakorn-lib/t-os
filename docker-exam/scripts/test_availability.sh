#!/bin/bash

# Availability Testing Script
# Concert Ticket Booking System

echo "=========================================="
echo "Availability Testing"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Container Status Check
echo "=========================================="
echo "Test 1: Container Status Check"
echo "=========================================="
echo "Standard: All containers should be running"
echo ""

docker-compose ps

echo ""
frontend_status=$(docker-compose ps | grep concert-frontend | grep "Up" | wc -l)
database_status=$(docker-compose ps | grep concert-database | grep "Up" | wc -l)

if [ $frontend_status -eq 1 ] && [ $database_status -eq 1 ]; then
    echo -e "${GREEN}✓ PASSED - All containers are running${NC}"
else
    echo -e "${RED}✗ FAILED - Some containers are not running${NC}"
fi
echo ""

# Test 2: Health Check Endpoint
echo "=========================================="
echo "Test 2: Health Check Endpoint"
echo "=========================================="
echo "Standard: Health endpoint should return status 200"
echo ""

health_response=$(curl -s -w "\n%{http_code}" http://localhost:3000/health)
health_body=$(echo "$health_response" | head -n -1)
health_code=$(echo "$health_response" | tail -1)

echo "HTTP Status Code: $health_code"
echo "Response Body:"
echo "$health_body" | jq '.' 2>/dev/null || echo "$health_body"
echo ""

if [ "$health_code" = "200" ]; then
    echo -e "${GREEN}✓ PASSED - Health check returns 200${NC}"
else
    echo -e "${RED}✗ FAILED - Health check returns $health_code${NC}"
fi
echo ""

# Test 3: Restart Policy Check
echo "=========================================="
echo "Test 3: Restart Policy Check"
echo "=========================================="
echo "Standard: Restart policy should be 'unless-stopped' or 'always'"
echo ""

echo "Frontend Restart Policy:"
frontend_restart=$(docker inspect concert-frontend | jq -r '.[0].HostConfig.RestartPolicy.Name')
echo "  Policy: $frontend_restart"

if [ "$frontend_restart" = "unless-stopped" ] || [ "$frontend_restart" = "always" ]; then
    echo -e "  ${GREEN}✓ PASSED${NC}"
else
    echo -e "  ${RED}✗ FAILED - Should be 'unless-stopped' or 'always'${NC}"
fi

echo ""
echo "Database Restart Policy:"
database_restart=$(docker inspect concert-database | jq -r '.[0].HostConfig.RestartPolicy.Name')
echo "  Policy: $database_restart"

if [ "$database_restart" = "unless-stopped" ] || [ "$database_restart" = "always" ]; then
    echo -e "  ${GREEN}✓ PASSED${NC}"
else
    echo -e "  ${RED}✗ FAILED - Should be 'unless-stopped' or 'always'${NC}"
fi
echo ""

# Test 4: Auto-restart Test
echo "=========================================="
echo "Test 4: Auto-restart Test"
echo "=========================================="
echo "Standard: Container should restart automatically after stopping"
echo ""

echo "Stopping frontend container..."
docker stop concert-frontend > /dev/null

echo "Waiting 10 seconds for auto-restart..."
sleep 10

echo "Checking container status..."
frontend_running=$(docker ps | grep concert-frontend | wc -l)

if [ $frontend_running -eq 1 ]; then
    echo -e "${GREEN}✓ PASSED - Container restarted automatically${NC}"
else
    echo -e "${RED}✗ FAILED - Container did not restart${NC}"
    echo "Manually restarting container..."
    docker-compose up -d frontend > /dev/null
    sleep 5
fi
echo ""

# Test 5: Database Health Check
echo "=========================================="
echo "Test 5: Database Health Check"
echo "=========================================="
echo "Standard: Database should be accepting connections"
echo ""

db_health=$(docker exec concert-database pg_isready -U concert_user -d concert_db)
echo "$db_health"

if echo "$db_health" | grep -q "accepting connections"; then
    echo -e "${GREEN}✓ PASSED - Database is accepting connections${NC}"
else
    echo -e "${RED}✗ FAILED - Database is not ready${NC}"
fi
echo ""

# Test 6: Continuous Availability Test
echo "=========================================="
echo "Test 6: Continuous Availability Test (60s)"
echo "=========================================="
echo "Standard: Availability should be ≥ 99%"
echo ""

echo "Testing availability for 60 seconds..."
echo "Checking health endpoint every 2 seconds..."
echo ""

start_time=$(date +%s)
end_time=$((start_time + 60))
success_count=0
fail_count=0

while [ $(date +%s) -lt $end_time ]; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))

    if curl -s -f http://localhost:3000/health > /dev/null 2>&1; then
        ((success_count++))
        echo -ne "\rElapsed: ${elapsed}s | Success: $success_count | Failed: $fail_count | "
    else
        ((fail_count++))
        echo -ne "\rElapsed: ${elapsed}s | Success: $success_count | Failed: $fail_count | "
    fi

    sleep 2
done

echo ""
echo ""

total_checks=$((success_count + fail_count))
if [ $total_checks -gt 0 ]; then
    availability=$(echo "scale=2; $success_count * 100 / $total_checks" | bc)
else
    availability=0
fi

echo "Results:"
echo "  Total Checks: $total_checks"
echo "  Successful: $success_count"
echo "  Failed: $fail_count"
echo "  Availability: ${availability}%"

if (( $(echo "$availability >= 99" | bc -l) )); then
    echo -e "  ${GREEN}✓ PASSED - Availability ≥ 99%${NC}"
else
    echo -e "  ${RED}✗ FAILED - Availability < 99%${NC}"
fi
echo ""

# Test 7: Resource Usage Check
echo "=========================================="
echo "Test 7: Resource Usage Check"
echo "=========================================="
echo ""

echo "Current resource usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" concert-frontend concert-database

echo ""

# Test 8: Check Logs for Errors
echo "=========================================="
echo "Test 8: Error Log Analysis"
echo "=========================================="
echo ""

echo "Checking frontend logs for errors (last 50 lines)..."
frontend_errors=$(docker-compose logs --tail=50 frontend | grep -i "error" | wc -l)
echo "  Found $frontend_errors error messages"

echo ""
echo "Checking database logs for errors (last 50 lines)..."
database_errors=$(docker-compose logs --tail=50 database | grep -i "error\|fatal" | wc -l)
echo "  Found $database_errors error messages"

echo ""
if [ $frontend_errors -eq 0 ] && [ $database_errors -eq 0 ]; then
    echo -e "${GREEN}✓ No critical errors found in logs${NC}"
else
    echo -e "${YELLOW}⚠ Found some error messages - review logs for details${NC}"
fi
echo ""

# Summary
echo "=========================================="
echo "Availability Testing Summary"
echo "=========================================="
echo ""

all_passed=true

echo "Test Results:"
if [ $frontend_status -eq 1 ] && [ $database_status -eq 1 ]; then
    echo -e "  1. Container Status: ${GREEN}PASSED${NC}"
else
    echo -e "  1. Container Status: ${RED}FAILED${NC}"
    all_passed=false
fi

if [ "$health_code" = "200" ]; then
    echo -e "  2. Health Check: ${GREEN}PASSED${NC}"
else
    echo -e "  2. Health Check: ${RED}FAILED${NC}"
    all_passed=false
fi

if ([ "$frontend_restart" = "unless-stopped" ] || [ "$frontend_restart" = "always" ]) && \
   ([ "$database_restart" = "unless-stopped" ] || [ "$database_restart" = "always" ]); then
    echo -e "  3. Restart Policy: ${GREEN}PASSED${NC}"
else
    echo -e "  3. Restart Policy: ${RED}FAILED${NC}"
    all_passed=false
fi

if [ $frontend_running -eq 1 ]; then
    echo -e "  4. Auto-restart: ${GREEN}PASSED${NC}"
else
    echo -e "  4. Auto-restart: ${RED}FAILED${NC}"
    all_passed=false
fi

if echo "$db_health" | grep -q "accepting connections"; then
    echo -e "  5. Database Health: ${GREEN}PASSED${NC}"
else
    echo -e "  5. Database Health: ${RED}FAILED${NC}"
    all_passed=false
fi

if (( $(echo "$availability >= 99" | bc -l) )); then
    echo -e "  6. Continuous Availability: ${GREEN}PASSED${NC} (${availability}%)"
else
    echo -e "  6. Continuous Availability: ${RED}FAILED${NC} (${availability}%)"
    all_passed=false
fi

echo ""
echo "Overall Assessment:"
if [ "$all_passed" = true ]; then
    echo -e "${GREEN}✓ PASSED - System meets availability standards${NC}"
else
    echo -e "${RED}✗ FAILED - System does not meet all availability standards${NC}"
    echo ""
    echo "Recommendations for improvement:"
    echo "  - Ensure all containers have proper restart policies"
    echo "  - Implement health checks in docker-compose.yml"
    echo "  - Set up monitoring and alerting"
    echo "  - Review and fix errors in logs"
    echo "  - Consider using orchestration tools (Kubernetes, Docker Swarm)"
fi

echo ""
echo "=========================================="
echo "Availability Testing Completed"
echo "=========================================="
