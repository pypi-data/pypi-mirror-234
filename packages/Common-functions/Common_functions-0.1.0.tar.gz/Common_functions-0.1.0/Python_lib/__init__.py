# Question 1
def greet_user():
    name = input("Enter your name: ")
    print("Welcome,", name)

# Question 2
def calculate_sum():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    total = num1 + num2
    print("The total is:", total)

# Question 3
def convert_celsius_to_fahrenheit():
    celsius = float(input("Enter the temperature in Celsius: "))
    fahrenheit = (9/5) * celsius + 32
    print("The equivalent temperature in Fahrenheit is:", fahrenheit)

# Question 4
def calculate_simple_interest():
    principle = float(input("Enter the principle amount: "))
    rate = float(input("Enter the rate of interest: "))
    time = float(input("Enter the time period: "))
    simple_interest = (principle * rate * time) / 100
    print("The simple interest is:", simple_interest)

# Question 5
def convert_seconds_to_hms():
    seconds = int(input("Enter the number of seconds: "))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    print("Time: {} hours, {} minutes, {} seconds".format(hours, minutes, seconds))

# Question 6
def swap_variables():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    num1, num2 = num2, num1
    print("After swapping, num1 =", num1, "and num2 =", num2)

# Question 7
def swap_variables_without_extra_variable():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    num1 = num1 + num2
    num2 = num1 - num2
    num1 = num1 - num2
    print("After swapping, num1 =", num1, "and num2 =", num2)

# Question 8
def calculate_circle_properties():
    radius = float(input("Enter the radius of the circle: "))
    area = 3.14159 * radius * radius
    circumference = 2 * 3.14159 * radius
    print("Area of the circle:", area)
    print("Circumference of the circle:", circumference)

# Question 9
def calculate_rectangle_properties():
    length = float(input("Enter the length of the rectangle: "))
    width = float(input("Enter the width of the rectangle: "))
    area = length * width
    circumference = 2 * (length + width)
    print("Area of the rectangle:", area)
    print("Circumference of the rectangle:", circumference)

# Question 10
def calculate_triangle_area():
    side1 = float(input("Enter the length of side 1: "))
    side2 = float(input("Enter the length of side 2: "))
    side3 = float(input("Enter the length of side 3: "))
    semi_perimeter = (side1 + side2 + side3) / 2
    area = (semi_perimeter * (semi_perimeter - side1) *
            (semi_perimeter - side2) * (semi_perimeter - side3)) ** 0.5
    print("Area = ",area)

# Question 11
def calculate_compound_interest():
    principle = float(input("Enter the principle amount: "))
    rate = float(input("Enter the rate of interest: "))
    time = float(input("Enter the time period: "))
    compound_interest = principle * ((1 + rate/100) ** time - 1)
    print("The compound interest is:", compound_interest)

# Question 12
def check_even_odd():
    number = int(input("Enter a number: "))
    if number % 2 == 0:
        print("The number is even.")
    else:
        print("The number is odd.")

# Question 13
def find_largest_of_two():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    if num1 > num2:
        print("The largest number is:", num1)
    else:
        print("The largest number is:", num2)

# Question 14
def find_largest_of_three():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    num3 = int(input("Enter the third number: "))
    largest = max(num1, num2, num3)
    print("The largest number is:", largest)

# Question 15
def check_leap_year():
    year = int(input("Enter a year: "))
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print("The year is a leap year.")
    else:
        print("The year is not a leap year.")

# Question 16
def calculate_telephone_bill():
    calls = int(input("Enter the number of calls: "))
    bill = 200
    if calls > 100:
        bill += (calls - 100) * 0.6
    if calls > 150:
        bill += (calls - 150) * 0.5
    if calls > 200:
        bill += (calls - 200) * 0.4
    print("The monthly telephone bill is:", bill)

# Question 17
import math

def calculate_quadratic_roots():
    a = float(input("Enter the coefficient of x^2 (a): "))
    b = float(input("Enter the coefficient of x (b): "))
    c = float(input("Enter the constant term (c): "))
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        print("The roots are real and distinct.")
        print("Root 1:", root1)
        print("Root 2:", root2)
    elif discriminant == 0:
        root = -b / (2*a)
        print("The roots are real and equal.")
        print("Root:", root)
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(abs(discriminant)) / (2*a)
        print("The roots are complex.")
        print("Root 1:", real_part, "+", imaginary_part, "i")
        print("Root 2:", real_part, "-", imaginary_part, "i")

