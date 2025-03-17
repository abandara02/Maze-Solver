from Freenove_Micro_Rover import *
Rover = Micro_Rover()
display.show(Image.HAPPY)
counter = 0
start = (0, 0)
end = (4, 4)


def Move_forward():
    flag = True
    while flag:
        sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()

        while sensor_value != 7:
            Rover.all_led_show(0, 0, 255, 0)
            Rover.motor(85, 110)
            display.show(Image.ARROW_N)
            sleep(50)
            sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()

            if sensor_value == 1:
                Rover.motor(110,55)
                sleep(200)
            if sensor_value == 4:
                Rover.motor(50, 110)
                sleep(200)


        while sensor_value == 7:
            Rover.motor(85, 110)
            sleep(500)
            display.show(Image.ARROW_S)
            sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()


        if sensor_value != 7:
            Rover.motor(0, 0)
            flag = False

    display.show(Image.BUTTERFLY)
    Rover.motor(0, 0)


def Rotate_right():
    sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()
    Rover.motor(85, -85)
    sleep(400)
    while sensor_value not in (4, 6):
        display.show(Image.ARROW_W)
        sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()
        Rover.motor(85, -85)
    display.show(Image.BUTTERFLY)
    Rover.motor(0, 0)

def Rotate_left():
    sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()

    Rover.motor(-100, 100)
    sleep(400)
    while sensor_value not in (1, 3):
        display.show(Image.ARROW_E)
        sensor_value = (pin14.read_digital() << 2) | (pin15.read_digital() << 1) | pin16.read_digital()
        Rover.motor(-100, 100)
    display.show(Image.BUTTERFLY)
    Rover.motor(0, 0)

def Stop():
    Rover.all_led_show(0,0,0,0)
    Rover.motor(0, 0)

def show_the_path(path):
    display.clear()
    for point in path:
        display.set_pixel(point[0], point[1], 9)
"""
def path_runner(path):
    directions = [(1,0), (0, 1), (-1, 0), (0, -1)]
    pos_direction = (1, 0)
    for i in range(1, len(path) - 1):
        if path[i] == (4, 4):
            Stop()
            break
        else:
            display.show(Image.SMILE)
            pos = path[i - 1]
            Move_forward()


            for j in range(len(directions)):
                if (pos[0] + directions[j][0] == path[i][0]) and (pos[1] + directions[j][1] == path[i][1]):
                    ind = directions.index(pos_direction)
                    if (j - ind) in (1, -3):
                        Rotate_left()
                        sleep(500)
                        pos_direction = directions[j]
                        break
                    else:
                        Rotate_right()
                        sleep(500)
                        pos_direction = directions[j]
                        break

            sleep(500)
"""

def navigate_path(path):
    # Initial orientation is facing right (east)
    current_direction = 'E'

    # Map to get the direction after rotation
    right_turn = {'E': 'S', 'S': 'W', 'W': 'N', 'N': 'E'}
    left_turn = {'E': 'N', 'N': 'W', 'W': 'S', 'S': 'E'}

    # Define moves for each direction
    moves = {
        'E': (1, 0),
        'W': (-1, 0),
        'N': (0, -1),
        'S': (0, 1)
    }
    Move_forward()

    # Function to determine required rotation
    def determine_rotation(current, next):
        if current == 'E':
            if next == 'N':
                return 'left'
            elif next == 'S':
                return 'right'
        elif current == 'W':
            if next == 'N':
                return 'right'
            elif next == 'S':
                return 'left'
        elif current == 'N':
            if next == 'E':
                return 'right'
            elif next == 'W':
                return 'left'
        elif current == 'S':
            if next == 'E':
                return 'left'
            elif next == 'W':
                return 'right'
        return 'none'

    for i in range(len(path) - 1):
        current_position = path[i]
        next_position = path[i + 1]

        # Determine direction needed to move to the next position
        move = (next_position[0] - current_position[0], next_position[1] - current_position[1])

        for direction, step in moves.items():
            if move == step:
                required_direction = direction
                break

        # Determine rotation needed
        while current_direction != required_direction:
            rotation = determine_rotation(current_direction, required_direction)
            if rotation == 'right':
                Rotate_right()
                sleep(1000)
                current_direction = right_turn[current_direction]
            elif rotation == 'left':
                Rotate_left()
                sleep(1000)
                current_direction = left_turn[current_direction]

        # Move to the next position
        Move_forward()
        sleep(1000)

# Example path


def bfs_no_deque(maze, start, end):
    queue = [(start, [start])]
    visited = set([start])

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current, path = queue.pop(0)

        if current == end:
            return path

        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]
            next_position = (next_row, next_col)

            if (0 <= next_row < len(maze) and
                0 <= next_col < len(maze[0]) and
                maze[next_row][next_col] != 'X' and
                next_position not in visited):

                visited.add(next_position)
                queue.append((next_position, path + [next_position]))

    return "No path found"

maze = [['S', 'O', 'O', 'O', 'X'], ['O', 'X', 'O', 'O', 'O'], ['O', 'O', 'O', 'X', 'X'], ['O', 'O', 'O', 'O', 'X'], ['O', 'O', 'X', 'O', 'E']]
start = (0, 0)
end = (4, 4)

path = bfs_no_deque(maze, start, end)

show_the_path(path)
sleep(3000)

navigate_path(path)


def Test():

    Move_forward()
    Rotate_right()
    Move_forward()
    Rotate_left()
    Move_forward()


def Test_path():
    Move_forward()
    sleep(500)
    Rotate_right()
    sleep(500)
    Move_forward()
    sleep(500)
    Rotate_left()
    sleep(500)
    Move_forward()
    sleep(500)
    Move_forward()
    sleep(500)
    Move_forward()

    sleep(500)
    Rotate_right()
    sleep(500)
    Move_forward()
    sleep(500)
    Move_forward()
    sleep(500)
    Move_forward()
    sleep(500)