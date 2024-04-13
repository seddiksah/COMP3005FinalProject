import psycopg2
import json

class Staff:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_admin(self):
        print("\nRegister New Admin Staff")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email: ")

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO admin_staff (first_name, last_name, email)
                    VALUES (%s, %s, %s)
                """, (first_name, last_name, email))
            self.db_connection.commit()
            print("Admin registration successful")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return "Admin registration failed due to a database error"

    def view_rooms(self):
        print("\nAvailable Rooms:")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT room_id, room_name, capacity FROM rooms")
                rooms = cursor.fetchall()
                for room in rooms:
                    print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def view_equipment(self):
        print("\nEquipment and Maintenance Schedules:")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT equipment_id, name, maintenance_schedule FROM equipment")
                equipments = cursor.fetchall()
                for equipment in equipments:
                    print(f"Equipment ID: {equipment[0]}, Name: {equipment[1]}, Maintenance Date: {equipment[2]}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def view_classes(self):
        print("\nClasses and Schedules:")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT class_id, class_name, schedule FROM classes")
                classes = cursor.fetchall()
                for cls in classes:
                    print(f"Class ID: {cls[0]}, Name: {cls[1]}, Schedule: {cls[2]}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def view_billings(self):
        print("\nCurrent Billing Records:")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT fee_id, member_id, amount, due_date, status FROM membership_fees")
                fees = cursor.fetchall()
                for fee in fees:
                    print(f"Billing ID: {fee[0]}, Member ID: {fee[1]}, Amount: ${fee[2]}, Due Date: {fee[3]}, Status: {fee[4]}")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def manage_room_booking(self):
        self.view_rooms()
        action = input("Choose action (Create, Update, Delete): ").lower()
        if action == 'create':
            room_name = input("Enter room name: ")
            capacity = input("Enter room capacity: ")
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO rooms (room_name, capacity)
                        VALUES (%s, %s)
                    """, (room_name, capacity))
                self.db_connection.commit()
                print("Room booking created successfully.")
            except psycopg2.Error as e:
                print(f"Database error: {e}")

        elif action == 'update':
            room_id = input("Enter room ID: ")
            room_name = input("Enter new room name (leave blank if no change): ")
            capacity = input("Enter new capacity (leave blank if no change): ")
            updates = []
            params = []
            if room_name:
                updates.append("room_name = %s")
                params.append(room_name)
            if capacity:
                updates.append("capacity = %s")
                params.append(capacity)
            if updates:
                params.append(room_id)
                update_query = f"UPDATE rooms SET {', '.join(updates)} WHERE room_id = %s"
                try:
                    with self.db_connection.cursor() as cursor:
                        cursor.execute(update_query, params)
                    self.db_connection.commit()
                    print("Room booking updated successfully.")
                except psycopg2.Error as e:
                    print(f"Database error: {e}")

        elif action == 'delete':
            room_id = input("Enter room ID to delete: ")
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
                self.db_connection.commit()
                print("Room booking deleted successfully.")
            except psycopg2.Error as e:
                print(f"Database error: {e}")

    def monitor_equipment_maintenance(self):
        self.view_equipment()
        equipment_id = input("Enter equipment ID to update schedule: ")
        new_schedule = input("Enter new maintenance schedule (YYYY-MM-DD): ")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE equipment SET maintenance_schedule = %s WHERE equipment_id = %s
                """, (new_schedule, equipment_id))
            self.db_connection.commit()
            print("Equipment maintenance schedule updated successfully.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def update_class_schedule(self):
        self.view_classes()
        class_id = input("Enter class ID to update schedule: ")
        new_schedule = input("Enter new schedule (TIMESTAMP 'YYYY-MM-DD HH:MM:SS'): ")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE classes SET schedule = %s WHERE class_id = %s
                """, (new_schedule, class_id))
            self.db_connection.commit()
            print("Class schedule updated successfully.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def process_billing(self):
        self.view_billings()
        member_id = input("Enter member ID to process billing: ")
        amount = input("Enter amount to be billed: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        status = input("Enter status (Due, Paid): ")
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO membership_fees (member_id, amount, due_date, status)
                    VALUES (%s, %s, %s, %s)
                """, (member_id, amount, due_date, status))
            self.db_connection.commit()
            print("Billing processed successfully.")
        except psycopg2.Error as e:
            print(f"Database error: {e}")
