## Left-Hand Wall Following
from controller import Robot

def run_robot(robot):
    timestep = int(robot.getBasicTimeStep())
    max_speed = 6.28

    # Initialize motors
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    # Initialize proximity sensors
    prox_sensors = []
    for i in range(8):
    # PS0 PS1 PS2 ....
        sensor = robot.getDevice('ps' + str(i))
        sensor.enable(timestep)
        prox_sensors.append(sensor)

    # Main control loop
    while robot.step(timestep) != -1:
        sensor_values = [sensor.getValue() for sensor in prox_sensors]

        # Debug print
        for i, val in enumerate(sensor_values):
            print(f"Sensor {i}: {val:.2f}")

        # Wall detection
        front_wall = sensor_values[7] > 80
        left_wall = sensor_values[5] > 80
        left_corner = sensor_values[6] > 80

        # Initialize speeds
        left_speed = max_speed
        right_speed = max_speed

        if front_wall and left_wall:
            print("Corner detected: turn right in place")
            left_speed = max_speed
            right_speed = -max_speed
        elif front_wall:
            print("Wall ahead: turn right")
            left_speed = max_speed
            right_speed = -max_speed / 2
        elif left_corner:
            print("Too close to left wall: adjust right")
            left_speed = max_speed
            right_speed = max_speed / 4
        elif left_wall:
            print("Wall on left: go forward")
            left_speed = max_speed
            right_speed = max_speed
        else:
            print("Turn left to find wall")
            left_speed = max_speed / 4
            right_speed = max_speed

        # Apply speeds
        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)
