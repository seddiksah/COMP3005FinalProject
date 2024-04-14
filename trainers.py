import psycopg2
import json

class Trainer:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_trainer(self):
        print("\nRegister New Trainer")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")
        password = input("Enter password: ")  

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO trainers (first_name, last_name, email, password)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, email, password))
            self.db_connection.commit()
            print("Trainer registration successful")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Trainer registration failed due to a database error"
        
        
    def set_availability(self):
        print("\nSet Trainer Availability")
        trainer_id = input("Enter your trainer ID: ")
        # Example JSON format: {"Monday": ["10:00", "11:00"], "Tuesday": ["12:00", "13:00"]}
        availability = input("Enter your availability in JSON format (days and times available): ")
        try:
            availability_json = json.loads(availability)
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return "Setting availability failed due to invalid JSON format."

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE trainers SET availability = %s WHERE trainer_id = %s
                """, (json.dumps(availability_json), trainer_id))
            self.db_connection.commit()
            print("Availability updated successfully.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Failed to update availability due to a database error."

    def view_member_profile(self):
        print("\nView Member Profile")
        member_name = input("Enter the name of the member to search: ")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT member_id, first_name, last_name, email, date_of_birth, gender, fitness_goals 
                    FROM members 
                    WHERE first_name ILIKE %s OR last_name ILIKE %sstaff.py:
                """, ('%' + member_name + '%', '%' + member_name + '%'))
                profiles = cursor.fetchall()
                if profiles:
                    print("Member Profiles Found:")
                    for profile in profiles:
                        print(profile)
                else:
                    print("No member profiles found with that name.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Failed to fetch member profiles due to a database error."