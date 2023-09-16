class User:

    def __new__(cls, name, email, password):
        try:
            if type(email) != str:
                raise TypeError("Email must be a string")
            if type(password) != str:
                raise TypeError("Password must be a string")
            if type(name) != str:
                raise TypeError("Name must be a string")
        except TypeError as err:
            print(err)
            return False
        else:
            return super().__new__(cls)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def sql_format(self):
        return f"('{self.email}', '{self.name}', '{self.password}')"
