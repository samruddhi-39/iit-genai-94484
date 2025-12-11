import arithmetic
import geometry as geo

print("Hello World!")
a=int(input("enter a: "))
b=int(input("enter b: "))
arithmetic.add(a,b)
arithmetic.substract(a,b)

len=int(input("enter length: "))
br=int(input("enter br: "))

geo.calc_rect_area(len,br)
geo.calc_rect_peri(len,br)