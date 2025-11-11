-- Concert Ticket Booking System Database
-- 2-Tier Architecture

-- Create concerts table
CREATE TABLE IF NOT EXISTS concerts (
    id SERIAL PRIMARY KEY,
    concert_name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    concert_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    total_tickets INTEGER NOT NULL,
    sold_tickets INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_tickets CHECK (sold_tickets >= 0 AND sold_tickets <= total_tickets)
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    concert_id INTEGER NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (concert_id) REFERENCES concerts(id) ON DELETE CASCADE,
    CONSTRAINT check_quantity CHECK (quantity > 0)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_concerts_date ON concerts(concert_date);
CREATE INDEX IF NOT EXISTS idx_bookings_concert ON bookings(concert_id);
CREATE INDEX IF NOT EXISTS idx_bookings_email ON bookings(customer_email);
CREATE INDEX IF NOT EXISTS idx_bookings_date ON bookings(booking_date);

-- Insert sample concert data
INSERT INTO concerts (concert_name, artist, concert_date, location, price, total_tickets, sold_tickets) VALUES
('Rock Festival 2024', 'The Rockers', '2024-12-15', 'Impact Arena, Bangkok', 2500.00, 5000, 1250),
('Jazz Night', 'Jazz Masters', '2024-11-20', 'Central World, Bangkok', 1500.00, 1000, 450),
('Pop Concert Extravaganza', 'Pop Stars United', '2024-12-01', 'Rajamangala Stadium, Bangkok', 3000.00, 10000, 7500),
('Classical Symphony', 'Bangkok Symphony Orchestra', '2024-11-25', 'Thailand Cultural Centre', 1200.00, 800, 200),
('Electronic Music Festival', 'DJ Masters', '2024-12-10', 'Bitec Bangna', 2000.00, 3000, 2999),
('Country Music Night', 'Country Legends', '2024-11-30', 'Thunder Dome, Bangkok', 1800.00, 2000, 0);

-- Insert sample booking data
INSERT INTO bookings (concert_id, customer_name, customer_email, quantity, booking_date) VALUES
(1, 'สมชาย ใจดี', 'somchai@email.com', 2, NOW() - INTERVAL '5 days'),
(1, 'สมหญิง รักดี', 'somying@email.com', 4, NOW() - INTERVAL '4 days'),
(2, 'ประยุทธ์ มานะ', 'prayut@email.com', 3, NOW() - INTERVAL '3 days'),
(3, 'วิไล สวยงาม', 'wilai@email.com', 5, NOW() - INTERVAL '2 days'),
(4, 'สุรชัย คงทน', 'surachai@email.com', 2, NOW() - INTERVAL '1 day'),
(1, 'นภา ใจงาม', 'napa@email.com', 1, NOW());

-- Create a view for concert statistics
CREATE OR REPLACE VIEW concert_statistics AS
SELECT
    c.id,
    c.concert_name,
    c.artist,
    c.concert_date,
    c.total_tickets,
    c.sold_tickets,
    (c.total_tickets - c.sold_tickets) AS available_tickets,
    ROUND((c.sold_tickets::DECIMAL / c.total_tickets::DECIMAL) * 100, 2) AS sold_percentage,
    COUNT(DISTINCT b.id) AS total_bookings,
    COALESCE(SUM(b.quantity), 0) AS total_tickets_booked
FROM concerts c
LEFT JOIN bookings b ON c.id = b.concert_id
GROUP BY c.id, c.concert_name, c.artist, c.concert_date, c.total_tickets, c.sold_tickets;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO concert_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO concert_user;

-- Display initialization message
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
    RAISE NOTICE 'Total concerts: %', (SELECT COUNT(*) FROM concerts);
    RAISE NOTICE 'Total bookings: %', (SELECT COUNT(*) FROM bookings);
END $$;
