from controller import Robot

timeStep = 32
robot = Robot()

wheel1 = robot.getDevice("wheel1 motor")
wheel2 = robot.getDevice("wheel2 motor")
wheel1.setPosition(float("inf"))       
wheel2.setPosition(float("inf"))

bal_sebesseg = 4.0
jobb_sebesseg = 4.0

print("A robot elindul, majd 3 másodperc múlva megáll.")

# Fő vezérlési ciklus
while robot.step(timeStep) != -1:
    
    if robot.getTime() < 3.0:
        wheel1.setVelocity(bal_sebesseg)
        wheel2.setVelocity(jobb_sebesseg)
        
    else:
        wheel1.setVelocity(0.0)
        wheel2.setVelocity(0.0)
        