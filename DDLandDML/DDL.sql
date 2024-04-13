CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(50) NOT NULL,
    fitness_goals TEXT,
    health_metrics JSONB
);

CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, 
    availability JSONB
);

CREATE TABLE admin_staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    capacity INT
);

CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    maintenance_schedule DATE
);

CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    class_description TEXT,
    schedule TIMESTAMPTZ NOT NULL
);

CREATE TABLE membership_fees (
    fee_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    amount DECIMAL(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE training_sessions (
    session_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    trainer_id INT REFERENCES trainers(trainer_id),
    session_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE trainer_availability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES trainers(trainer_id) ON DELETE CASCADE,
    day_of_week VARCHAR(50) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE,
    trainer_id INT REFERENCES trainers(trainer_id),
    room_id INT REFERENCES rooms(room_id),
    booking_time TIMESTAMPTZ NOT NULL,
    booking_status VARCHAR(50) NOT NULL,
    booking_type VARCHAR(255) NOT NULL
);

ALTER TABLE bookings
ADD COLUMN class_id INT REFERENCES classes(class_id);


ALTER TABLE training_sessions
DROP COLUMN session_date;

ALTER TABLE training_sessions
ADD COLUMN session_day VARCHAR(10),
ADD COLUMN session_time TIME;