
import turtle
import math

def draw_segment(t, length, depth):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_segment(t, length, depth - 1)
        t.right(60)   # inward
        draw_segment(t, length, depth - 1)
        t.left(120)   # inward
        draw_segment(t, length, depth - 1)
        t.right(60)   # inward
        draw_segment(t, length, depth - 1)

def draw_polygon(t, sides, length, depth):
    angle = 360 / sides
    for _ in range(sides):
        draw_segment(t, length, depth)
        t.right(angle)

def main():
    # input
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    screen = turtle.Screen()
    screen.setup(width=1000, height=800)   # bigger window
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)

    radius = length / (2 * math.sin(math.pi / sides))

    t.penup()
    t.setheading(0)
    t.goto(-length/2, -radius/2)   
    t.pendown()


    draw_polygon(t, sides, length, depth)

    t.hideturtle()
    screen.mainloop()

if __name__ == "__main__":
    main()
