"""Wall_Follow_controller controller."""

from controller import Robot

def Wall_Follow(robot):
    timestep = int(robot.getBasicTimeStep())
    max_speed = 6.28

    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    
    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)

    prox_sensors = []
    for i in range(8):
        sensor = robot.getDevice('ps' + str(i))
        sensor.enable(timestep)
        prox_sensors.append(sensor)

    spin_counter = 0  

    # Main loop
    while robot.step(timestep) != -1:
        sensor_values = [sensor.getValue() for sensor in prox_sensors]
        for i, val in enumerate(sensor_values):
            print(f"Sensor {i}: {val:.2f}")

        front_wall = sensor_values[7] > 100
        left_wall = sensor_values[5] > 100
        left_corner = sensor_values[6] > 100

        left_speed = max_speed
        right_speed = max_speed

        if front_wall and left_wall:
            spin_counter += 1
            print(f"Spinning... Counter: {spin_counter}")
            if spin_counter > 10:
                left_speed = -max_speed / 2
                right_speed = -max_speed / 2
            else:
                left_speed = max_speed
                right_speed = -max_speed
        else:
            spin_counter = 0  

            if front_wall:
                left_speed = max_speed
                right_speed = -max_speed / 4

            elif left_corner:
                left_speed = max_speed
                right_speed = max_speed / 8

            elif left_wall:
                left_speed = max_speed
                right_speed = max_speed

            else:
                left_speed = max_speed / 4
                right_speed = max_speed

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

if __name__ == "__main__":
    my_robot = Robot()
    Wall_Follow(my_robot)
