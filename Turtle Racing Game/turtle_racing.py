import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.title("Turtle Race")
screen.bgcolor("white")

# Colors for turtles
colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan", "brown", "black"]

# Ask user for the number of turtles
num_turtles = 0
while num_turtles < 3 or num_turtles > 10:
    num_turtles = int(screen.textinput("Number of Turtles", "Enter the number of turtles (3-10):"))

# Setup turtles
turtles = []
start_x = -200
start_y = 200
spacing = 400 // (num_turtles - 1)
for i in range(num_turtles):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(colors[i])
    t.penup()
    t.goto(start_x, start_y - i * spacing)
    turtles.append(t)

# Draw finish line
finish_line = turtle.Turtle()
finish_line.penup()
finish_line.goto(200, start_y + 20)
finish_line.pendown()
finish_line.right(90)
finish_line.forward(400)
finish_line.hideturtle()

# Random race distance
race_distance = random.randint(100, 300)

# Race logic
is_race_on = False

def start_race():
    global is_race_on
    is_race_on = True

screen.listen()
screen.onkey(start_race, "space")

# Display instructions
instruction_turtle = turtle.Turtle()
instruction_turtle.hideturtle()
instruction_turtle.penup()
instruction_turtle.goto(0, start_y + 50)
instruction_turtle.write("Press SPACE to start the race!", align="center", font=("Arial", 16, "bold"))

# Start race when space key is pressed
while not is_race_on:
    screen.update()

# Clear instructions
instruction_turtle.clear()

# Run the race
while is_race_on:
    for t in turtles:
        t.forward(random.randint(1, 10))
        if t.xcor() >= 200:
            is_race_on = False
            winner_color = t.color()[0]
            break

# Display the winner
winner_turtle = turtle.Turtle()
winner_turtle.hideturtle()
winner_turtle.penup()
winner_turtle.goto(0, start_y + 50)
winner_turtle.write(f"The winner is the {winner_color} turtle!", align="center", font=("Arial", 16, "bold"))

# Display positions throughout the race (every 10 iterations)
def display_positions():
    positions = {t.color()[0]: t.xcor() for t in turtles}
    sorted_positions = sorted(positions.items(), key=lambda item: item[1], reverse=True)
    position_turtle = turtle.Turtle()
    position_turtle.hideturtle()
    position_turtle.penup()
    position_turtle.goto(-250, start_y + 20)
    position_turtle.clear()
    for idx, (color, pos) in enumerate(sorted_positions):
        position_turtle.write(f"{idx + 1}. {color} turtle", align="left", font=("Arial", 10, "normal"))
        position_turtle.goto(-250, position_turtle.ycor() - 20)
    screen.ontimer(display_positions, 500)

display_positions()
screen.mainloop()
