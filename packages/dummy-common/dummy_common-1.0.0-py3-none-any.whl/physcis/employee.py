import datetime
class Employee:
    raise_amount = 1.5
    def __init__(self,firstname,lastname,salary) -> None:
        print('Init method called')
        self.firstname = firstname
        self.lastname = lastname
        self.email = firstname + '.' + lastname + '@email.com'
        self.salary = salary
    @property
    def fullname(self) -> str:
        return '{} {}'.format(self.firstname,self.lastname)
    @fullname.setter
    def fullnames(self,first):
        self.firstname = first
    def apply_raise(self) -> None:
        self.salary = int(self.salary * self.raise_amount)

    @classmethod
    def from_string(cls,emp_str) -> 'Employee':
        first,last,salary =emp_str.split('-')
        return cls(first,last,salary)
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or  day.weekday() == 6:
            return False
        return True
    def __repr__(self):
        return "Employee('{}','{}','{}')".format(self.firstname,self.lastname,self.salary)
class Developer(Employee):
    def __init__(self,firstname,lastname,salary,lang_frm='Java'):
        super().__init__(firstname,lastname,salary)
        self.lang_frm = lang_frm
   
# emp1 =  Developer('Velmurugan','Dhanapal',50000,'Python')
# emp2 =  Developer('Priya','Subramaniyam',40000,'Node JS')

# emp = Employee.from_string('vel-murugan-40000')
# emp.fullnames = 'vel123'
# print(emp.fullname)
# print(emp.fullname())
# print(emp.__dict__)
# print(emp1.__dict__)
# print(emp2.__dict__)

# print( isinstance(emp,Developer))
# print( isinstance(emp1,Employee))

# my_date = datetime.date(2023,10,6)
# print(my_date.weekday())
# print(Employee.is_workday(my_date))

# print(repr((emp1)))
