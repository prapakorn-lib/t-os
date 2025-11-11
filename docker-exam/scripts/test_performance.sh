#!/bin/bash

# Performance Testing Script
# Concert Ticket Booking System

echo "=========================================="
echo "Performance Testing"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if services are running
echo "1. Checking if services are running..."
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${RED}ERROR: Services are not running. Please start with 'docker-compose up -d'${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Services are running${NC}"
echo ""

# Test 1: API Response Time
echo "=========================================="
echo "Test 1: API Response Time"
echo "=========================================="
echo "Standard: Response time should be ≤ 200ms"
echo ""

total_time=0
success_count=0
fail_count=0

for i in {1..10}; do
    echo -n "Request $i: "

    # Measure response time
    response=$(curl -w "\n%{time_total}" -s http://localhost:3000/api/concerts)
    time_total=$(echo "$response" | tail -1)

    # Convert to milliseconds
    time_ms=$(echo "$time_total * 1000" | bc)
    time_ms_int=$(printf "%.0f" $time_ms)

    echo -n "${time_ms_int}ms "

    # Check if request was successful
    if echo "$response" | head -n -1 | jq -e '.data' > /dev/null 2>&1; then
        ((success_count++))
        echo -e "${GREEN}✓${NC}"
    else
        ((fail_count++))
        echo -e "${RED}✗${NC}"
    fi

    total_time=$(echo "$total_time + $time_ms" | bc)
    sleep 0.5
done

# Calculate average
avg_time=$(echo "scale=2; $total_time / 10" | bc)
avg_time_int=$(printf "%.0f" $avg_time)

echo ""
echo "Results:"
echo "  Success: $success_count/10"
echo "  Failed: $fail_count/10"
echo "  Average Response Time: ${avg_time_int}ms"

# Check against standard
if (( $(echo "$avg_time_int <= 200" | bc -l) )); then
    echo -e "  Status: ${GREEN}PASSED ✓${NC} (≤ 200ms)"
else
    echo -e "  Status: ${RED}FAILED ✗${NC} (> 200ms)"
fi
echo ""

# Test 2: Health Check Response Time
echo "=========================================="
echo "Test 2: Health Check Response Time"
echo "=========================================="
echo "Standard: Response time should be ≤ 100ms"
echo ""

health_response=$(curl -w "\n%{time_total}" -s http://localhost:3000/health)
health_time=$(echo "$health_response" | tail -1)
health_time_ms=$(echo "$health_time * 1000" | bc)
health_time_ms_int=$(printf "%.0f" $health_time_ms)

echo "Health Check Response Time: ${health_time_ms_int}ms"

if (( $(echo "$health_time_ms_int <= 100" | bc -l) )); then
    echo -e "Status: ${GREEN}PASSED ✓${NC} (≤ 100ms)"
else
    echo -e "Status: ${RED}FAILED ✗${NC} (> 100ms)"
fi
echo ""

# Test 3: Concurrent Requests Test
echo "=========================================="
echo "Test 3: Concurrent Requests (10 parallel)"
echo "=========================================="
echo "Standard: Success rate ≥ 95%"
echo ""

echo "Sending 10 concurrent requests..."
start_time=$(date +%s.%N)

# Send 10 requests in parallel
for i in {1..10}; do
    curl -s -o /tmp/perf_test_$i.json http://localhost:3000/api/concerts &
done

# Wait for all to complete
wait

end_time=$(date +%s.%N)
total_concurrent_time=$(echo "$end_time - $start_time" | bc)

# Check results
concurrent_success=0
concurrent_fail=0

for i in {1..10}; do
    if [ -f /tmp/perf_test_$i.json ] && jq -e '.data' /tmp/perf_test_$i.json > /dev/null 2>&1; then
        ((concurrent_success++))
    else
        ((concurrent_fail++))
    fi
    rm -f /tmp/perf_test_$i.json
done

success_rate=$(echo "scale=2; $concurrent_success * 100 / 10" | bc)

echo "Results:"
echo "  Total Requests: 10"
echo "  Successful: $concurrent_success"
echo "  Failed: $concurrent_fail"
echo "  Success Rate: ${success_rate}%"
echo "  Total Time: $(printf "%.3f" $total_concurrent_time)s"

if (( $(echo "$success_rate >= 95" | bc -l) )); then
    echo -e "  Status: ${GREEN}PASSED ✓${NC} (≥ 95%)"
else
    echo -e "  Status: ${RED}FAILED ✗${NC} (< 95%)"
fi
echo ""

# Test 4: Database Query Performance
echo "=========================================="
echo "Test 4: Database Query Performance"
echo "=========================================="
echo "Standard: Query time should be ≤ 100ms"
echo ""

echo "Running database query..."
db_output=$(docker exec concert-database psql -U concert_user -d concert_db -c "\timing on" -c "SELECT * FROM concerts;" 2>&1)

# Extract timing information
db_time=$(echo "$db_output" | grep "Time:" | awk '{print $2}')

if [ -z "$db_time" ]; then
    echo -e "${RED}Could not measure database query time${NC}"
else
    echo "Database Query Time: ${db_time}"

    # Remove 'ms' and compare
    db_time_value=$(echo "$db_time" | sed 's/ms//')

    if (( $(echo "$db_time_value <= 100" | bc -l) )); then
        echo -e "Status: ${GREEN}PASSED ✓${NC} (≤ 100ms)"
    else
        echo -e "Status: ${RED}FAILED ✗${NC} (> 100ms)"
    fi
fi
echo ""

# Test 5: Load Test with Apache Bench (if available)
echo "=========================================="
echo "Test 5: Load Test (Apache Bench)"
echo "=========================================="

if command -v ab &> /dev/null; then
    echo "Running load test: 100 requests, 10 concurrent..."
    echo ""

    ab -n 100 -c 10 -q http://localhost:3000/api/concerts | grep -E "(Requests per second|Time per request|Failed requests)"

    echo ""
else
    echo -e "${YELLOW}Apache Bench (ab) not installed. Skipping load test.${NC}"
    echo "Install with: sudo apt-get install apache2-utils"
    echo ""
fi

# Summary
echo "=========================================="
echo "Performance Testing Summary"
echo "=========================================="
echo ""
echo "Test Results:"
echo "  1. API Response Time: Average ${avg_time_int}ms"
echo "  2. Health Check Time: ${health_time_ms_int}ms"
echo "  3. Concurrent Requests: ${success_rate}% success rate"
echo "  4. Database Query: ${db_time:-N/A}"
echo ""

# Overall assessment
echo "Overall Assessment:"
if (( $(echo "$avg_time_int <= 200" | bc -l) )) && \
   (( $(echo "$health_time_ms_int <= 100" | bc -l) )) && \
   (( $(echo "$success_rate >= 95" | bc -l) )); then
    echo -e "${GREEN}✓ PASSED - System meets performance standards${NC}"
else
    echo -e "${RED}✗ FAILED - System does not meet all performance standards${NC}"
    echo ""
    echo "Recommendations for improvement:"
    if (( $(echo "$avg_time_int > 200" | bc -l) )); then
        echo "  - Optimize API response time (add caching, optimize queries)"
    fi
    if (( $(echo "$health_time_ms_int > 100" | bc -l) )); then
        echo "  - Optimize health check endpoint"
    fi
    if (( $(echo "$success_rate < 95" | bc -l) )); then
        echo "  - Improve system stability for concurrent requests"
        echo "  - Add connection pooling"
        echo "  - Optimize database connections"
    fi
fi

echo ""
echo "=========================================="
echo "Performance Testing Completed"
echo "=========================================="
