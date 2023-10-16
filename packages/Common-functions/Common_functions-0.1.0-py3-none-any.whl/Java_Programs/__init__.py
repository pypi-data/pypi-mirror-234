import subprocess
import os

root=os.path.dirname(__file__)
os.chdir(root)

def factorial_of_numbers():
    numbers = input("Enter the number: ")
    result = subprocess.run(["java", "FactorialOfNumbers"] + numbers.split(), capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def prime_series():
    n = int(input("Enter the value of n: "))
    result = subprocess.run(["java", "PrimeSeries", str(n)], capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def rhombus_pattern():
    subprocess.run(["java", "RhombusPattern"])


def string_operations():
    subprocess.run(["java", "StringOperations"])


def average_of_numbers():
    numbers = input("Enter the numbers (separated by spaces): ")
    result = subprocess.run(["java", "AverageOfNumbers"] + numbers.split(), capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def distance_between_points():
    points = input("Enter the points (x1 y1 x2 y2): ")
    result = subprocess.run(["java", "DistanceBetweenPoints"] + points.split(), capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def average_marks():
    marks = input("Enter the marks (separated by spaces): ")
    result = subprocess.run(["java", "AverageMarks"] + marks.split(), capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def sum_of_numbers():
    numbers = input("Enter the numbers (separated by spaces): ")
    result = subprocess.run(["java", "SumOfNumbers"] + numbers.split(), capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)


def linear_search():
    numbers = input("Enter the numbers (separated by spaces): ")
    target = input("Enter the target number: ")
    result = subprocess.run(["java", "LinearSearch"] + numbers.split(), capture_output=True, text=True, input=target)
    print(result.stdout if result.stdout else result.stderr)


def mouse_events():
    subprocess.run(["appletviewer", "applet.html"])
