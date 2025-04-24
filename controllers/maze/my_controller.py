from controller import Robot

def run_robot(robot):
    timestep = int(robot.getBasicTimeStep())
    max_speed = 2.5

    left_motor = robot.getMotor('left wheel robot')
    right_motor = robot.getMotor('right wheel robot')

    left_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setPosition(float('inf'))
    right_motor.setVelocity(0.0)

    prox_sensors = []
    for ind in range(8):
        sensor_name = 'ps' + str(ind)
        prox_sensors.append(robot.getDistanceSensor(sensor_name))
        prox_sensors[ind].enable(timestep)

    while robot.step(timestep) != -1:
        sensor_values = [sensor.getValue() for sensor in prox_sensors]
        print("Sensor readings:", sensor_values)

        front_wall = sensor_values[7] > 60 or sensor_values[0] > 60
        right_wall = sensor_values[2] > 60
        left_wall = sensor_values[5] > 60
        left_corner = sensor_values[6] > 60

        left_speed = max_speed
        right_speed = max_speed

        if front_wall:
            print("Obstacle ahead, rotating right")
            left_speed = max_speed
            right_speed = -max_speed
            robot.step(timestep * 10)  # Increase delay for full rotation
        elif right_wall and not left_wall:
            print("Adjusting left to follow right-hand wall")
            left_speed = max_speed / 2
            right_speed = max_speed
        elif left_corner:
            print("Too close to the wall, shifting right")
            left_speed = max_speed
            right_speed = max_speed / 4
        else:
            print("Moving forward")
            left_speed = max_speed
            right_speed = max_speed

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)

if __name__ == "__main__":
    my_robot = Robot()
    run_robot(my_robot)