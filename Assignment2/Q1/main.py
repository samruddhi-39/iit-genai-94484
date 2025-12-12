# main.py
from math_utils import area_circle, area_rectangle, area_triangle

r = float(input("Enter radius of circle: "))
l = float(input("Enter length of rectangle: "))
w = float(input("Enter width of rectangle: "))
b = float(input("Enter base of triangle: "))
h = float(input("Enter height of triangle: "))

print("Circle area:", area_circle(r))
print("Rectangle area:", area_rectangle(l, w))
print("Triangle area:", area_triangle(b, h))
