const express = require('express');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const PORT = 3000;

// Database configuration
const pool = new Pool({
  host: process.env.DB_HOST || 'database',
  user: process.env.DB_USER || 'concert_user',
  password: process.env.DB_PASSWORD || 'concert_pass',
  database: process.env.DB_NAME || 'concert_db',
  port: process.env.DB_PORT || 5432,
});

app.use(express.json());
app.use(express.static('public'));

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
  } catch (error) {
    res.status(500).json({ status: 'unhealthy', error: error.message });
  }
});

// Get all concerts
app.get('/api/concerts', async (req, res) => {
  const startTime = Date.now();
  try {
    const result = await pool.query(`
      SELECT c.*,
             (c.total_tickets - c.sold_tickets) as available_tickets
      FROM concerts c
      ORDER BY c.concert_date
    `);
    const responseTime = Date.now() - startTime;
    res.json({
      data: result.rows,
      count: result.rows.length,
      responseTime: `${responseTime}ms`
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get concert by ID
app.get('/api/concerts/:id', async (req, res) => {
  const startTime = Date.now();
  try {
    const { id } = req.params;
    const result = await pool.query(`
      SELECT c.*,
             (c.total_tickets - c.sold_tickets) as available_tickets
      FROM concerts c
      WHERE c.id = $1
    `, [id]);

    const responseTime = Date.now() - startTime;

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Concert not found' });
    }

    res.json({
      data: result.rows[0],
      responseTime: `${responseTime}ms`
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Book tickets
app.post('/api/book', async (req, res) => {
  const startTime = Date.now();
  const client = await pool.connect();

  try {
    const { concert_id, customer_name, customer_email, quantity } = req.body;

    await client.query('BEGIN');

    // Check available tickets
    const concertResult = await client.query(
      'SELECT * FROM concerts WHERE id = $1 FOR UPDATE',
      [concert_id]
    );

    if (concertResult.rows.length === 0) {
      throw new Error('Concert not found');
    }

    const concert = concertResult.rows[0];
    const available = concert.total_tickets - concert.sold_tickets;

    if (available < quantity) {
      throw new Error(`Only ${available} tickets available`);
    }

    // Update sold tickets
    await client.query(
      'UPDATE concerts SET sold_tickets = sold_tickets + $1 WHERE id = $2',
      [quantity, concert_id]
    );

    // Create booking
    const bookingResult = await client.query(
      `INSERT INTO bookings (concert_id, customer_name, customer_email, quantity, booking_date)
       VALUES ($1, $2, $3, $4, NOW())
       RETURNING *`,
      [concert_id, customer_name, customer_email, quantity]
    );

    await client.query('COMMIT');

    const responseTime = Date.now() - startTime;

    res.json({
      success: true,
      booking: bookingResult.rows[0],
      responseTime: `${responseTime}ms`
    });
  } catch (error) {
    await client.query('ROLLBACK');
    res.status(400).json({ error: error.message });
  } finally {
    client.release();
  }
});

// Get all bookings
app.get('/api/bookings', async (req, res) => {
  const startTime = Date.now();
  try {
    const result = await pool.query(`
      SELECT b.*, c.concert_name, c.concert_date
      FROM bookings b
      JOIN concerts c ON b.concert_id = c.id
      ORDER BY b.booking_date DESC
    `);
    const responseTime = Date.now() - startTime;
    res.json({
      data: result.rows,
      count: result.rows.length,
      responseTime: `${responseTime}ms`
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Database statistics
app.get('/api/stats', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        COUNT(DISTINCT c.id) as total_concerts,
        SUM(c.sold_tickets) as total_tickets_sold,
        COUNT(DISTINCT b.id) as total_bookings
      FROM concerts c
      LEFT JOIN bookings b ON c.id = b.concert_id
    `);
    res.json(result.rows[0]);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Access the application at http://localhost:${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM signal received: closing HTTP server');
  await pool.end();
  process.exit(0);
});