# Question 18
def calculate_grade():
    marks1 = float(input("Enter the marks for subject 1: "))
    marks2 = float(input("Enter the marks for subject 2: "))
    marks3 = float(input("Enter the marks for subject 3: "))
    average = (marks1 + marks2 + marks3) / 3
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"
    print("The average marks is:", average)
    print("The grade is:", grade)

# Question 19
def determine_astrological_sign():
    day = int(input("Enter the day of birth: "))
    month = int(input("Enter the month of birth: "))
    
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        sign = "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        sign = "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        sign = "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        sign = "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        sign = "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        sign = "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        sign = "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        sign = "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        sign = "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        sign = "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        sign = "Aquarius"
    else:
        sign = "Pisces"
    
    print("Your astrological sign is:", sign)

# Question 20
def display_day_of_week():
    number = int(input("Enter a number (1-7): "))
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if number >= 1 and number <= 7:
        day = days[number - 1]
        print("The corresponding day is:", day)
    else:
        print("Invalid number. Please enter a number between 1 and 7.")

# Question 21
def check_vowel_or_consonant():
    character = input("Enter a character: ").lower()
    if len(character) == 1 and character.isalpha():
        if character in "aeiou":
            print("The character is a vowel.")
        else:
            print("The character is a consonant.")
    else:
        print("Invalid input. Please enter a single alphabet character.")

# Question 22
def print_numbers_1_to_10():
    for num in range(1, 11):
        print(num)

# Question 23
def calculate_sum_of_integers():
    number = int(input("Enter a positive integer: "))
    if number <= 0:
        print("Invalid input. Please enter a positive integer.")
        return
    total = 0
    for num in range(1, number + 1):
        total += num
    print("The sum of all integers from 1 to", number, "is:", total)

# Question 24
def print_multiplication_table():
    number = int(input("Enter a number: "))
    print("Multiplication Table of", number)
    for i in range(1, 11):
        print(number, "x", i, "=", number * i)

# Question 25
def calculate_factorial():
    number = int(input("Enter a number: "))
    if number < 0:
        print("Factorial is not defined for negative numbers.")
        return
    factorial = 1
    for num in range(1, number + 1):
        factorial *= num
    print("The factorial of", number, "is:", factorial)

# Question 26
def calculate_power():
    number1 = float(input("Enter the base number: "))
    number2 = float(input("Enter the exponent: "))
    result = number1 ** number2
    print(number1, "raised to the power of", number2, "is:", result)

# Question 27
def reverse_digits():
    number = int(input("Enter a number: "))
    reverse = 0
    while number > 0:
        digit = number % 10
        reverse = reverse * 10 + digit
        number = number // 10
    print("The reversed number is:", reverse)

# Question 28
def calculate_sum_of_digits():
    number = int(input("Enter a positive integer: "))
    if number <= 0:
        print("Invalid input. Please enter a positive integer.")
        return
    total = 0
    while number > 0:
        digit = number % 10
        total += digit
        number = number // 10
    print("The sum of digits is:", total)

# Question 29
def check_palindrome_number():
    number = int(input("Enter a number: "))
    temp = number
    reverse = 0
    while number > 0:
        digit = number % 10
        reverse = reverse * 10 + digit
        number = number // 10
    if temp == reverse:
        print("The number is a palindrome.")
    else:
        print("The number is not a palindrome.")

# Question 30
def decimal_to_binary():
    decimal = int(input("Enter a decimal integer: "))
    binary = bin(decimal)[2:]
    print("The binary equivalent is:", binary)

# Question 31
def binary_to_decimal():
    binary = input("Enter a binary number: ")
    decimal = int(binary, 2)
    print("The decimal equivalent is:", decimal)

# Question 32
def check_prime_number():
    number = int(input("Enter a positive integer: "))
    if number <= 1:
        print("The number is not a prime number.")
        return
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            print("The number is not a prime number.")
            return
    print("The number is a prime number.")

# Question 33
def calculate_hcf():
    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))
    smaller = min(number1, number2)
    for i in range(smaller, 0, -1):
        if number1 % i == 0 and number2 % i == 0:
            hcf = i
            break
    print("The HCF of", number1, "and", number2, "is:", hcf)

# Question 34
def count_numbers():
    positive_count = 0
    negative_count = 0
    zero_count = 0
    while True:
        number = int(input("Enter a number (0 to quit): "))
        if number > 0:
            positive_count += 1
        elif number < 0:
            negative_count += 1
        else:
            zero_count += 1
            break
    print("Count of positive numbers:", positive_count)
    print("Count of negative numbers:", negative_count)
    print("Count of zeros:", zero_count)

