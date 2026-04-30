from controller import Robot 
import random

timeStep = 32
robot = Robot()

wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor")
wheel1.setPosition(float("inf"))       
wheel2.setPosition(float("inf"))

color_sensor = robot.getDevice("color")
distance_sensor = robot.getDevice("distance_sensor3")
distance_sensor2 = robot.getDevice("distance_sensor4")

color_sensor.enable(timeStep)
distance_sensor.enable(timeStep)
distance_sensor2.enable(timeStep)

color_sensor_values = [0, 0, 0]

movement_counter = 0
movement_phase = 0  
phase_duration = 20  

# SZÍNFELISMERŐ FÜGGVÉNYEK

def get_colour_sensor_value():
    image = color_sensor.getImage()
    color_sensor_values[0] = color_sensor.imageGetRed(image, 1, 0, 0)
    color_sensor_values[1] = color_sensor.imageGetGreen(image, 1, 0, 0)
    color_sensor_values[2] = color_sensor.imageGetBlue(image, 1, 0, 0)

def is_black():
    target = 53; tolerance = 5  
    return (abs(color_sensor_values[0] - target) < tolerance and 
            abs(color_sensor_values[1] - target) < tolerance and 
            abs(color_sensor_values[2] - target) < tolerance)

def is_blue():
    target = 81; target2 = 81; target3 = 255; tolerance = 5  
    return (abs(color_sensor_values[0] - target) < tolerance and 
            abs(color_sensor_values[1] - target2) < tolerance and 
            abs(color_sensor_values[2] - target3) < tolerance)

def is_purple():
    target_r = 177; target_g = 81; target_b = 246; tolerance = 5  
    return (abs(color_sensor_values[0] - target_r) < tolerance and 
            abs(color_sensor_values[1] - target_g) < tolerance and 
            abs(color_sensor_values[2] - target_b) < tolerance)

def is_yellow():
    target_r = 236; target_g = 208; target_b = 128; tolerance = 5  
    return (abs(color_sensor_values[0] - target_r) < tolerance and 
            abs(color_sensor_values[1] - target_g) < tolerance and 
            abs(color_sensor_values[2] - target_b) < tolerance)

def is_white():
    tolerance = 25
    return (abs(color_sensor_values[0] - 228) < tolerance and
            abs(color_sensor_values[1] - 228) < tolerance and
            abs(color_sensor_values[2] - 228) < tolerance)

def is_green():
    target_r = 43; target_g = 254; target_b = 43; tolerance = 5  
    return (abs(color_sensor_values[0] - target_r) < tolerance and 
            abs(color_sensor_values[1] - target_g) < tolerance and 
            abs(color_sensor_values[2] - target_b) < tolerance)

def is_grey():
    target_r = 165; target_g = 169; target_b = 174; tolerance = 5
    return (abs(color_sensor_values[0] - target_r) < tolerance and 
            abs(color_sensor_values[1] - target_g) < tolerance and 
            abs(color_sensor_values[2] - target_b) < tolerance)

def is_darkgrey():
    target_r = 144; target_g = 144; target_b = 145; tolerance = 5
    return (abs(color_sensor_values[0] - target_r) < tolerance and 
            abs(color_sensor_values[1] - target_g) < tolerance and 
            abs(color_sensor_values[2] - target_b) < tolerance)


# MOZGÁSI FÜGGVÉNYEK

def forduljon_el():
    turn_time = 1.09 
    wheel1.setVelocity(2)
    wheel2.setVelocity(-2)
    start_time = robot.getTime() 
    while robot.step(timeStep) != -1: 
        if robot.getTime() - start_time >= turn_time:
            break

def spiral_movement():
    global movement_counter, movement_phase, phase_duration
    base_speed = 4  
    movement_counter += 1
    if movement_counter >= phase_duration:
        movement_phase = 1 - movement_phase
        movement_counter = 0
        phase_duration = random.randint(40, 60)  
    
    if movement_phase == 0:
        wheel1.setVelocity(base_speed - 0.2)
        wheel2.setVelocity(base_speed + 0.2)
    else:
        wheel1.setVelocity(base_speed + 0.2)
        wheel2.setVelocity(base_speed - 0.2)

# FŐ VEZÉRLÉSI CIKLUS

while robot.step(timeStep) != -1:
    get_colour_sensor_value()
    
    front_dist1 = distance_sensor.getValue() * 100
    front_dist2 = distance_sensor2.getValue() * 100
    front_distance = min(front_dist1, front_dist2)
    
    if front_distance < 7.0 or is_black():
        forduljon_el()
        movement_counter = 0  

    elif is_blue() or is_purple() or is_yellow() or is_green() or is_grey() or is_darkgrey():
        celszin_neve = "Ismeretlen"
        if is_blue(): celszin_neve = "Kék"
        elif is_purple(): celszin_neve = "Lila"
        elif is_yellow(): celszin_neve = "Sárga"
        elif is_green(): celszin_neve = "Zöld"
        elif is_grey(): celszin_neve = "Szürke"
        elif is_darkgrey(): celszin_neve = "Sötét szürke"

        print(f"\n---> CÉLSZÍN TALÁLVA! Észlelt szín: {celszin_neve} <---\n")
        
        wheel1.setVelocity(3.0)
        wheel2.setVelocity(3.0)
        
        # BELSŐ CIKLUS a színes területen
        while robot.step(timeStep) != -1:
            get_colour_sensor_value()
            
            belso_dist1 = distance_sensor.getValue() * 100
            belso_dist2 = distance_sensor2.getValue() * 100
            belso_distance = min(belso_dist1, belso_dist2)
            
            if belso_distance < 7.0 or is_black():
                forduljon_el()
                wheel1.setVelocity(3.0)
                wheel2.setVelocity(3.0)
        
            if is_white():
                break  
    
    else:
        spiral_movement()