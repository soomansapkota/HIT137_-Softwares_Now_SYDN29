# Assignment 2 Q3
#Group Name : SYDN 29

#Group Members :
# 1. Suman Sapkota - S396224
# 2. Bibek Pandit - S395718
# 3. Asha Devi - S394864
# 4. Sulav Subedi - S396117

import turtle

def draw_koch_edge(t, length, depth):
    """Recursive function to draw one edge with Koch-like indentation pointing inward."""
    if depth == 0:
        t.forward(length)
    else:
        length /= 3.0
        draw_koch_edge(t, length, depth - 1)

        # Inward indentation (flipped directions)
        t.right(60)
        draw_koch_edge(t, length, depth - 1)
        t.left(120)
        draw_koch_edge(t, length, depth - 1)
        t.right(60)

        draw_koch_edge(t, length, depth - 1)

def draw_polygon(t, sides, length, depth):
    """Draw a polygon with Koch-like recursive inward edges."""
    angle = 360 / sides
    for _ in range(sides):
        draw_koch_edge(t, length, depth)
        t.right(angle)

def main():
    # User input
    sides = int(input("Enter the number of sides: "))
    length = float(input("Enter the side length: "))
    depth = int(input("Enter the recursion depth: "))

    # Setup turtle
    screen = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)  # Fastest

    # Move turtle so drawing starts closer to center
    t.penup()
    t.goto(-length/2, length/3)
    t.pendown()

    # Draw pattern
    draw_polygon(t, sides, length, depth)

    # Finish
    t.hideturtle()
    screen.mainloop()

if __name__ == "__main__":
    main()

