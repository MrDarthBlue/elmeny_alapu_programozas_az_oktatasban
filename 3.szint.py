from controller import Robot 

timeStep = 32
max_velocity = 6.28
alap_sebesseg = 3.0
robot = Robot()

wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor")
wheel1.setPosition(float("inf"))       
wheel2.setPosition(float("inf"))
color_sensor = robot.getDevice("color")
color_sensor.enable(timeStep)

color_sensor_values = [0, 0, 0]

def get_colour_sensor_value():
    image = color_sensor.getImage()
    color_sensor_values[0] = color_sensor.imageGetRed(image, 1, 0, 0)
    color_sensor_values[1] = color_sensor.imageGetGreen(image, 1, 0, 0)
    color_sensor_values[2] = color_sensor.imageGetBlue(image, 1, 0, 0)

def is_black():
    target = 53
    tolerance = 5  
    return (abs(color_sensor_values[0] - target) < tolerance and 
            abs(color_sensor_values[1] - target) < tolerance and 
            abs(color_sensor_values[2] - target) < tolerance)

def is_blue():
    target = 81
    target2 = 81
    target3 = 255
    tolerance = 5  
    return (abs(color_sensor_values[0] - target) < tolerance and 
            abs(color_sensor_values[1] - target2) < tolerance and 
            abs(color_sensor_values[2] - target3) < tolerance)

def turn_180():
    turn_time = 2.1  
    wheel1.setVelocity(2.0)
    wheel2.setVelocity(-2.0)
    
    start_time = robot.getTime()
    while robot.step(timeStep) != -1:
        if robot.getTime() - start_time >= turn_time:
            break

# Fő vezérlési ciklus
while robot.step(timeStep) != -1:
    
    get_colour_sensor_value()

    if is_black():
        print("Fekete csapda! 180 fokos fordulás...")
        turn_180()
        
    elif is_blue():
        print("Kék zóna! Sebesség növelése maximumra...")
        wheel1.setVelocity(max_velocity)
        wheel2.setVelocity(max_velocity)
        
    else:
        wheel1.setVelocity(alap_sebesseg)
        wheel2.setVelocity(alap_sebesseg)