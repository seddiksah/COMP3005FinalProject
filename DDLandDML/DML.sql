INSERT INTO members (first_name, last_name, email, date_of_birth, gender, fitness_goals, health_metrics)
VALUES ('Tyler', 'Attardo', 'tyler123@gmail.com', '1990-01-01', 'Male', 'Lose weight', '{"height": 180, "weight": 80}');


INSERT INTO trainers (first_name, last_name, email, password, availability)
VALUES ('Stephanie', 'Smith', 'stephanie.smith@example.com', 'stephanie123', '{"Tuesday": ["09:00-12:00", "14:00-17:00"], "Wednesday": ["10:00-13:00"]}');


INSERT INTO admin_staff (first_name, last_name, email)
VALUES ('Brandon', 'Washington', 'brandon.w@yahoo.com');

INSERT INTO rooms (room_name, capacity)
VALUES ('Example Room', 100);

INSERT INTO rooms (room_name, capacity)
VALUES ('Spin Room', 15);

INSERT INTO rooms (room_name, capacity)
VALUES ('Yoga Room', 20);


INSERT INTO equipment (name, maintenance_schedule)
VALUES ('Treadmill', '2023-12-22');


INSERT INTO classes (class_name, class_description, schedule)
VALUES ('Spin Class', 'A refreshing morning spin session to start your day.', TIMESTAMP '2023-08-01 08:00:00');

INSERT INTO classes (class_name, class_description, schedule)
VALUES ('Yoga Class', 'Beginners Yoga Class.', TIMESTAMP '2023-03-20 10:30:00');


INSERT INTO membership_fees (member_id, amount, due_date, status)
VALUES (1, 50.00, '2023-08-03', 'Due');


INSERT INTO training_sessions (member_id, trainer_id, session_day, session_time, status)
VALUES (1, 1, 'Monday', '09:00', 'Scheduled');


INSERT INTO bookings (member_id, trainer_id, room_id, booking_time, booking_status, booking_type, class_id)
VALUES (1, 1, 1, TIMESTAMP '2023-08-01 08:00:00', 'Confirmed', 'Group Class', 1);

