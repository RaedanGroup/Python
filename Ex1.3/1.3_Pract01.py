a = int(input("Enter 1st number: "))
b = int(input("Enter 2nd number: "))
c = int(input("Choose an operation: 1 for addition, 2 for subtraction, 3 for multiplication, 4 for division: "))
if c == 1:
    print("The sum of these numbers is " + str(a + b))
elif c == 2:
    print("The difference of these numbers is " + str(a - b))
elif c == 3:
    print("The product of these numbers is " + str(a * b))
elif c == 4:
    print("The quotient of these numbers is " + str(a / b))
else:
    print("Invalid operation")
    