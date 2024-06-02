from user import User
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

    def create_task(self,name, description, deadline, user_id, project_id):
        if not description:
            raise ValueError("Task description cannot be empty.")
        if not self.validate_date(deadline):
            raise ValueError("Invalid date format for deadline.")
        if not self.validate_user_id(user_id):
            raise ValueError("Invalid user_id.")

        query = '''
        INSERT INTO Tasks (TaskName,TaskDescription, TaskDeadline, TaskStatus, UserID, ProjectID)
        VALUES (%s,%s, %s, %s, %s, %s)
        '''
        task_status = 'Uncompleted'
        with get_cursor() as cursor:
            cursor.execute(query, (name,description, deadline, task_status, user_id, project_id))

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

        # Insert the project with the fetched team ID
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

    def create_meeting(self, meeting_datetime, meeting_agenda, team_id,name):
        if not self.validate_team_id(team_id):
            raise ValueError("Invalid team_id.")

        query = '''
        INSERT INTO Meetings (MeetingDateTime, MeetingAgenda, TeamID, MeetingName)
        VALUES (%s, %s, %s,%s)
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (meeting_datetime, meeting_agenda, team_id,name))

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
            WHERE UserRole = 'employee' AND Team = %s AND LeaveStatus ='Υπο εξέταση'
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
        update_team_query = '''
        UPDATE Users
        SET Team = NULL
        WHERE UserID = %s AND Team = %s
        '''
        
        delete_tasks_query = '''
        DELETE FROM Tasks
        WHERE UserID = %s
        '''
        
        delete_leave_requests_query = '''
        DELETE FROM LeaveRequests
        WHERE UserID = %s
        '''
        
        with get_cursor() as cursor:
            cursor.execute(update_team_query, (user_id, self.team_id))
            cursor.execute(delete_tasks_query, (user_id,))
            cursor.execute(delete_leave_requests_query, (user_id,))


    
    def accept_withdrawal(self, user_id):
        # Check if the user is in the same team as the employer
        check_query = '''
        SELECT Team
        FROM Users
        WHERE UserID = %s AND Team = %s
        '''
        update_query = '''
        UPDATE withdrawals
        SET Status = 'Εγκεκριμένη'
        WHERE UserID = %s
        '''

        team_null = '''
        UPDATE users
        SET Team = null
        WHERE UserID = %s
        '''

        with get_cursor() as cursor:
            cursor.execute(check_query, (user_id, self.team_id))
            user_team = cursor.fetchone()
            if user_team:  # If the user is in the same team
                cursor.execute(update_query, (user_id,))
                cursor.execute(team_null,(user_id,))
                print("Done!")
            else:
                print("Employer and User are not in the same team!!")
    


    def deny_withdrawal(self, user_id):
        # Check if the user is in the same team as the employer
        check_query = '''
        SELECT Team
        FROM Users
        WHERE UserID = %s AND Team = %s
        '''
        update_query = '''
        UPDATE withdrawals
        SET Status = 'Απορριμμένη'
        WHERE UserID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(check_query, (user_id, self.team_id))
            user_team = cursor.fetchone()
            if user_team:  # If the user is in the same team
                cursor.execute(update_query, (user_id,))
                print("Done!")
            else:
                print("Employer and User are not in the same team!!")
    

    def view_withdrawal_requests(self):
        query = '''
        SELECT w.UserID, u.Username, w.Status
        FROM withdrawals w
        JOIN Users u ON w.UserID = u.UserID
        WHERE u.Team = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (self.team_id,))
            withdrawals = cursor.fetchall()
            return withdrawals 




    def invite_member_to_team(self, user_id):
        query = '''
        UPDATE Users
        SET Team = %s
        WHERE UserID = %s
        '''
        with get_cursor() as cursor:    
            cursor.execute(query, (self.team_id, user_id))

    

    def view_meetings(self):
        query = '''
        SELECT MeetingID, MeetingDateTime, MeetingAgenda
        FROM Meetings
        WHERE TeamID = %s
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (self.team_id,))
            meetings = cursor.fetchall()
        return meetings

    
    def view_team_members(self):
        query = '''
        SELECT *
        FROM Users
        WHERE Team = %s AND UserRole= 'employee'
        
        '''
        with get_cursor() as cursor:
            cursor.execute(query, (self.team_id,))
            leave_requests = cursor.fetchall()
        return leave_requests
    

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





    



