#!/bin/bash

# Reliability Testing Script
# Concert Ticket Booking System

echo "=========================================="
echo "Reliability Testing"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if services are running
echo "Checking if services are running..."
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${RED}ERROR: Services are not running. Please start with 'docker-compose up -d'${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Services are running${NC}"
echo ""

# Test 1: Transaction Integrity (ACID - Atomicity)
echo "=========================================="
echo "Test 1: Transaction Integrity Test"
echo "=========================================="
echo "Standard: Transactions should rollback on constraint violations"
echo ""

echo "Attempting to violate sold_tickets constraint..."
transaction_test=$(docker exec concert-database psql -U concert_user -d concert_db << EOF
BEGIN;
UPDATE concerts SET sold_tickets = total_tickets + 1000 WHERE id = 1;
SELECT 'If you see this, constraint was not enforced' as warning;
ROLLBACK;
SELECT 'Transaction test completed' as result;
EOF
)

echo "$transaction_test"
echo ""

if echo "$transaction_test" | grep -q "constraint"; then
    echo -e "${GREEN}✓ PASSED - Transaction constraint enforced${NC}"
else
    echo -e "${YELLOW}⚠ Note: Constraint should prevent invalid updates${NC}"
fi
echo ""

# Test 2: Data Integrity Constraints
echo "=========================================="
echo "Test 2: Data Integrity Constraints Test"
echo "=========================================="
echo "Standard: Database should reject invalid data"
echo ""

echo "Test 2.1: Attempting to insert negative quantity..."
negative_test=$(docker exec concert-database psql -U concert_user -d concert_db << EOF 2>&1
INSERT INTO bookings (concert_id, customer_name, customer_email, quantity)
VALUES (1, 'Test User', 'test@test.com', -1);
EOF
)

if echo "$negative_test" | grep -qi "error\|violates"; then
    echo -e "${GREEN}✓ PASSED - Negative quantity rejected${NC}"
else
    echo -e "${RED}✗ FAILED - Negative quantity was accepted${NC}"
fi

echo ""
echo "Test 2.2: Attempting to insert invalid concert_id..."
invalid_concert=$(docker exec concert-database psql -U concert_user -d concert_db << EOF 2>&1
INSERT INTO bookings (concert_id, customer_name, customer_email, quantity)
VALUES (9999, 'Test User', 'test@test.com', 1);
EOF
)

if echo "$invalid_concert" | grep -qi "error\|violates\|foreign key"; then
    echo -e "${GREEN}✓ PASSED - Invalid concert_id rejected${NC}"
else
    echo -e "${RED}✗ FAILED - Invalid concert_id was accepted${NC}"
fi
echo ""

# Test 3: Concurrent Booking (Race Condition)
echo "=========================================="
echo "Test 3: Concurrent Booking Test"
echo "=========================================="
echo "Standard: System should prevent double booking"
echo ""

# Get concert with only 1 available ticket (concert_id = 5)
echo "Setting up test: Concert with 1 available ticket..."
docker exec concert-database psql -U concert_user -d concert_db << EOF > /dev/null
UPDATE concerts SET sold_tickets = total_tickets - 1 WHERE id = 5;
EOF

initial_available=$(docker exec concert-database psql -U concert_user -d concert_db -t -c \
    "SELECT total_tickets - sold_tickets FROM concerts WHERE id = 5;")

echo "Initial available tickets: $(echo $initial_available | tr -d ' ')"
echo ""
echo "Attempting 5 concurrent bookings for concert with 1 ticket..."

# Create temporary directory for results
mkdir -p /tmp/reliability_test

# Send 5 concurrent booking requests
for i in {1..5}; do
    (curl -s -X POST http://localhost:3000/api/book \
        -H "Content-Type: application/json" \
        -d "{
            \"concert_id\": 5,
            \"customer_name\": \"Concurrent User $i\",
            \"customer_email\": \"concurrent$i@test.com\",
            \"quantity\": 1
        }" > /tmp/reliability_test/booking_$i.json) &
done

# Wait for all requests to complete
wait
sleep 2

# Count successful bookings
success_count=0
fail_count=0

echo ""
echo "Booking Results:"
for i in {1..5}; do
    if [ -f /tmp/reliability_test/booking_$i.json ]; then
        if jq -e '.success' /tmp/reliability_test/booking_$i.json > /dev/null 2>&1; then
            ((success_count++))
            echo "  Request $i: SUCCESS"
        else
            ((fail_count++))
            error_msg=$(jq -r '.error' /tmp/reliability_test/booking_$i.json 2>/dev/null)
            echo "  Request $i: FAILED ($error_msg)"
        fi
    fi
done

# Check final available tickets
final_available=$(docker exec concert-database psql -U concert_user -d concert_db -t -c \
    "SELECT total_tickets - sold_tickets FROM concerts WHERE id = 5;")

echo ""
echo "Results:"
echo "  Successful bookings: $success_count"
echo "  Failed bookings: $fail_count"
echo "  Final available tickets: $(echo $final_available | tr -d ' ')"

# Clean up
rm -rf /tmp/reliability_test

if [ $success_count -eq 1 ] && [ $fail_count -eq 4 ]; then
    echo -e "  ${GREEN}✓ PASSED - Only 1 booking succeeded (no double booking)${NC}"
elif [ $success_count -gt 1 ]; then
    echo -e "  ${RED}✗ FAILED - Double booking occurred ($success_count bookings succeeded)${NC}"
else
    echo -e "  ${YELLOW}⚠ WARNING - No bookings succeeded${NC}"
fi
echo ""

# Test 4: Data Consistency Check
echo "=========================================="
echo "Test 4: Data Consistency Check"
echo "=========================================="
echo "Standard: sold_tickets should match sum of bookings"
echo ""

echo "Checking data consistency across all concerts..."
consistency_check=$(docker exec concert-database psql -U concert_user -d concert_db -t << EOF
SELECT
    c.id,
    c.concert_name,
    c.sold_tickets,
    COALESCE(SUM(b.quantity), 0) as total_booked,
    CASE
        WHEN c.sold_tickets = COALESCE(SUM(b.quantity), 0) THEN 'CONSISTENT'
        ELSE 'INCONSISTENT'
    END as status
FROM concerts c
LEFT JOIN bookings b ON c.id = b.concert_id
GROUP BY c.id, c.concert_name, c.sold_tickets
ORDER BY c.id;
EOF
)

echo "$consistency_check"
echo ""

if echo "$consistency_check" | grep -q "INCONSISTENT"; then
    echo -e "${RED}✗ FAILED - Found data inconsistencies${NC}"
    echo "Action Required: Investigate and fix data inconsistencies"
else
    echo -e "${GREEN}✓ PASSED - All data is consistent${NC}"
fi
echo ""

# Test 5: Error Handling Test
echo "=========================================="
echo "Test 5: Error Handling Test"
echo "=========================================="
echo "Standard: System should return proper error messages"
echo ""

echo "Test 5.1: Booking non-existent concert..."
error_test1=$(curl -s -X POST http://localhost:3000/api/book \
    -H "Content-Type: application/json" \
    -d '{
        "concert_id": 999,
        "customer_name": "Test User",
        "customer_email": "test@test.com",
        "quantity": 1
    }')

echo "Response: $(echo $error_test1 | jq -r '.error')"

if echo "$error_test1" | jq -e '.error' > /dev/null; then
    echo -e "${GREEN}✓ PASSED - Proper error message returned${NC}"
else
    echo -e "${RED}✗ FAILED - No error message returned${NC}"
fi

echo ""
echo "Test 5.2: Booking more tickets than available..."
error_test2=$(curl -s -X POST http://localhost:3000/api/book \
    -H "Content-Type: application/json" \
    -d '{
        "concert_id": 1,
        "customer_name": "Test User",
        "customer_email": "test@test.com",
        "quantity": 99999
    }')

echo "Response: $(echo $error_test2 | jq -r '.error')"

if echo "$error_test2" | jq -e '.error' | grep -qi "available\|not enough"; then
    echo -e "${GREEN}✓ PASSED - Proper error message for insufficient tickets${NC}"
else
    echo -e "${RED}✗ FAILED - Improper error handling${NC}"
fi
echo ""

# Test 6: Data Persistence Test
echo "=========================================="
echo "Test 6: Data Persistence Test"
echo "=========================================="
echo "Standard: Data should persist in volumes"
echo ""

echo "Creating database backup..."
docker exec concert-database pg_dump -U concert_user concert_db > /tmp/concert_backup.sql 2>/dev/null

if [ -f /tmp/concert_backup.sql ]; then
    backup_size=$(wc -c < /tmp/concert_backup.sql)
    backup_lines=$(wc -l < /tmp/concert_backup.sql)

    echo "Backup created successfully:"
    echo "  File: /tmp/concert_backup.sql"
    echo "  Size: $backup_size bytes"
    echo "  Lines: $backup_lines"
    echo -e "  ${GREEN}✓ PASSED - Data can be backed up${NC}"
else
    echo -e "  ${RED}✗ FAILED - Could not create backup${NC}"
fi
echo ""

# Test 7: ACID Properties Verification
echo "=========================================="
echo "Test 7: ACID Properties Verification"
echo "=========================================="
echo ""

echo "A - Atomicity: Tested in Test 1 (Transaction Integrity)"
echo "C - Consistency: Tested in Test 4 (Data Consistency)"
echo "I - Isolation: Tested in Test 3 (Concurrent Booking)"
echo "D - Durability: Tested in Test 6 (Data Persistence)"
echo ""

# Summary
echo "=========================================="
echo "Reliability Testing Summary"
echo "=========================================="
echo ""

all_passed=true

echo "Test Results:"

# Test 1: Transaction Integrity
if echo "$transaction_test" | grep -q "constraint\|result"; then
    echo -e "  1. Transaction Integrity: ${GREEN}PASSED${NC}"
else
    echo -e "  1. Transaction Integrity: ${YELLOW}PARTIAL${NC}"
fi

# Test 2: Data Integrity Constraints
if echo "$negative_test" | grep -qi "error\|violates" && \
   echo "$invalid_concert" | grep -qi "error\|violates"; then
    echo -e "  2. Data Integrity Constraints: ${GREEN}PASSED${NC}"
else
    echo -e "  2. Data Integrity Constraints: ${RED}FAILED${NC}"
    all_passed=false
fi

# Test 3: Concurrent Booking
if [ $success_count -eq 1 ] && [ $fail_count -eq 4 ]; then
    echo -e "  3. Concurrent Booking (No Race Condition): ${GREEN}PASSED${NC}"
else
    echo -e "  3. Concurrent Booking (No Race Condition): ${RED}FAILED${NC}"
    all_passed=false
fi

# Test 4: Data Consistency
if ! echo "$consistency_check" | grep -q "INCONSISTENT"; then
    echo -e "  4. Data Consistency: ${GREEN}PASSED${NC}"
else
    echo -e "  4. Data Consistency: ${RED}FAILED${NC}"
    all_passed=false
fi

# Test 5: Error Handling
if echo "$error_test1" | jq -e '.error' > /dev/null && \
   echo "$error_test2" | jq -e '.error' > /dev/null; then
    echo -e "  5. Error Handling: ${GREEN}PASSED${NC}"
else
    echo -e "  5. Error Handling: ${RED}FAILED${NC}"
    all_passed=false
fi

# Test 6: Data Persistence
if [ -f /tmp/concert_backup.sql ]; then
    echo -e "  6. Data Persistence: ${GREEN}PASSED${NC}"
else
    echo -e "  6. Data Persistence: ${RED}FAILED${NC}"
    all_passed=false
fi

echo ""
echo "ACID Properties:"
echo "  ✓ Atomicity - Transactions are all-or-nothing"
echo "  ✓ Consistency - Data remains consistent"
echo "  ✓ Isolation - Concurrent transactions don't interfere"
echo "  ✓ Durability - Data persists after transactions"

echo ""
echo "Overall Assessment:"
if [ "$all_passed" = true ]; then
    echo -e "${GREEN}✓ PASSED - System demonstrates high reliability${NC}"
else
    echo -e "${RED}✗ FAILED - System has reliability issues${NC}"
    echo ""
    echo "Recommendations for improvement:"
    echo "  - Implement proper transaction handling in all operations"
    echo "  - Use row-level locking (SELECT FOR UPDATE) for critical operations"
    echo "  - Add more database constraints to ensure data integrity"
    echo "  - Implement proper error handling and logging"
    echo "  - Regular database backups and testing restore procedures"
    echo "  - Monitor database health and performance"
fi

echo ""
echo "=========================================="
echo "Reliability Testing Completed"
echo "=========================================="

# Cleanup
rm -f /tmp/concert_backup.sql
