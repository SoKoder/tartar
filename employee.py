

class Employee:
    instance_variables = {'first','last','salary','employee_number','fullname'}
 #   instance_variables = set()
    number_of_employees = 0

    def __setattr__(self, instance, value):
        if( instance in Employee.instance_variables ):
            object.__setattr__(self,instance,value)
        else:
            raise AttributeError( 'Bad field name {}'.format(instance))

    def __repr__(self):
        return str(self.employee_number) + ' ' + self.fullname + ' ' + str(self.salary) + ' ' +self.email

    def __init__(self,first,last,salary):
        self.first                    = first
        self.last                     = last
        self.salary                   = salary
        Employee.number_of_employees += 1
        self.employee_number          = Employee.number_of_employees

    @property
    def email(self):
        return '{}.{}@me.com'.format(self.first,self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first,self.last)

    @fullname.setter
    def fullname(self,name):
        first, last = name.split(' ')
        self.first,self.last = (first,last)

if(__name__ == '__main__'):

    emp_1 = Employee('John','Duh',None)
    emp_2 = Employee('Jane','Air',10000)

    print(emp_1)
    print(emp_2)

    emp_1.saalary=20000  # should have been emp_1.salary=20000
    print(emp_1)


