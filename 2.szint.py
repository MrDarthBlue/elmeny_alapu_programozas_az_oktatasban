from controller import Robot 
import random

timeStep = 32
robot = Robot()

wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor")
wheel1.setPosition(float("inf"))       
wheel2.setPosition(float("inf"))

distance_sensor = robot.getDevice("distance_sensor3")
distance_sensor2 = robot.getDevice("distance_sensor4")
distance_sensor.enable(timeStep)
distance_sensor2.enable(timeStep)

def turn():
    turn_time = 1.09 
    wheel1.setVelocity(2)
    wheel2.setVelocity(-2)
    
    start_time = robot.getTime()
    while robot.step(timeStep) != -1:
        if robot.getTime() - start_time >= turn_time:
            break

print("Reaktív akadálykerülés elindult.")

# Fő vezérlési ciklus
while robot.step(timeStep) != -1:
    
    front_dist1 = distance_sensor.getValue() * 100
    front_dist2 = distance_sensor2.getValue() * 100
    
    # A két szenzor közül kiválasztjuk azt, amelyik közelebb látja a falat
    front_distance = min(front_dist1, front_dist2)
    
    if front_distance < 7.0:
        print("Fal a közelben! Elkerülő manőver...")
        turn()
        
    else:
        wheel1.setVelocity(3.0)
        wheel2.setVelocity(3.0)
        