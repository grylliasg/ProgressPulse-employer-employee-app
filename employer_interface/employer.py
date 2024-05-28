from employee_interface.employee import User
import connect
from datetime import datetime
from contextlib import contextmanager

@contextmanager
def get_cursor():
    connection = connect.get_connection()
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        cursor.close()

class Employer(User):
    def __init__(self, name, user_id, username, password, role, team_id):
        super().__init__(user_id, name, username, password, role)
        self.team_id = team_id

    def create_task(self, description, deadline, user_id, project_id):
        if not description:
            raise ValueError("Task description cannot be empty.")
        if not self.validate_date(deadline):
            raise ValueError("Invalid date format for deadline.")
        if not self.validate_user_id(user_id):
            raise ValueError("Invalid user_id.")

        query = '''
        INSERT INTO Tasks (TaskDescription, TaskDeadline, TaskStatus, UserID, ProjectID)
        VALUES (%s, %s, %s, %s, %s)
        '''
        task_status = 'Μη ολοκληρωμένη'
        with get_cursor() as cursor:
            cursor.execute(query, (description, deadline, task_status, user_id, project_id))

    def create_project(self, name, description, team_id):
        if not name:
            raise ValueError("Project name cannot be empty.")
        if not self.validate_team_id(team_id):
            raise ValueError("Invalid team_id.")

        query = '''
        INSERT INTO Projects (ProjectName, ProjectDescription, ProjectStatus, TeamID)
        VALUES (%s, %s, %s, %s)
        '''
        project_status = 'Σε εξέλιξη'
        with get_cursor() as cursor:
            cursor.execute(query, (name, description, project_status, team_id))

    def delete_project(self, project_id):
        if not self.validate_project_id(project_id):
            raise ValueError("Invalid project_id.")

        delete_tasks_query = 'DELETE FROM Tasks WHERE ProjectID = %s'
        delete_project_query = 'DELETE FROM Projects WHERE ProjectID = %s'

        with get_cursor() as cursor:
            cursor.execute(delete_tasks_query, (project_id,))
            cursor.execute(delete_project_query, (project_id,))

    def create_meeting(self, meeting_datetime, meeting_agenda, team_id):
        if not self.validate_datetime(meeting_datetime):
            raise ValueError("Invalid datetime format for meeting.")
        if not self.validate_team_id(team_id):
            raise ValueError("Invalid team_id.")

        query = '''
        INSERT INTO Meetings (MeetingDateTime, MeetingAgenda, TeamID)
        VALUES (%s, %s, %s)
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (meeting_datetime, meeting_agenda, team_id))

    def delete_meeting(self, meeting_id):
        if not self.validate_meeting_id(meeting_id):
            raise ValueError("Invalid meeting_id.")

        query = 'DELETE FROM Meetings WHERE MeetingID = %s'
        with get_cursor() as cursor:
            cursor.execute(query, (meeting_id,))

    def edit_meeting(self, meeting_id, new_meeting_datetime=None, new_meeting_agenda=None):
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

        with get_cursor() as cursor:
            cursor.execute(query, tuple(params))

    def edit_project(self, project_id, new_project_name=None, new_project_description=None, new_project_status=None):
        if not self.validate_project_id(project_id):
            raise ValueError("Invalid project_id.")

        query_parts = []
        params = []

        if new_project_name is not None:
            query_parts.append("ProjectName = %s")
            params.append(new_project_name)
        
        if new_project_description is not None:
            query_parts.append("ProjectDescription = %s")
            params.append(new_project_description)
        
        if new_project_status is not None:
            query_parts.append("ProjectStatus = %s")
            params.append(new_project_status)
        
        if not query_parts:
            raise ValueError("No new values provided to update the project")

        query = "UPDATE Projects SET " + ", ".join(query_parts) + " WHERE ProjectID = %s"
        params.append(project_id)

        with get_cursor() as cursor:
            cursor.execute(query, tuple(params))

    def view_progress(self):
        query = '''
        SELECT p.ProjectID, p.ProjectName, 
               COUNT(t.TaskID) AS TotalTasks,
               SUM(CASE WHEN t.TaskStatus = 'Completed' THEN 1 ELSE 0 END) AS CompletedTasks
        FROM Projects p
        LEFT JOIN Tasks t ON p.ProjectID = t.ProjectID
        WHERE p.TeamID = %s
        GROUP BY p.ProjectID, p.ProjectName
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (self.team_id,))
            progress_data = cursor.fetchall()
        return progress_data

    def accept_leave_request(self, leave_request_id):
        query = '''
        UPDATE LeaveRequests
        SET LeaveStatus = 'Αποδεκτή'
        WHERE LeaveRequestID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (leave_request_id,))

    def deny_leave_request(self, leave_request_id):
        query = '''
        UPDATE LeaveRequests
        SET LeaveStatus = 'Απορριμμένη'
        WHERE LeaveRequestID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (leave_request_id,))

    
    
    def view_leave_requests(self):
        query = '''
        SELECT *
        FROM LeaveRequests
        WHERE UserID IN (
            SELECT UserID
            FROM Users
            WHERE UserRole = 'employee' AND Team = %s
        )
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (self.team_id,))
            leave_requests = cursor.fetchall()
        return leave_requests
    

    def change_team_name(self, new_team_name):
        query = '''
        UPDATE Teams
        SET TeamName = %s
        WHERE TeamID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (new_team_name, self.team_id))

    
    def change_team_description(self, new_team_description):
        query = '''
        UPDATE Teams
        SET TeamDescription = %s
        WHERE TeamID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (new_team_description, self.team_id))

    
    def remove_member_from_team(self, user_id):
        query = '''
        UPDATE Users
        SET Team = NULL
        WHERE UserID = %s AND Team = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (user_id, self.team_id))

    def validate_user_id(self, user_id):
        query = "SELECT UserID FROM users WHERE UserID = %s"
        with get_cursor() as cursor:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
        return result is not None

    def validate_team_id(self, team_id):
        query = "SELECT TeamID FROM teams WHERE TeamID = %s"
        with get_cursor() as cursor:
            cursor.execute(query, (team_id,))
            result = cursor.fetchone()
        return result is not None

    def validate_project_id(self, project_id):
        query = "SELECT ProjectID FROM Projects WHERE ProjectID = %s"
        with get_cursor() as cursor:
            cursor.execute(query, (project_id,))
            result = cursor.fetchone()
        return result is not None

    def validate_meeting_id(self, meeting_id):
        query = "SELECT MeetingID FROM Meetings WHERE MeetingID = %s"
        with get_cursor() as cursor:
            cursor.execute(query, (meeting_id,))
            result = cursor.fetchone()
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
    query = "SELECT * FROM `users` WHERE `UserRole` = 'employer';"
    with get_cursor() as cursor:
        cursor.execute(query)
        employers_data = cursor.fetchall()
    
    employers = []
    for employer_data in employers_data:
        employer = Employer(*employer_data)
        employers.append(employer)
    
    return employers


if __name__ == "__main__":
    employers = fetch_employers()
    if employers:
        employer = employers[0]
        
        # Remove a member from the team by updating their team to NULL
        member_user_id_to_remove = 1  # Example user ID to be removed from the team
        employer.remove_member_from_team(member_user_id_to_remove)
        print(f"User with ID {member_user_id_to_remove} removed from the team.")
    



