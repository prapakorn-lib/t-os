#!/bin/bash
# System and API Monitoring Script
# Usage: ./monitor.sh

echo "=================================="
echo "FastAPI Monitoring Dashboard"
echo "=================================="
echo "Time: $(date)"
echo ""

# Check if FastAPI is running
echo "--- Service Status ---"
if pgrep -f "uvicorn app.main:app" > /dev/null; then
    echo "✓ FastAPI: Running (PID: $(pgrep -f 'uvicorn app.main:app'))"
else
    echo "✗ FastAPI: Not running"
fi

if systemctl is-active --quiet postgresql; then
    echo "✓ PostgreSQL: Running"
else
    echo "✗ PostgreSQL: Not running"
fi
echo ""

# System Resources
echo "--- System Resources ---"
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "  Usage: " 100 - $1 "%"}'

echo "Memory Usage:"
free -h | awk 'NR==2{printf "  Total: %s | Used: %s | Free: %s | Usage: %.2f%%\n", $2,$3,$4,$3*100/$2 }'

echo "Disk Usage:"
df -h / | awk 'NR==2{printf "  Total: %s | Used: %s | Available: %s | Usage: %s\n", $2,$3,$4,$5}'
echo ""

# Network
echo "--- Network ---"
echo "Active connections on port 8000:"
ss -tuln | grep :8000 || echo "  No connections"
echo ""

# PostgreSQL Stats
echo "--- Database ---"
if command -v psql &> /dev/null; then
    DB_SIZE=$(psql -U apiuser -d apidb -tAc "SELECT pg_size_pretty(pg_database_size('apidb'));" 2>/dev/null)
    CONN_COUNT=$(psql -U apiuser -d apidb -tAc "SELECT count(*) FROM pg_stat_activity WHERE datname='apidb';" 2>/dev/null)
    
    if [ ! -z "$DB_SIZE" ]; then
        echo "Database size: $DB_SIZE"
        echo "Active connections: $CONN_COUNT"
    else
        echo "Cannot connect to database"
    fi
else
    echo "psql not available"
fi
echo ""

# API Health Check
echo "--- API Health Check ---"
if command -v curl &> /dev/null; then
    HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
    if [ ! -z "$HEALTH" ]; then
        echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
    else
        echo "API not responding"
    fi
else
    echo "curl not available"
fi
echo ""

# Recent logs (if using systemd)
echo "--- Recent Logs (last 10 lines) ---"
if systemctl list-unit-files | grep -q fastapi.service; then
    sudo journalctl -u fastapi -n 10 --no-pager
else
    if [ -f "app.log" ]; then
        tail -n 10 app.log
    else
        echo "No logs found"
    fi
fi
echo ""

echo "=================================="
echo "Monitoring completed"
echo "=================================="
