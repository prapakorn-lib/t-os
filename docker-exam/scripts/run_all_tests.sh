#!/bin/bash

# Run All Tests Script
# Concert Ticket Booking System

echo "=========================================="
echo "Concert Ticket Booking System"
echo "Complete Test Suite"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "$PROJECT_DIR/docker-compose.yml" ]; then
    echo -e "${RED}ERROR: docker-compose.yml not found${NC}"
    echo "Please run this script from the project root or scripts directory"
    exit 1
fi

cd "$PROJECT_DIR"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

# Check if services are running
echo "Checking Docker services..."
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Services are not running. Starting services...${NC}"
    docker-compose up -d

    echo "Waiting for services to be ready..."
    sleep 10

    # Check again
    if ! docker-compose ps | grep -q "Up"; then
        echo -e "${RED}ERROR: Failed to start services${NC}"
        echo "Please check docker-compose logs for details"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Services are running${NC}"
echo ""

# Wait for services to be fully ready
echo "Waiting for services to be fully ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s -f http://localhost:3000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Services are ready${NC}"
        break
    fi

    ((attempt++))
    echo -n "."
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo ""
    echo -e "${RED}ERROR: Services did not become ready in time${NC}"
    exit 1
fi

echo ""
echo ""

# Create results directory
RESULTS_DIR="$PROJECT_DIR/test_results"
mkdir -p "$RESULTS_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_FILE="$RESULTS_DIR/test_results_$TIMESTAMP.log"

echo "Test results will be saved to: $RESULTS_FILE"
echo ""

# Run Performance Tests
echo -e "${BLUE}=========================================="
echo "Running Performance Tests..."
echo "==========================================${NC}"
echo ""

if [ -f "$SCRIPT_DIR/test_performance.sh" ]; then
    bash "$SCRIPT_DIR/test_performance.sh" | tee -a "$RESULTS_FILE"
    performance_exit_code=${PIPESTATUS[0]}
else
    echo -e "${RED}ERROR: test_performance.sh not found${NC}"
    performance_exit_code=1
fi

echo ""
echo ""

# Run Availability Tests
echo -e "${BLUE}=========================================="
echo "Running Availability Tests..."
echo "==========================================${NC}"
echo ""

if [ -f "$SCRIPT_DIR/test_availability.sh" ]; then
    bash "$SCRIPT_DIR/test_availability.sh" | tee -a "$RESULTS_FILE"
    availability_exit_code=${PIPESTATUS[0]}
else
    echo -e "${RED}ERROR: test_availability.sh not found${NC}"
    availability_exit_code=1
fi

echo ""
echo ""

# Run Reliability Tests
echo -e "${BLUE}=========================================="
echo "Running Reliability Tests..."
echo "==========================================${NC}"
echo ""

if [ -f "$SCRIPT_DIR/test_reliability.sh" ]; then
    bash "$SCRIPT_DIR/test_reliability.sh" | tee -a "$RESULTS_FILE"
    reliability_exit_code=${PIPESTATUS[0]}
else
    echo -e "${RED}ERROR: test_reliability.sh not found${NC}"
    reliability_exit_code=1
fi

echo ""
echo ""

# Final Summary
echo "==========================================" | tee -a "$RESULTS_FILE"
echo "FINAL TEST SUMMARY" | tee -a "$RESULTS_FILE"
echo "==========================================" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

echo "Test Execution Status:" | tee -a "$RESULTS_FILE"

if [ $performance_exit_code -eq 0 ]; then
    echo -e "  Performance Tests:  ${GREEN}COMPLETED${NC}" | tee -a "$RESULTS_FILE"
else
    echo -e "  Performance Tests:  ${RED}FAILED${NC}" | tee -a "$RESULTS_FILE"
fi

if [ $availability_exit_code -eq 0 ]; then
    echo -e "  Availability Tests: ${GREEN}COMPLETED${NC}" | tee -a "$RESULTS_FILE"
else
    echo -e "  Availability Tests: ${RED}FAILED${NC}" | tee -a "$RESULTS_FILE"
fi

if [ $reliability_exit_code -eq 0 ]; then
    echo -e "  Reliability Tests:  ${GREEN}COMPLETED${NC}" | tee -a "$RESULTS_FILE"
else
    echo -e "  Reliability Tests:  ${RED}FAILED${NC}" | tee -a "$RESULTS_FILE"
fi

echo "" | tee -a "$RESULTS_FILE"
echo "Test Results Location: $RESULTS_FILE" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Overall result
if [ $performance_exit_code -eq 0 ] && [ $availability_exit_code -eq 0 ] && [ $reliability_exit_code -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS COMPLETED SUCCESSFULLY${NC}" | tee -a "$RESULTS_FILE"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED - REVIEW RESULTS ABOVE${NC}" | tee -a "$RESULTS_FILE"
    exit 1
fi

echo ""
echo "==========================================" | tee -a "$RESULTS_FILE"
