class Task:
    def __init__(self, title, description, deadline, completed):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.completed = completed


class Meeting:
    def __init__(self, meetingName, date):
        self.meetingName = meetingName
        self.date = date


class Leave:
    def __init__(self, leaveName, leaveStart, leaveEnd):
        self.leaveName = leaveName
        self.leaveStart = leaveStart
        self.leaveEnd = leaveEnd

