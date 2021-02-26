def get_robot_name():
    """get robot name"""
    robot_name = input("What do you want to name your robot? ").upper()
    print(robot_name + ": " + "Hello kiddo!")
    return robot_name


def robot_shut_down(robot_name):
    """shut down robot"""

    print(str(robot_name)+': Shutting down..')


def output_help_list(list_commands, help_commands):
    """returns a string that will output when user inputs help command"""
    output = 'I can understand these commands:\n'
    for i in range(7):
        output = output + " " + list_commands[i] + " - " + help_commands[i] + "\n"
    return output


def print_help_list(list_commands, help_commands):
    """print help list"""
    print("I can understand these commands:")
    #change range if commands are added
    help_output = """OFF  - Shut down robot
HELP - provide information about commands"""
    print(help_output)


def change_value_in_tuple(tuple_obj, index, value):
    """Changes value in tuple at specified index"""
    
    list_obj = list(tuple_obj)
    list_obj[index] = value
    tuple_obj = tuple(list_obj)
    return tuple_obj


def in_limit(axis, index):
    """Check to see if coordinates are in the limit"""
    
    if (axis > 100 or axis < -100) and index == 0:
        return False
    if (axis > 200 or axis < -200) and index == 1:
        return False
    return True


def robot_direction(command, direction):
    """Sets direction robot faces after move"""
    index = 0
    coords = ["forward", "back", "right", "left"]
    if command == "right" or command == "left":
        if command == "right":
            if direction == "forward":
                index += 2
            if direction == "back":
                index += 3
            if direction == "right":
                index += 1
            if direction == "left":
                index == 0
        elif command == "left":
            if direction == "forward":
                index += 3
            if direction == "back":
                index += 2
            if direction == "right":
                index == 0
            if direction == "left":
                index += 1
        return coords[index]
    return direction


def get_move(command, list_commands):
    """checks if input is in command list and returns move"""
    command_list = command.split()
    move = command_list[0] 
    if move in list_commands:
        return move


def get_distance(command):
    """Returns distance from input"""
    distance = ''
    command_list = command.split()
    if len(command_list)  == 1:
        return 'no_steps'
    if len(command_list) == 2:
        distance = command_list[1]
        return distance
       
        
def get_coordinates(command, position, distance, direction):
    """changes coordinates when robot moves"""
    if (direction == 'right' or direction == 'left'):
        index = 0
    else:
        index = 1

    axis = position[index]
    command_list = command.split()
    action = command_list[0]
    if action == "forward" and (direction != 'left' and direction != 'back'):
        axis += int(distance)
    elif (action == "back" and direction != 'left') or (action == 'forward' and (direction == 'back' or direction == 'left')):
        axis -= int(distance)
    elif action == 'back' and direction == 'left':
        axis += int(distance)
        
    if in_limit(axis, index):
        position = change_value_in_tuple(position, index, axis)
    return position


def print_sprint_move(is_valid, robot_name, position, distance):
    """Print output after robot performs sprint move"""
    
    if (is_valid):
        for i in range(0, int(distance)):
            print_steps = int(distance) - i
            print(' > '+ str(robot_name) +' moved forward by '+ str(print_steps) +' steps.')
    

def calculate_sprint_taken_steps(distance, robot_name):
    """Calculate # steps taken by robot when sprint move is performed"""
    
    if (distance != 0):
        return distance + calculate_sprint_taken_steps(distance - 1, robot_name)
    else:
        return distance


def sprint(distance, robot_info):
    """Perform sprint move"""

    robot_name = robot_info[0]
    position = robot_info[1]
    direction = robot_info[2]
    
    temp_position = position
    taken_steps = calculate_sprint_taken_steps(int(distance), robot_name)
    position = get_coordinates('forward', position, taken_steps, direction)
    print_sprint_move(temp_position != position, robot_name, position, distance)
    robot_info = (robot_name, position, direction)
    return robot_info


def check_valid_input(command, steps):
    """Check if (valid) command has correct step input"""
    
    command_and_steps = (command, steps)
    if (command == 'back' or command == 'forward' or command == 'sprint') and steps == 'no_steps':
        command_and_steps = ('not_option', 'no_steps')
    elif (command == 'right' or command == 'left') and steps != 'no_steps':
        command_and_steps = ('not_option', 'no_steps')
    return command_and_steps


def choose_command(command, list_commands):
    """Returns tuple with command and # of steps; ONLY if it's a valid move"""
    
    command_input = get_move(command, list_commands)
    for item in list_commands:
        if item.lower() == command_input:
            command_and_steps = check_valid_input(command_input, get_distance(command.lower().strip()))
            return command_and_steps
    return ('not_option', 'no_steps')


def move_robot(command, distance, robot_info):
    """Moves robot"""

    name = robot_info[0]
    position = robot_info[1]
    direction = robot_info[2]
    
    prev_position = position
    position = get_coordinates(command, position, distance, direction)
    #invalid move
    if (position == prev_position) and (command != 'left') and (command != 'right') and (int(distance) != 0):
        print(str(name) + ': Sorry, I cannot go outside my safe zone.')
        robot_info = (name, position, direction) 
    #valid move
    else:
        #forward/backwards
        if command != 'left' and command != 'right':
            print(' > ' + str(name) + ' moved '+ str(command) +' by ' + str(distance) + ' steps.')
        #left/right
        else:
            print(' > ' + name + ' turned '+ command + '.')
        direction = robot_direction(command, direction)
        robot_info = (name, position, direction)
    return robot_info


def do_command(tuple_command_and_steps, list_commands, help_commands, robot_info):
    """Executes user's command; returns whether robot should turn off"""
    
    command = tuple_command_and_steps[0]
    distance = tuple_command_and_steps[1]
    robot_name = robot_info[0]
    
    if command == 'help':
        print_help_list(list_commands, help_commands)
    else:
        if command == 'forward':
            robot_info = move_robot(command, distance, robot_info)
        elif command == 'back':
            robot_info = move_robot(command, distance, robot_info)
        elif command == 'right':
            robot_info = move_robot(command, distance, robot_info)
        elif command == 'left':
            robot_info = move_robot(command, distance, robot_info)
        elif command == 'sprint':
            robot_info = sprint(distance, robot_info)
        #print position after robot moved
        position = robot_info[1]
        print(' > ' + str(robot_name) + ' now at position ' + '(' + str(position[0]) + ',' + str(position[1]) + ').')
    
    return robot_info

    
def robot_start():
    """This is the entry function, do not change"""
    #change range in help_list if commands are added
    help_commands = ["Shut down robot","provide information about commands","move robot forward","move robot backwards","turns robot right","turns robot left","gives robot a short burst of speed extra distance"]
    list_commands = ["off","help","forward","back","right","left","sprint"]
    robot_name = get_robot_name()
    position = (0,0)
    direction = 'forward'
    robot_info = (robot_name, position, direction)
    

    while True:
        print(robot_name + ': ', end = '')
        command = input('What must I do next? ')
        command_lower = command.lower()
        while choose_command(command_lower, list_commands)[0] == 'not_option':
            print(str(robot_name) + ': Sorry, I did not understand '+'\'' + str(command) + '\'.')
            command = input(str(robot_name)+': What must I do next? ')
            command_lower = command.lower()
        if  command.lower().strip() == 'off':
            robot_shut_down(robot_name)
            break
        command_and_steps = choose_command(command_lower, list_commands)
        robot_info = do_command(command_and_steps, list_commands, help_commands, robot_info)
        

if __name__ == "__main__":
    robot_start()