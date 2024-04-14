import psycopg2
import json

class Member:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register(self):
        print("\nRegister New Member")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
        gender = input("Enter gender: ")
        fitness_goals = input("Enter fitness goals: ")

        # Get health metrics as a JSON string {"weight": 70, "height": 170}
        health_metrics_input = input("Enter health metrics (in JSON format): ")
        try:
            health_metrics = json.loads(health_metrics_input)
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return "Registration failed due to invalid health metrics format"

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO members (first_name, last_name, email, date_of_birth, gender, fitness_goals, health_metrics)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (first_name, last_name, email, date_of_birth, gender, fitness_goals, json.dumps(health_metrics)))
            self.db_connection.commit()
            print("Registration successful")
            return "Registration completed successfully"
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Registration failed due to a database error"  

    def update_personal_info(self):
        print("\nUpdate Personal Information")
        member_id = input("Enter your member ID: ")
        first_name = input("Enter new first name (leave blank if no change): ")
        last_name = input("Enter new last name (leave blank if no change): ")
        email = input("Enter new email (leave blank if no change): ")
        date_of_birth = input("Enter new date of birth (YYYY-MM-DD, leave blank if no change): ")
        gender = input("Enter new gender (leave blank if no change): ")

        try:
            with self.db_connection.cursor() as cursor:
                update_query = "UPDATE members SET "
                update_cols = []
                update_vals = []
                if first_name:
                    update_cols.append("first_name = %s")
                    update_vals.append(first_name)
                if last_name:
                    update_cols.append("last_name = %s")
                    update_vals.append(last_name)
                if email:
                    update_cols.append("email = %s")
                    update_vals.append(email)
                if date_of_birth:
                    update_cols.append("date_of_birth = %s")
                    update_vals.append(date_of_birth)
                if gender:
                    update_cols.append("gender = %s")
                    update_vals.append(gender)

                if not update_cols:
                    print("No updates made.")
                    return

                update_query += ', '.join(update_cols)
                update_query += " WHERE member_id = %s"
                update_vals.append(member_id)
                cursor.execute(update_query, tuple(update_vals))
                
            self.db_connection.commit()
            print("Personal information updated successfully")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def update_fitness_goals(self):
        member_id = input("\nEnter your member ID: ")
        fitness_goals = input("Enter new fitness goals (leave blank if no change): ")

        if not fitness_goals:
            print("No updates made.")
            return

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE members SET fitness_goals = %s
                    WHERE member_id = %s
                """, (fitness_goals, member_id))
            self.db_connection.commit()
            print("Fitness goals updated successfully")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def update_health_metrics(self):
        member_id = input("\nEnter your member ID: ")
        health_metrics_input = input("Enter new health metrics in JSON format (leave blank if no change): ")

        if not health_metrics_input:
            print("No updates made.")
            return

        try:
            health_metrics = json.loads(health_metrics_input)
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE members SET health_metrics = %s
                    WHERE member_id = %s
                """, (json.dumps(health_metrics), member_id))
            self.db_connection.commit()
            print("Health metrics updated successfully")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            

    def view_dashboard(self):
        first_name = input("Enter the first name of the member: ")
        last_name = input("Enter the last name of the member: ")

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM members 
                    WHERE first_name = %s AND last_name = %s
                """, (first_name, last_name))
                member_info = cursor.fetchone()

                if member_info:
                    member_id = member_info[0] 
                    print(f"\nMember Dashboard for {member_info[1]} {member_info[2]}:")
                    print(f"Member ID: {member_id}, Name: {member_info[1]} {member_info[2]}, Email: {member_info[3]}, "
                        f"DOB: {member_info[4]}, Gender: {member_info[5]}, Fitness Goals: {member_info[6]}, "
                        f"Health Metrics: {member_info[7]}")

                    cursor.execute("""
                        SELECT s.session_id, s.session_day, s.session_time, t.first_name, t.last_name
                        FROM training_sessions s
                        JOIN trainers t ON s.trainer_id = t.trainer_id
                        WHERE s.member_id = %s AND s.status = 'Scheduled'
                    """, (member_id,))
                    training_sessions = cursor.fetchall()
                    if training_sessions:
                        print("Scheduled Training Sessions:")
                        for session in training_sessions:
                            print(f"Session ID: {session[0]}, Trainer: {session[3]} {session[4]}, Day: {session[1]}, Time: {session[2]}")
                    else:
                        print("No scheduled training sessions.")

                    cursor.execute("""
                        SELECT c.class_name, b.booking_time, b.booking_status
                        FROM bookings b
                        JOIN classes c ON b.class_id = c.class_id
                        WHERE b.member_id = %s AND b.booking_status = 'Confirmed'
                    """, (member_id,))
                    class_bookings = cursor.fetchall()
                    if class_bookings:
                        print("Class Bookings:")
                        for booking in class_bookings:
                            print(f"Class: {booking[0]}, Time: {booking[1]}, Status: {booking[2]}")
                    else:
                        print("No class bookings.")
                else:
                    print("No member found with that name.")

        except psycopg2.Error as e:
            self.db_connection.rollback()
            print(f"Database error: {e}")

    def schedule_training_session(self):
        print("\nSchedule a Training or Fitness Class")
        member_id = input("Enter your member ID: ")
        session_type = input("Type 'P' for Personal Training or 'G' for Group Fitness Class: ").upper()

        if session_type == 'P':
            print("Available Personal Trainers:")
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT trainer_id, first_name, last_name, availability
                        FROM trainers
                    """)
                    trainers = cursor.fetchall()
                    for trainer in trainers:
                        print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]} {trainer[2]}, Availability: {trainer[3]}")
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                return

            trainer_id = input("Enter trainer ID: ")
            session_day = input("Enter day of the week (e.g., Monday, Tuesday): ")
            session_time = input("Enter session time (HH:MM): ")

            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT availability FROM trainers WHERE trainer_id = %s
                    """, (trainer_id,))
                    availability = cursor.fetchone()[0]
                    # Check if day and time are available within the stored availability
                    if session_day in availability and session_time in str(availability[session_day]):
                        cursor.execute("""
                            INSERT INTO training_sessions (member_id, trainer_id, session_day, session_time, status)
                            VALUES (%s, %s, %s, %s, 'Scheduled')
                        """, (member_id, trainer_id, session_day, session_time))
                        self.db_connection.commit()
                        print("Personal training session scheduled successfully")
                    else:
                        print("Trainer is not available at this time.")
            except psycopg2.Error as e:
                print(f"Database error: {e}")

        elif session_type == 'G':
            print("Available Group Fitness Classes:")
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT class_id, class_name, schedule FROM classes
                    """)
                    classes = cursor.fetchall()
                    for cls in classes:
                        print(f"Class ID: {cls[0]}, Name: {cls[1]}, Schedule: {cls[2]}")
            except psycopg2.Error as e:
                print(f"Database error: {e}")
                return

            class_id = input("Enter class ID to register: ")
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO bookings (member_id, class_id, booking_time, booking_status, booking_type)
                        VALUES (%s, %s, NOW(), 'Confirmed', 'Group Class')
                    """, (member_id, class_id))
                self.db_connection.commit()
                print("Registered for group fitness class successfully")
            except psycopg2.Error as e:
                print(f"Database error: {e}")

        else:
            print("Invalid selection, please choose 'P' for Personal or 'G' for Group.")

    def cancel_training_session(self):
        session_id = input("Enter the session ID to cancel: ")

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("DELETE FROM training_sessions WHERE session_id = %s", (session_id,))
            self.db_connection.commit()
            print("Training session cancelled successfully")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            
        
    def reschedule_training_session(self):
        member_id = input("Enter your member ID: ")

        # Display all scheduled sessions for the member
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT session_id, trainer_id, session_day, session_time
                    FROM training_sessions
                    WHERE member_id = %s AND status = 'Scheduled'
                """, (member_id,))
                sessions = cursor.fetchall()
                if not sessions:
                    print("No scheduled sessions found.")
                    return
                print("Scheduled Sessions:")
                for session in sessions:
                    print(f"Session ID: {session[0]}, Trainer ID: {session[1]}, Day: {session[2]}, Time: {session[3]}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return

        session_id = input("Enter the session ID to reschedule: ")
        # Fetch trainer details based on selected session
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT trainer_id FROM training_sessions WHERE session_id = %s
                """, (session_id,))
                result = cursor.fetchone()
                if not result:
                    print("No such session found.")
                    return
                trainer_id = result[0]
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return

        # Show availability of the trainer
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT availability FROM trainers WHERE trainer_id = %s
                """, (trainer_id,))
                availability = cursor.fetchone()[0]
                print(f"Trainer {trainer_id} Availability: {availability}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return

        session_day = input("Enter the new day of the week (e.g., Monday, Tuesday): ")
        session_time = input("Enter the new time (HH:MM): ")

        # Update the session with new day and time
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE training_sessions
                    SET session_day = %s, session_time = %s
                    WHERE session_id = %s
                """, (session_day, session_time, session_id))
            self.db_connection.commit()
            print("Training session rescheduled successfully")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