# Question 35
def find_largest_smallest_numbers():
    largest = float('-inf')
    smallest = float('inf')
    while True:
        number = int(input("Enter a number (0 to quit): "))
        if number == 0:
            break
        if number > largest:
            largest = number
        if number < smallest:
            smallest = number
    print("Largest number:", largest)
    print("Smallest number:", smallest)

# Question 36
def find_armstrong_numbers():
    for number in range(0, 1000):
        temp = number
        sum_of_cubes = 0
        while temp > 0:
            digit = temp % 10
            sum_of_cubes += digit ** 3
            temp //= 10
        if number == sum_of_cubes:
            print(number)

# Question 37
def fibonacci_sequence():
    n = int(input("Enter the number of terms: "))
    fibonacci = [0, 1]
    for i in range(2, n):
        next_term = fibonacci[i - 1] + fibonacci[i - 2]
        fibonacci.append(next_term)
    print("Fibonacci Sequence:", fibonacci)

# Question 38
def calculate_series_sum():
    n = int(input("Enter the number of terms: "))
    total = 0
    for i in range(1, n + 1):
        total += i / (i * (i + 1))
    print("Sum of the series:", total)

# Question 39
def calculate_series_sum_alternating():
    n = int(input("Enter the number of terms: "))
    total = 0
    sign = 1
    for i in range(1, n + 1):
        term = sign / i
        total += term
        sign *= -1
    print("Sum of the series:", total)

# Question 40
def print_pattern1():
    for i in range(1, 6):
        for j in range(1, i + 1):
            print(j, end=" ")
        print()

# Question 41
def print_floyd_triangle():
    n = int(input("Enter the number of rows: "))
    num = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            print(num, end=" ")
            num += 1
        print()

# Question 42
import math

def compute_sine():
    x = float(input("Enter the value of x in radians: "))
    sine = math.sin(x)
    print("The sine of", x, "is:", sine)

# Question 43
import math

def compute_cosine():
    x = float(input("Enter the value of x in radians: "))
    cosine = math.cos(x)
    print("The cosine of", x, "is:", cosine)

# Question 44
import random

def guess_random_number():
    random_number = random.randint(1, 100)
    attempts = 0
    while True:
        guess = int(input("Guess the random number (1-100): "))
        attempts += 1
        if guess > random_number:
            print("Too high, try again.")
        elif guess < random_number:
            print("Too low, try again.")
        else:
            print("Congratulations! You guessed the random number", random_number, "in", attempts, "attempts.")
            break

# Question 45
def count_vowels():
    string = input("Enter a string: ")
    vowels = "aeiouAEIOU"
    count = 0
    for char in string:
        if char in vowels:
            count += 1
    print("Number of vowels:", count)

# Question 46
def count_characters():
    string = input("Enter a string: ")
    uppercase_count = 0
    lowercase_count = 0
    digit_count = 0
    whitespace_count = 0
    for char in string:
        if char.isupper():
            uppercase_count += 1
        elif char.islower():
            lowercase_count += 1
        elif char.isdigit():
            digit_count += 1
        elif char.isspace():
            whitespace_count += 1
    print("Number of uppercase letters:", uppercase_count)
    print("Number of lowercase letters:", lowercase_count)
    print("Number of digits:", digit_count)
    print("Number of whitespace characters:", whitespace_count)

# Question 47
def exchange_first_last():
    string = input("Enter a string: ")
    if len(string) < 2:
        print("String must contain at least two characters.")
        return
    new_string = string[-1] + string[1:-1] + string[0]
    print("New string:", new_string)

# Question 48
def reverse_string():
    string = input("Enter a string: ")
    reversed_string = string[::-1]
    print("Reversed string:", reversed_string)

# Question 49
def shift_string_left():
    string = input("Enter a string: ")
    shifted_string = string[1:] + string[0]
    print("Shifted string:", shifted_string)

# Question 50
def print_initials():
    name = input("Enter your name: ")
    initials = ""
    name_parts = name.split()
    for part in name_parts:
        initials += part[0].upper() + "."
    print("Initials:", initials)

# Question 51
def check_palindrome():
    string = input("Enter a string: ")
    reversed_string = string[::-1]
    if string == reversed_string:
        print("The string is a palindrome.")
    else:
        print("The string is not a palindrome.")

