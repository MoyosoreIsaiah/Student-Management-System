import json
from datetime import datetime


# =========================
# PERSON CLASS
# =========================

class Person:
    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone

    def display_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Gender:", self.gender)
        print("Phone:", self.phone)


# =========================
# PATIENT CLASS
# =========================

class Patient(Person):
    def __init__(self, patient_id, name, age, gender, phone):
        super().__init__(name, age, gender, phone)
        self.patient_id = patient_id
        self.appointments = []

    def display_info(self):
        print("\nPatient ID:", self.patient_id)
        super().display_info()


# =========================
# DOCTOR CLASS
# =========================

class Doctor(Person):
    def __init__(self, doctor_id, name, age, gender, phone, specialization):
        super().__init__(name, age, gender, phone)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.appointments = []

    def display_info(self):
        print("\nDoctor ID:", self.doctor_id)
        super().display_info()
        print("Specialization:", self.specialization)


# =========================
# HOSPITAL SYSTEM CLASS
# =========================

class HospitalSystem:

    def __init__(self):
        self.patients = {}
        self.doctors = {}
        self.appointments = []
        self.bills = []

    # =========================
    # REGISTER PATIENT
    # =========================

    def register_patient(self):
        print("\n--- REGISTER PATIENT ---")

        patient_id = input("Enter patient ID: ")

        if patient_id in self.patients:
            print("Patient already exists.")
            return

        name = input("Enter full name: ")

        # Handle wrong age input
        try:
            age = int(input("Enter age: "))

            if age <= 0:
                print("Age must be greater than 0.")
                return

        except ValueError:
            print("Invalid age. Please enter a number.")
            return

        gender = input("Enter gender: ")
        phone = input("Enter phone number: ")

        patient = Patient(
            patient_id,
            name,
            age,
            gender,
            phone
        )

        self.patients[patient_id] = patient

        print("Patient registered successfully.")


    # =========================
    # ADD DOCTOR
    # =========================

    def add_doctor(self):
        print("\n--- ADD DOCTOR ---")

        doctor_id = input("Enter doctor ID: ")

        if doctor_id in self.doctors:
            print("Doctor already exists.")
            return

        name = input("Enter doctor's name: ")

        try:
            age = int(input("Enter doctor's age: "))

            if age <= 0:
                print("Age must be greater than 0.")
                return

        except ValueError:
            print("Invalid age.")
            return

        gender = input("Enter gender: ")
        phone = input("Enter phone number: ")
        specialization = input("Enter specialization: ")

        doctor = Doctor(
            doctor_id,
            name,
            age,
            gender,
            phone,
            specialization
        )

        self.doctors[doctor_id] = doctor

        print("Doctor added successfully.")


    # =========================
    # VIEW PATIENT
    # =========================

    def view_patient(self):
        print("\n--- SEARCH PATIENT ---")

        patient_id = input("Enter patient ID: ")

        if patient_id not in self.patients:
            print("Patient record not found.")
            return

        patient = self.patients[patient_id]

        patient.display_info()

        print("\nAppointments:")

        if len(patient.appointments) == 0:
            print("No appointments.")

        else:
            for appointment in patient.appointments:
                print(
                    "Doctor:",
                    appointment["doctor_id"],
                    "| Date:",
                    appointment["date"],
                    "| Time:",
                    appointment["time"]
                )


    # =========================
    # VIEW DOCTORS
    # =========================

    def view_doctors(self):
        print("\n--- DOCTORS ---")

        if len(self.doctors) == 0:
            print("No doctors available.")
            return

        for doctor in self.doctors.values():
            doctor.display_info()


    # =========================
    # BOOK APPOINTMENT
    # =========================

    def book_appointment(self):
        print("\n--- BOOK APPOINTMENT ---")

        patient_id = input("Enter patient ID: ")

        # Check patient exists
        if patient_id not in self.patients:
            print("Patient record not found.")
            return

        doctor_id = input("Enter doctor ID: ")

        # Check doctor exists
        if doctor_id not in self.doctors:
            print("Doctor not found.")
            return

        date = input("Enter appointment date (DD-MM-YYYY): ")
        time = input("Enter appointment time (HH:MM): ")

        # =========================
        # CHECK VALID DATE
        # =========================

        try:
            appointment_date = datetime.strptime(
                date + " " + time,
                "%d-%m-%Y %H:%M"
            )

        except ValueError:
            print("Invalid date or time.")
            return

        # =========================
        # CHECK DUPLICATE BOOKING
        # =========================

        for appointment in self.appointments:

            if (
                appointment["doctor_id"] == doctor_id
                and appointment["date"] == date
                and appointment["time"] == time
            ):
                print("Doctor is already booked at this time.")
                return

        # =========================
        # CREATE APPOINTMENT
        # =========================

        appointment = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": date,
            "time": time
        }

        self.appointments.append(appointment)

        self.patients[patient_id].appointments.append(appointment)
        self.doctors[doctor_id].appointments.append(appointment)

        print("Appointment booked successfully.")
        print("Appointment date:", appointment_date.strftime("%d-%m-%Y"))
        print("Appointment time:", appointment_date.strftime("%H:%M"))


    # =========================
    # VIEW APPOINTMENTS
    # =========================

    def view_appointments(self):
        print("\n--- ALL APPOINTMENTS ---")

        if len(self.appointments) == 0:
            print("No appointments available.")
            return

        for appointment in self.appointments:

            print(
                "Patient:",
                appointment["patient_id"],
                "| Doctor:",
                appointment["doctor_id"],
                "| Date:",
                appointment["date"],
                "| Time:",
                appointment["time"]
            )


    # =========================
    # CALCULATE BILL
    # =========================

    def calculate_bill(self):
        print("\n--- CALCULATE BILL ---")

        patient_id = input("Enter patient ID: ")

        if patient_id not in self.patients:
            print("Patient record not found.")
            return

        try:
            consultation_fee = float(
                input("Enter consultation fee: ")
            )

            medication_fee = float(
                input("Enter medication fee: ")
            )

            if consultation_fee < 0 or medication_fee < 0:
                print("Fees cannot be negative.")
                return

        except ValueError:
            print("Please enter valid numbers.")
            return

        total_bill = consultation_fee + medication_fee

        bill = {
            "patient_id": patient_id,
            "consultation_fee": consultation_fee,
            "medication_fee": medication_fee,
            "total_bill": total_bill
        }

        self.bills.append(bill)

        print("\n--- BILL ---")
        print("Patient ID:", patient_id)
        print("Consultation Fee:", consultation_fee)
        print("Medication Fee:", medication_fee)
        print("Total Bill:", total_bill)


    # =========================
    # VIEW BILL HISTORY
    # =========================

    def view_bill_history(self):
        print("\n--- BILL HISTORY ---")

        patient_id = input("Enter patient ID: ")

        found = False

        for bill in self.bills:

            if bill["patient_id"] == patient_id:

                found = True

                print("\nConsultation Fee:",
                      bill["consultation_fee"])

                print("Medication Fee:",
                      bill["medication_fee"])

                print("Total Bill:",
                      bill["total_bill"])

        if not found:
            print("No bill history found for this patient.")


    # =========================
    # SAVE RECORDS TO FILE
    # =========================

    def save_records(self):
        data = {
            "patients": {},
            "doctors": {},
            "appointments": self.appointments,
            "bills": self.bills
        }

        # Save patients
        for patient_id, patient in self.patients.items():

            data["patients"][patient_id] = {
                "patient_id": patient.patient_id,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender,
                "phone": patient.phone
            }

        # Save doctors
        for doctor_id, doctor in self.doctors.items():

            data["doctors"][doctor_id] = {
                "doctor_id": doctor.doctor_id,
                "name": doctor.name,
                "age": doctor.age,
                "gender": doctor.gender,
                "phone": doctor.phone,
                "specialization": doctor.specialization
            }

        try:

            with open("hospital_records.json", "w") as file:

                json.dump(data, file, indent=4)

            print("Records saved successfully.")

        except Exception as error:

            print("Error saving records:", error)


    # =========================
    # LOAD RECORDS FROM FILE
    # =========================

    def load_records(self):

        try:

            with open("hospital_records.json", "r") as file:

                data = json.load(file)

            # Load patients
            for patient_id, patient_data in data["patients"].items():

                patient = Patient(
                    patient_data["patient_id"],
                    patient_data["name"],
                    patient_data["age"],
                    patient_data["gender"],
                    patient_data["phone"]
                )

                self.patients[patient_id] = patient

            # Load doctors
            for doctor_id, doctor_data in data["doctors"].items():

                doctor = Doctor(
                    doctor_data["doctor_id"],
                    doctor_data["name"],
                    doctor_data["age"],
                    doctor_data["gender"],
                    doctor_data["phone"],
                    doctor_data["specialization"]
                )

                self.doctors[doctor_id] = doctor

            # Load appointments
            self.appointments = data["appointments"]

            # Connect appointments to patients and doctors
            for appointment in self.appointments:

                patient_id = appointment["patient_id"]
                doctor_id = appointment["doctor_id"]

                if patient_id in self.patients:
                    self.patients[
                        patient_id
                    ].appointments.append(appointment)

                if doctor_id in self.doctors:
                    self.doctors[
                        doctor_id
                    ].appointments.append(appointment)

            # Load bills
            self.bills = data["bills"]

            print("Records loaded successfully.")

        except FileNotFoundError:

            print("No previous records found.")

        except json.JSONDecodeError:

            print("The records file is not valid.")


# =========================
# MAIN PROGRAM
# =========================

hospital = HospitalSystem()

hospital.load_records()


while True:

    print("\n")
    print("==============================")
    print("   HOSPITAL RECORD SYSTEM")
    print("==============================")

    print("1. Register Patient")
    print("2. Add Doctor")
    print("3. View Patient")
    print("4. View Doctors")
    print("5. Book Appointment")
    print("6. View Appointments")
    print("7. Calculate Bill")
    print("8. View Bill History")
    print("9. Save Records")
    print("10. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        hospital.register_patient()

    elif choice == "2":

        hospital.add_doctor()

    elif choice == "3":

        hospital.view_patient()

    elif choice == "4":

        hospital.view_doctors()

    elif choice == "5":

        hospital.book_appointment()

    elif choice == "6":

        hospital.view_appointments()

    elif choice == "7":

        hospital.calculate_bill()

    elif choice == "8":

        hospital.view_bill_history()

    elif choice == "9":

        hospital.save_records()

    elif choice == "10":

        hospital.save_records()

        print("Thank you for using the Hospital Record System.")

        break

    else:

        print("Invalid choice. Please try again.")