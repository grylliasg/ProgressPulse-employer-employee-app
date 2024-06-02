from datetime import datetime

class Project:
    def __init__(self, title: str, description: str, deadline: datetime, numberOfTasks: int, numberOfTasksCompleted: int):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.numberOfTasks = numberOfTasks
        self.numberOfTasksCompleted = numberOfTasksCompleted