# Question 52
def print_pattern2():
    word = "SHIFT"
    length = len(word)
    for i in range(1, length + 1):
        for j in range(i, length + 1):
            print(word[j - i], end="")
        print()

# Question 53
def create_password():
    while True:
        password = input("Enter a password: ")
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
        elif not any(char.isupper() for char in password):
            print("Password must contain at least one uppercase letter.")
        elif not any(char.islower() for char in password):
            print("Password must contain at least one lowercase letter.")
        elif not any(char.isdigit() for char in password):
            print("Password must contain at least one numeric digit.")
        else:
            print("Password is valid.")
            break

# Question 54
def print_alternate_elements():
    elements = input("Enter elements of a list (space-separated): ").split()
    alternate_elements = elements[::2]
    print("Alternate elements:", alternate_elements)

# Question 55
def reverse_list():
    elements = input("Enter elements of a list (space-separated): ").split()
    reversed_list = []
    for i in range(len(elements) - 1, -1, -1):
        reversed_list.append(elements[i])
    print("Reversed list:", reversed_list)

# Question 56
def find_largest_number():
    elements = input("Enter elements of a list (space-separated): ").split()
    largest = elements[0]
    for element in elements:
        if element > largest:
            largest = element
    print("Largest number:", largest)

# Question 57
def rotate_list():
    elements = input("Enter elements of a list (space-separated): ").split()
    rotated_list = elements[1:] + elements[0:1]
    print("Rotated list:", rotated_list)

# Question 58
def delete_word():
    string = input("Enter a string: ")
    word = input("Enter a word to delete: ")
    new_string = string.replace(word, "")
    print("Modified string:", new_string)

# Question 59
import datetime

def format_date():
    date_str = input("Enter a date (mm/dd/yyyy): ")
    try:
        date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        formatted_date = date.strftime("%B %d, %Y")
        print("Formatted date:", formatted_date)
    except ValueError:
        print("Invalid date format.")

# Question 60
def sum_of_rows():
    m = int(input("Enter the number of rows: "))
    n = int(input("Enter the number of columns: "))
    matrix = []
    for i in range(m):
        row = input(f"Enter elements of row {i+1} (space-separated): ").split()
        row = [int(num) for num in row]
        matrix.append(row)
    row_sums = []
    for row in matrix:
        row_sum = sum(row)
        row_sums.append(row_sum)
    print("Sum of each row:", row_sums)


# Question 61
def find_max():
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    num3 = int(input("Enter the third number: "))

    max_num = max(num1, num2, num3)
    print("The largest number is:", max_num)



def is_vowel():
    vowels = ['a', 'e', 'i', 'o', 'u']
    string = input("Enter a string: ")
    count = 0
    for char in string:
        if char.lower() in vowels:
            count += 1
    print("Number of vowels in the string:", count)


# Question 63
def is_prime():
    def sub_is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    print("Prime numbers between 1 and 500:")
    for num in range(1, 501):
        if sub_is_prime(num):
            print(num)

# Question 64
def sum_of_cubes():
    lst = list(map(int, input("Enter the numbers (separated by spaces): ").split()))
    return sum([num ** 3 for num in lst])



# Question 65
def zero_ending():
    scores = list(map(int, input("Enter the scores (separated by spaces): ").split()))
    total = 0
    for score in scores:
        if str(score)[-1] == '0':
            total += score
    return total
def count_now():
    places = input("Enter the list of places (separated by spaces): ").split()
    count = 0
    for place in places:
        if len(place) > 5:
            count += 1
    return count
def display_list_elements():
    lst = input("Enter the list elements (separated by spaces): ").split()
    for element in lst:
        if isinstance(element, int) or isinstance(element, float):
            print(element * 3)
        else:
            print(element + '#')
