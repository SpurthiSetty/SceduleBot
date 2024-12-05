import datetime

# Course class to represent a course and its schedule details.
class Course:
    def __init__(self, code, start_time, duration, days):
        self.code = code  # Course code
        self.start_time = datetime.datetime.strptime(start_time, '%H:%M')  # Convert to datetime object
        self.duration = duration  # Duration in hours
        self.days = days  # Days the class is available

    def __str__(self):
        return f"{self.code}, {self.start_time.strftime('%H:%M')} for {self.duration} hours, Days: {', '.join(self.days)}"

# Preferences class to store the user's preferred time-off days and hours.
class Preferences:
    def __init__(self):
        self.days_off = []  # Days user prefers off (e.g., ['Monday', 'Friday'])
        self.hours_off_start = None  # Start of preferred off hours (e.g., '09:00')
        self.hours_off_end = None  # End of preferred off hours (e.g., '12:00')

    def set_days_off(self, days):
        self.days_off = days  # List of days off

    def set_hours_off(self, start, end):
        self.hours_off_start = datetime.datetime.strptime(start, '%H:%M')
        self.hours_off_end = datetime.datetime.strptime(end, '%H:%M')

    def __str__(self):
        days_off_str = ', '.join(self.days_off)
        hours_off_str = f"{self.hours_off_start.strftime('%H:%M')} to {self.hours_off_end.strftime('%H:%M')}"
        return f"Days off: {days_off_str}, Hours off: {hours_off_str}"

# Schedule class to store the generated class schedule.
class Schedule:
    def __init__(self):
        self.courses = []  # List to hold courses

    def add_course(self, course):
        self.courses.append(course)

    def display(self):
        print("Your class schedule:")
        for course in self.courses:
            print(course)

# User class to manage user preferences and schedule.
class User:
    def __init__(self):
        self.preferences = Preferences()
        self.schedule = Schedule()

    def set_preferences(self):
        days = input("Enter preferred days off (comma separated): ").split(",")
        self.preferences.set_days_off([day.strip() for day in days])

        hours_off_start = input("Enter start time for hours off (HH:MM): ")
        hours_off_end = input("Enter end time for hours off (HH:MM): ")
        self.preferences.set_hours_off(hours_off_start, hours_off_end)

    def add_course(self, course):
        self.schedule.add_course(course)

    def display_schedule(self):
        self.schedule.display()

# ScheduleFactory class to generate possible schedules based on inputs.
class ScheduleFactory:
    def __init__(self, user):
        self.user = user

    def validate_schedule(self):
        # Check if any required class conflicts with the preferred days off or hours off.
        for course in self.user.schedule.courses:
            for day in course.days:
                if day in self.user.preferences.days_off:
                    print(f"Error: {course.code} cannot be scheduled on {day} because it's a day off.")
                    return False
                
            # Check if course time conflicts with preferred hours off
            course_end_time = course.start_time + datetime.timedelta(hours=course.duration)
            if (self.user.preferences.hours_off_start <= course.start_time <= self.user.preferences.hours_off_end) or \
               (self.user.preferences.hours_off_start <= course_end_time <= self.user.preferences.hours_off_end):
                print(f"Error: {course.code} conflicts with the preferred hours off.")
                return False
        
        return True

    def generate_schedule(self, courses_data):
        print("Generating your schedule...")
        for course_data in courses_data:
            for schedule in course_data['available_schedules']:
                course = Course(course_data['code'], schedule['start_time'], schedule['duration'], schedule['days'])
                self.user.add_course(course)

        if self.validate_schedule():
            self.user.display_schedule()
        else:
            print("Schedule could not be created due to conflicts.")

# Main function to simulate the ScheduleBot process.
def main():
    user = User()
    
    # Step 1: Set preferences
    user.set_preferences()

    # Step 2: Define available courses
    courses_data = [
        {'code': 'CS115', 'available_schedules': [{'start_time': '10:00', 'duration': 2, 'days': ['Monday', 'Wednesday']}, {'start_time': '14:00', 'duration': 2, 'days': ['Tuesday', 'Thursday']}]},
        {'code': 'ENGR112', 'available_schedules': [{'start_time': '13:00', 'duration': 1, 'days': ['Tuesday', 'Thursday']}, {'start_time': '09:00', 'duration': 1, 'days': ['Monday', 'Wednesday']}]},
        {'code': 'SSW345', 'available_schedules': [{'start_time': '15:00', 'duration': 2, 'days': ['Monday', 'Wednesday']}, {'start_time': '17:00', 'duration': 2, 'days': ['Tuesday', 'Thursday']}]}
    ]
    
    # Step 3: Generate schedule
    factory = ScheduleFactory(user)
    factory.generate_schedule(courses_data)

# Run the main function
main()