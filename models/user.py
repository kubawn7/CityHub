class User:
    def __init__(self, user_id, first_name, last_name, email, password, role):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"