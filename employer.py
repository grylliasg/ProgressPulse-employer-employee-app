from tasks1 import User
import connect
from datetime import datetime

class Employer(User):
    def __init__(self, user_id, username, password, role, team_id):
        super().__init__(user_id, username, password, role)
        self.team_id = team_id

    def create_task(self, description, deadline, user_id, project_id):
        # Check for empty description
        if not description:
            raise ValueError("Task description cannot be empty.")
        # Check for invalid date format
        if not self.validate_date(deadline):
            raise ValueError("Invalid date format for deadline.")
        # Check for invalid user_id
        if not self.validate_user_id(user_id):
            raise ValueError("Invalid user_id.")
        
        query = '''
        INSERT INTO Tasks (TaskDescription, TaskDeadline, TaskStatus, UserID, ProjectID)
        VALUES (%s, %s, %s, %s, %s)
        '''
        task_status = 'Μη ολοκληρωμένη'  # Initial status for new tasks
        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, (description, deadline, task_status, user_id, project_id))
        connection.commit()  # Commit using the connection object
        cursor.close()

    def create_project(self, name, description, team_id):
        # Check for empty project name
        if not name:
            raise ValueError("Project name cannot be empty.")
        # Check for invalid team_id
        if not self.validate_team_id(team_id):
            raise ValueError("Invalid team_id.")
        
        query = '''
        INSERT INTO Projects (ProjectName, ProjectDescription, ProjectStatus, TeamID)
        VALUES (%s, %s, %s, %s)
        '''
        project_status = 'Σε εξέλιξη'  # Initial status for new tasks
        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, (name, description, project_status, team_id))
        connection.commit()  # Commit using the connection object
        cursor.close()

    def delete_project(self, project_id):
        # Check for invalid project_id
        if not self.validate_project_id(project_id):
            raise ValueError("Invalid project_id.")
        
        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        
        # Delete all tasks associated with the project
        delete_tasks_query = '''
        DELETE FROM Tasks
        WHERE ProjectID = %s
        '''
        cursor.execute(delete_tasks_query, (project_id,))
        
        # Delete the project itself
        delete_project_query = '''
        DELETE FROM Projects
        WHERE ProjectID = %s
        '''
        cursor.execute(delete_project_query, (project_id,))
        
        connection.commit()  # Commit both changes using the connection object
        cursor.close()

    def create_meeting(self, meeting_datetime, meeting_agenda, team_id):
        # Check for invalid date format
        if not self.validate_datetime(meeting_datetime):
            raise ValueError("Invalid datetime format for meeting.")
        # Check for invalid team_id
        if not self.validate_team_id(team_id):
            raise ValueError("Invalid team_id.")
        
        query = '''
        INSERT INTO Meetings (MeetingDateTime, MeetingAgenda, TeamID)
        VALUES (%s, %s, %s)
        '''
        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, (meeting_datetime, meeting_agenda, team_id))
        connection.commit()  # Commit the changes using the connection object
        cursor.close()

    def delete_meeting(self, meeting_id):
        # Check for invalid meeting_id
        if not self.validate_meeting_id(meeting_id):
            raise ValueError("Invalid meeting_id.")
        
        query = '''
        DELETE FROM Meetings
        WHERE MeetingID = %s
        '''
        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, (meeting_id,))
        connection.commit()  # Commit the changes using the connection object
        cursor.close()

    def edit_meeting(self, meeting_id, new_meeting_datetime=None, new_meeting_agenda=None):
        # Check for invalid meeting_id
        if not self.validate_meeting_id(meeting_id):
            raise ValueError("Invalid meeting_id.")

        query_parts = []
        params = []

        if new_meeting_datetime is not None:
            if not self.validate_datetime(new_meeting_datetime):
                raise ValueError("Invalid datetime format for meeting.")
            query_parts.append("MeetingDateTime = %s")
            params.append(new_meeting_datetime)
        
        if new_meeting_agenda is not None:
            query_parts.append("MeetingAgenda = %s")
            params.append(new_meeting_agenda)
        
        if not query_parts:
            raise ValueError("No new values provided to update the meeting")

        query = "UPDATE Meetings SET " + ", ".join(query_parts) + " WHERE MeetingID = %s"
        params.append(meeting_id)

        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        connection.commit()  # Commit the changes using the connection object
        cursor.close()

    def edit_project(self, project_id, new_project_name=None, new_project_description=None, new_project_status=None):
        # Check for invalid project_id
        if not self.validate_project_id(project_id):
            raise ValueError("Invalid project_id.")

        query_parts = []
        params = []

        # Check if new_project_name is provided
        if new_project_name is not None:
            query_parts.append("ProjectName = %s")
            params.append(new_project_name)
        
        # Check if new_project_description is provided
        if new_project_description is not None:
            query_parts.append("ProjectDescription = %s")
            params.append(new_project_description)
        
        # Check if new_project_status is provided
        if new_project_status is not None:
            query_parts.append("ProjectStatus = %s")
            params.append(new_project_status)
        
        # If no new values provided, raise an error
        if not query_parts:
            raise ValueError("No new values provided to update the project")

        # Construct the update query dynamically
        query = "UPDATE Projects SET " + ", ".join(query_parts) + " WHERE ProjectID = %s"
        params.append(project_id)

        connection = connect.get_connection()  # Get the connection object
        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        connection.commit()  # Commit the changes using the connection object
        cursor.close()

    # Helper methods to validate IDs and dates
    def validate_user_id(self, user_id):
        query = "SELECT UserID FROM users WHERE UserID = %s"
        connection = connect.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def validate_team_id(self, team_id):
        query = "SELECT TeamID FROM teams WHERE TeamID = %s"
        connection = connect.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (team_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def validate_project_id(self, project_id):
        query = "SELECT ProjectID FROM Projects WHERE ProjectID = %s"
        connection = connect.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (project_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def validate_meeting_id(self, meeting_id):
        query = "SELECT MeetingID FROM Meetings WHERE MeetingID = %s"
        connection = connect.get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (meeting_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_datetime(self, datetime_str):
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            return True
        except ValueError:
            return False

def fetch_employers():
    query = '''
    SELECT u.UserID, u.Username, u.Password, u.UserRole, t.TeamID
    FROM users u
    JOIN teams t ON u.UserID = t.employer_id
    WHERE u.UserRole = "employer"
    '''
    connection = connect.get_connection()  # Get the connection object
    cursor = connection.cursor()
    cursor.execute(query)
    employers_data = cursor.fetchall()
    
    employers = []
    for employer_data in employers_data:
        employer = Employer(*employer_data)
        employers.append(employer)
    
    cursor.close()
    return employers

# Fetch employers and print them for demonstration purposes
if __name__ == "__main__":
    employers = fetch_employers()
    for emp in employers:
        print(emp.__dict__)
    
    # Create a task for demonstration purposes
    if employers:
        employer = employers[0]
        
        try:
            employer.edit_meeting(4,"2024-06-01 11:00:00","Updated")
            print("Done everything okay!!")
        except ValueError as e:
            print(f"Error: {e}")
    



