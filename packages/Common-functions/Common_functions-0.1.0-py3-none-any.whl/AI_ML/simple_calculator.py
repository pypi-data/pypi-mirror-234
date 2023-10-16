def calculator():
    print("Simple Calculator Program")
    print("Enter 'x' to exit")

    while True:
        num1 = float(input("Enter the first number: "))
        if num1 == 'x':
            break

        operator = input("Enter the operator (+, -, *, /): ")
        if operator == 'x':
            break

        num2 = float(input("Enter the second number: "))
        if num2 == 'x':
            break

        result = None

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                print("Error: Division by zero!")
                continue
        else:
            print("Invalid operator!")
            continue

        print(f"Result: {result}\n")

