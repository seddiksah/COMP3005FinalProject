import psycopg2
from members import Member
from trainers import Trainer
from staff import Staff

# Connection parameters
connectionParameters = {
    'dbname': 'COMP3005FinalProjectV2',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

# Connect to the database
def connect():
    try:
        conn = psycopg2.connect(**connectionParameters)
        print("Connection successful.")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None
    

def main_menu():
    print("\nHealth and Fitness Club Management System")
    print("Select a user type:")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    print("0. Exit")
    return input("Select an option: ")

def member_menu():
    print("\nMember Management")
    print("1. Register New Member")
    print("2. Update Personal Information")
    print("3. Update Fitness Goals")
    print("4. Update Health Metrics")
    print("5. View Dashboard")
    print("6. Schedule Training Session")
    print("7. Reschedule Training Session")
    print("8. Cancel Training Session")
    print("0. Return to Main Menu")
    return input("Select an option: ")

def trainer_menu():
    print("\nTrainer Management")
    print("1. Set Availability")
    print("2. View Member Profile")
    print("3. Register New Trainer")
    print("0. Return to Main Menu")
    return input("Select an option: ")

def staff_menu():
    print("\nAdmin Management")
    print("1. Manage Room Booking")
    print("2. Monitor Equipment Maintenance")
    print("3. Update Class Schedule")
    print("4. Process Billing")
    print("5. Register New Admin")
    print("0. Return to Main Menu")
    return input("Select an option: ")

def main():
    conn = connect()
    if conn:
        member = Member(conn)
        trainer = Trainer(conn)
        staff = Staff(conn)

        while True:
            choice = main_menu()

            if choice == "1":
                while True:
                    member_choice = member_menu()
                    if member_choice == "1":
                        member.register()
                    elif member_choice == "2":
                        member.update_personal_info()
                    elif member_choice == "3":
                        member.update_fitness_goals()
                    elif member_choice == "4":
                        member.update_health_metrics()
                    elif member_choice == "5":
                        member.view_dashboard()
                    elif member_choice == "6":
                        member.schedule_training_session()
                    elif member_choice == "7":
                        member.reschedule_training_session()
                    elif member_choice == "8":
                        member.cancel_training_session()
                    elif member_choice == "0":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "2":
                while True:
                    trainer_choice = trainer_menu()
                    if trainer_choice == "1":
                        trainer.set_availability()
                    elif trainer_choice == "2":
                        trainer.view_member_profile()
                    elif trainer_choice == "3":
                        trainer.register_trainer()
                    elif trainer_choice == "0":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "3":
                while True:
                    admin_choice = staff_menu()
                    if admin_choice == "1":
                        staff.manage_room_booking()
                    elif admin_choice == "2":
                        staff.monitor_equipment_maintenance()
                    elif admin_choice == "3":
                        staff.update_class_schedule()
                    elif admin_choice == "4":
                        staff.process_billing()
                    elif admin_choice == "5":
                        staff.register_admin()
                    elif admin_choice == "0":
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")

        conn.close()

if __name__ == '__main__':
    main()