def binary_search():
    values = list(map(int, input("Enter the sorted list of values (separated by spaces): ").split()))
    target = int(input("Enter the target value: "))
    start = 0
    end = len(values) - 1
    while start <= end:
        mid = (start + end) // 2
        if values[mid] == target:
            return mid
        elif values[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
    return -1

def half_and_half():
    lst = input("Enter the list elements (separated by spaces): ").split()
    length = len(lst)
    half = length // 2
    lst[:half], lst[half:] = lst[half:], lst[:half]
    return lst
def remove_duplicates():
    dictionary = eval(input("Enter the dictionary: "))  # Assuming the input format is valid dictionary syntax
    values = list(dictionary.values())
    if len(values) == len(set(values)):
        return dictionary
    else:
        return {}
def count_word_frequency():
    text = input("Enter the text: ")
    words = text.split()
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency

# Question 72
def phonebook_menu():
    phonebook = {}
    while True:
        print("Phonebook Menu:")
        print("1. Search a person's phone number")
        print("2. Add a new name and phone number")
        print("3. Change an existing phone number")
        print("4. Delete an existing name and phone number")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            name = input("Enter the name to search: ")
            if name in phonebook:
                print("Phone number:", phonebook[name])
            else:
                print("Name not found in the phonebook.")
        elif choice == '2':
            name = input("Enter the name to add: ")
            phone = input("Enter the phone number: ")
            phonebook[name] = phone
            print("Name and phone number added to the phonebook.")
        elif choice == '3':
            name = input("Enter the name to change the phone number: ")
            if name in phonebook:
                new_phone = input("Enter the new phone number: ")
                phonebook[name] = new_phone
                print("Phone number updated.")
            else:
                print("Name not found in the phonebook.")
        elif choice == '4':
            name = input("Enter the name to delete: ")
            if name in phonebook:
                del phonebook[name]
                print("Name and phone number deleted from the phonebook.")
            else:
                print("Name not found in the phonebook.")
        elif choice == '5':
            print("Exiting the phonebook.")
            break
        else:
            print("Invalid choice. Please enter a valid choice.")

# Question 73
def reverse_tuple():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    return tuple(reversed(t))

# Question 74
def multiply_tuple():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    product = 1
    for num in t:
        product *= num
    return product

# Question 75
def average_tuple_values():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    total = sum(t)
    return total / len(t)

# Question 76
def elementwise_sum():
    tuples = eval(input("Enter a list of tuples: "))  # Assuming the input format is a valid list of tuples syntax
    result = []
    length = len(tuples[0])
    for i in range(length):
        total = 0
        for tpl in tuples:
            total += tpl[i]
        result.append(total)
    return tuple(result)

# Question 77
def find_largest_smallest_tuple():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    return max(t), min(t)

# Question 78
def sum_even_odd_numbers_tuple():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    even_sum = 0
    odd_sum = 0
    for num in t:
        if num % 2 == 0:
            even_sum += num
        else:
            odd_sum += num
    return even_sum, odd_sum

# Question 79
def count_positive_negative_numbers_tuple():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    positive_count = 0
    negative_count = 0
    for num in t:
        if num > 0:
            positive_count += 1
        elif num < 0:
            negative_count += 1
    return positive_count, negative_count

# Question 80
def tuple_to_string():
    t = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    return "".join(str(t))

# 81. Program to Check whether the given item exists in a Tuple or not
def check_item_in_tuple():
    item = eval(input("Enter an item: "))  # Assuming the input format is a valid item syntax
    tuple_data = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    if item in tuple_data:
        print(f"{item} exists in the tuple.")
    else:
        print(f"{item} does not exist in the tuple.")

# 82. Write a Python program to Convert Tuple items to the dictionary
def convert_tuple_to_dict():
    tuple_data = eval(input("Enter a tuple: "))  # Assuming the input format is a valid tuple syntax
    dictionary = dict(enumerate(tuple_data))
    print(dictionary)

# 83. Write Python Program to Add Key-Value Pair to a Dictionary
def add_key_value_pair_to_dict():
    dictionary_data = eval(input("Enter a dictionary: "))  # Assuming the input format is a valid dictionary syntax
    key = input("Enter a key: ")
    value = input("Enter a value: ")
    dictionary_data[key] = value
    print(f"Key-value pair ({key}: {value}) added to the dictionary.")

# 84. Python Program to Create a Dictionary of keys and values are square of keys
def create_square_dict():
    n = int(input("Enter a number: "))
    square_dict = {key: key ** 2 for key in range(1, n + 1)}
    print(square_dict)

# 85. Python Program to Create Dictionary of Numbers 1 to n in (x, x*x) form
def create_num_dict():
    n = int(input("Enter a number: "))
    num_dict = {key: key * key for key in range(1, n + 1)}
    print(num_dict)

# 86. Python Program to Map two lists into a Dictionary
def map_lists_to_dict():
    keys = eval(input("Enter a list of keys: "))  # Assuming the input format is a valid list syntax
    values = eval(input("Enter a list of values: "))  # Assuming the input format is a valid list syntax
    mapped_dict = dict(zip(keys, values))
    print(mapped_dict)

# 87. Python Program to Concatenate Two Dictionaries
def concatenate_dicts():
    dict1 = eval(input("Enter the first dictionary: "))  # Assuming the input format is a valid dictionary syntax
    dict2 = eval(input("Enter the second dictionary: "))  # Assuming the input format is a valid dictionary syntax
    concatenated_dict = {**dict1, **dict2}
    print(concatenated_dict)

# 88. Python Program to Multiply All Items in a Dictionary
def multiply_dict_items():
    dictionary_data = eval(input("Enter a dictionary: "))  # Assuming the input format is a valid dictionary syntax
    multiplier = int(input("Enter a multiplier: "))
    multiplied_dict = {key: value * multiplier for key, value in dictionary_data.items()}
    print(multiplied_dict)

# 89. Python Program to Remove Given Key from a Dictionary
def remove_key_from_dict():
    dictionary_data = eval(input("Enter a dictionary: "))  # Assuming the input format is a valid dictionary syntax
    key = input("Enter a key: ")
    if key in dictionary_data:
        del dictionary_data[key]
        print(f"The key '{key}' has been removed from the dictionary.")
    else:
        print(f"The key '{key}' does not exist in the dictionary.")

# 90. Python Program to find Sum of Items in a Dictionary
def calculate_dict_sum():
    dictionary_data = eval(input("Enter a dictionary: "))  # Assuming the input format is a valid dictionary syntax
    total_sum = sum(dictionary_data.values())
    print(f"The sum of items in the dictionary is: {total_sum}")

# 91. Python program implement an Employee class
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display_employee_details(self):
        print(f"Name: {self.name}")
        print(f"Salary: {self.salary}")

# 92. Python program Setting values from the function using class
class MyClass:
    def __init__(self):
        self.value = None

    def set_value(self, value):
        self.value = value

    def display_value(self):
        print(f"The value is: {self.value}")

# 93. Python program Employee class using Constructor and Destructor
class Employee2:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __del__(self):
        print(f"Employee {self.name} has been deleted.")

# 94. Python program implement single inheritance
class ParentClass:
    def parent_method(self):
        print("This is a parent method.")

class ChildClass(ParentClass):
    def child_method(self):
        print("This is a child method.")

# 95. Python program to implement multiple inheritance
class ParentClass1:
    def method1(self):
        print("This is Parent Class 1 method.")

class ParentClass2:
    def method2(self):
        print("This is Parent Class 2 method.")

class ChildClass(ParentClass1, ParentClass2):
    def child_method(self):
        print("This is Child Class method.")

# 96. Python program to implement multilevel inheritance
class GrandparentClass:
    def grandparent_method(self):
        print("This is a grandparent method.")

class ParentClass(GrandparentClass):
    def parent_method(self):
        print("This is a parent method.")

class ChildClass(ParentClass):
    def child_method(self):
        print("This is a child method.")

# 97. Python program to implement hierarchical inheritance
class ParentClass:
    def parent_method(self):
        print("This is a parent method.")

class ChildClass1(ParentClass):
    def child1_method(self):
        print("This is Child Class 1 method.")

class ChildClass2(ParentClass):
    def child2_method(self):
        print("This is Child Class 2 method.")

# 98. Python program to count the number of objects created
class MyClass:
    objects_count = 0

    def __init__(self):
        MyClass.objects_count += 1

    @staticmethod
    def display_objects_count():
        print(f"The number of objects created is: {MyClass.objects_count}")

# 99. Python Program: Print student's marks list using class in Python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def display_student_details(self):
        print(f"Name: {self.name}")
        print(f"Marks: {self.marks}")

# 100. Python program to add objects using the '+' operator
class MyClass:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return MyClass(self.value + other.value)

    def display_value(self):
        print(f"The value is: {self.value}")

# 101. Python program to search student record using percentage
def search_student_record():
    student_records = {}
    num_students = int(input("Enter the number of students: "))

    for _ in range(num_students):
        student = input("Enter student name: ")
        marks = float(input("Enter student marks: "))
        student_records[student] = marks

    percentage = float(input("Enter the percentage: "))

    for student, marks in student_records.items():
        calculated_percentage = (marks / 100) * 100
        if calculated_percentage == percentage:
            print(f"Student with {percentage}% marks found: {student}")
            return

    print(f"No student found with {percentage}% marks.")


# 102. Python program to illustrate Matrix Addition using Class
class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def display_matrix(self):
        for row in self.matrix:
            print(row)

    def __add__(self, other):
        result = []
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix[0])):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            result.append(row)
        return Matrix(result)

