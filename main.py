
from vpython import *
import math

# =====================================================
# FUZZY OBSTACLE AVOIDANCE FOR A MOBILE ROBOT
# 3D Simulation | Python + VPython
# =====================================================

# -------------------- SCENE --------------------------
scene = canvas(
    title="Fuzzy Obstacle Avoidance - Mobile Robot",
    width=1100,
    height=720,
    background=vector(0.84, 0.91, 1.0)
)
scene.autoscale = False
scene.center = vector(0, 0.4, 0)
scene.range = 15
scene.forward = vector(-1, -1.4, -1.8)
scene.up = vector(0, 1, 0)

# -------------------- ARENA ---------------------------
box(
    pos=vector(0, -0.16, 0),
    size=vector(24, 0.3, 18),
    color=vector(0.72, 0.78, 0.68)
)

# Boundary walls
for x in [-12, 12]:
    box(
        pos=vector(x, 0.45, 0),
        size=vector(0.22, 0.9, 18),
        color=vector(0.85, 0.88, 0.92)
    )

for z in [-9, 9]:
    box(
        pos=vector(0, 0.45, z),
        size=vector(24, 0.9, 0.22),
        color=vector(0.85, 0.88, 0.92)
    )

# Floor grid
grid_color = vector(0.57, 0.64, 0.56)

for x in range(-10, 11, 2):
    curve(
        pos=[vector(x, 0.012, -8.8), vector(x, 0.012, 8.8)],
        color=grid_color,
        radius=0.008
    )

for z in range(-8, 9, 2):
    curve(
        pos=[vector(-11.8, 0.012, z), vector(11.8, 0.012, z)],
        color=grid_color,
        radius=0.008
    )

# -------------------- OBSTACLES ----------------------
obstacle_data = [
    (-3, 1, 0.9),
    (1, -2, 0.9),
    (4, 2, 0.85),
    (0, 4, 0.75),
    (-6, -3, 0.85),
    (6, -4, 0.75)
]

obstacles = []

for ox, oz, radius in obstacle_data:
    cylinder(
        pos=vector(ox, 0, oz),
        axis=vector(0, 1.5, 0),
        radius=radius,
        color=vector(0.88, 0.16, 0.12)
    )

    # Obstacle top marker
    cylinder(
        pos=vector(ox, 1.5, oz),
        axis=vector(0, 0.04, 0),
        radius=radius * 0.55,
        color=color.orange
    )

    obstacles.append((ox, oz, radius))

# -------------------- GOAL ---------------------------
goal_x, goal_z = 8.0, 6.0

cylinder(
    pos=vector(goal_x, 0.025, goal_z),
    axis=vector(0, 0.05, 0),
    radius=0.8,
    color=color.green,
    opacity=0.8
)

# Goal rings
ring(
    pos=vector(goal_x, 0.08, goal_z),
    axis=vector(0, 1, 0),
    radius=1.0,
    thickness=0.035,
    color=color.green
)

label(
    pos=vector(goal_x, 0.45, goal_z),
    text="GOAL",
    color=color.green,
    box=False,
    height=18
)

# -------------------- ROBOT STATE --------------------
robot_x, robot_z = -9.0, -6.0
heading = 0.25

robot_length = 1.55
robot_width = 1.05
wheel_radius = 0.30
wheel_width = 0.18

blue = vector(0.08, 0.30, 0.82)
light_blue = vector(0.15, 0.65, 1.0)
dark = vector(0.12, 0.14, 0.18)

# Main robot chassis
body = box(
    pos=vector(robot_x, 0.55, robot_z),
    size=vector(robot_length, 0.42, robot_width),
    color=blue
)

# Upper shell
top = box(
    pos=vector(robot_x, 0.83, robot_z),
    size=vector(0.82, 0.18, 0.70),
    color=light_blue
)

# Front bumper
bumper = box(
    pos=vector(robot_x + 0.80, 0.48, robot_z),
    size=vector(0.12, 0.20, 0.82),
    color=vector(0.88, 0.91, 0.96)
)

# Front headlights
headlight_left = sphere(
    pos=vector(robot_x + 0.82, 0.57, robot_z - 0.28),
    radius=0.075,
    color=color.yellow
)

headlight_right = sphere(
    pos=vector(robot_x + 0.82, 0.57, robot_z + 0.28),
    radius=0.075,
    color=color.yellow
)

# Wheels
left_wheel = cylinder(
    pos=vector(robot_x, 0.30, robot_z - 0.58),
    axis=vector(0, 0, wheel_width),
    radius=wheel_radius,
    color=dark
)

right_wheel = cylinder(
    pos=vector(robot_x, 0.30, robot_z + 0.40),
    axis=vector(0, 0, wheel_width),
    radius=wheel_radius,
    color=dark
)

# Wheel hubs
left_hub = cylinder(
    pos=vector(robot_x, 0.30, robot_z - 0.59),
    axis=vector(0, 0, 0.025),
    radius=0.13,
    color=vector(0.65, 0.68, 0.73)
)

right_hub = cylinder(
    pos=vector(robot_x, 0.30, robot_z + 0.56),
    axis=vector(0, 0, 0.025),
    radius=0.13,
    color=vector(0.65, 0.68, 0.73)
)

# Top-mounted sensor / LiDAR-style unit
sensor_unit = cylinder(
    pos=vector(robot_x, 0.94, robot_z),
    axis=vector(0, 0.22, 0),
    radius=0.16,
    color=color.orange
)

sensor_cap = cylinder(
    pos=vector(robot_x, 1.16, robot_z),
    axis=vector(0, 0.045, 0),
    radius=0.18,
    color=dark
)

# -------------------- SENSOR RAYS --------------------
sensor_angles = [-0.90, -0.55, 0.0, 0.55, 0.90]
sensor_rays = []

for angle in sensor_angles:
    ray = curve(color=color.cyan, radius=0.018)
    sensor_rays.append(ray)

# -------------------- PATH TRACKING ------------------
path_line = curve(
    color=vector(0.10, 0.35, 0.95),
    radius=0.025
)
path_line.append(vector(robot_x, 0.035, robot_z))

# -------------------- LIVE DISPLAY -------------------
title_label = label(
    pos=vector(-8.5, 2.8, 7.2),
    text="FUZZY MOBILE ROBOT",
    height=18,
    box=False,
    color=blue
)

status_label = label(
    pos=vector(-8.5, 2.2, 7.2),
    text="Status: Initializing",
    height=14,
    box=False,
    color=color.black
)

sensor_label = label(
    pos=vector(-8.5, 1.65, 7.2),
    text="Sensors: Waiting",
    height=13,
    box=False,
    color=color.black
)

steering_label = label(
    pos=vector(-8.5, 1.1, 7.2),
    text="Steering: Straight",
    height=13,
    box=False,
    color=color.black
)

# -------------------- HELPER FUNCTIONS ---------------
def wrap_angle(angle):
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle


def ray_distance(angle):
    """Approximate distance to an obstacle along a sensor ray."""
    dx = math.cos(angle)
    dz = math.sin(angle)
    nearest = 6.0

    for ox, oz, radius in obstacles:
        vx = ox - robot_x
        vz = oz - robot_z

        along = vx * dx + vz * dz

        if along <= 0:
            continue

        side = abs(vx * dz - vz * dx)
        expanded_radius = radius + 0.65

        if side < expanded_radius:
            offset = math.sqrt(
                max(0.0, expanded_radius ** 2 - side ** 2)
            )
            hit = along - offset

            if hit > 0:
                nearest = min(nearest, hit)

    # Arena boundary distances
    if dx > 0.001:
        nearest = min(nearest, (11.2 - robot_x) / dx)
    elif dx < -0.001:
        nearest = min(nearest, (-11.2 - robot_x) / dx)

    if dz > 0.001:
        nearest = min(nearest, (8.2 - robot_z) / dz)
    elif dz < -0.001:
        nearest = min(nearest, (-8.2 - robot_z) / dz)

    return max(0.1, nearest)


def fuzzy_controller(front, left, right):
    """
    Simple fuzzy-style controller using near/medium/far
    membership values. Output is a steering command.
    Positive = turn left; negative = turn right.
    """

    def near_membership(distance):
        return max(0.0, min(1.0, (2.8 - distance) / 2.0))

    front_near = near_membership(front)
    left_near = near_membership(left)
    right_near = near_membership(right)

    # If the front is blocked, prefer the clearer side
    avoidance = 0.0

    if front_near > 0:
        if left > right:
            avoidance += 1.15 * front_near
        else:
            avoidance -= 1.15 * front_near

    # Side obstacle rules
    avoidance += 0.45 * left_near
    avoidance -= 0.45 * right_near

    return max(-1.0, min(1.0, avoidance))


def is_safe(x, z):
    for ox, oz, radius in obstacles:
        if math.hypot(x - ox, z - oz) < radius + 0.78:
            return False

    return (-11.0 < x < 11.0 and -8.0 < z < 8.0)


def update_robot_parts():
    """Move and rotate every robot part together."""
    forward = vector(math.cos(heading), 0, math.sin(heading))
    side = vector(-math.sin(heading), 0, math.cos(heading))

    body.pos = vector(robot_x, 0.55, robot_z)
    body.axis = forward
    body.up = vector(0, 1, 0)

    top.pos = vector(robot_x, 0.83, robot_z) + forward * 0.10
    top.axis = forward
    top.up = vector(0, 1, 0)

    bumper.pos = vector(robot_x, 0.48, robot_z) + forward * 0.79
    bumper.axis = forward
    bumper.up = vector(0, 1, 0)

    headlight_left.pos = (
        vector(robot_x, 0.57, robot_z)
        + forward * 0.80 - side * 0.28
    )
    headlight_right.pos = (
        vector(robot_x, 0.57, robot_z)
        + forward * 0.80 + side * 0.28
    )

    left_wheel.pos = vector(robot_x, 0.30, robot_z) - side * 0.55
    left_wheel.axis = side * wheel_width

    right_wheel.pos = vector(robot_x, 0.30, robot_z) + side * 0.55
    right_wheel.axis = side * wheel_width

    left_hub.pos = left_wheel.pos - side * 0.01
    left_hub.axis = side * 0.025

    right_hub.pos = right_wheel.pos - side * 0.01
    right_hub.axis = side * 0.025

    sensor_unit.pos = vector(robot_x, 0.94, robot_z)
    sensor_cap.pos = vector(robot_x, 1.16, robot_z)


# -------------------- SIMULATION ---------------------
speed = 0.055
simulation_steps = 0
max_steps = 30000
goal_reached = False
path_update_interval = 3

status_label.text = "Status: Robot moving"
steering_label.text = "Steering: Calculating"

while simulation_steps < max_steps:
    rate(40)
    simulation_steps += 1

    # Distance and direction to goal
    goal_dx = goal_x - robot_x
    goal_dz = goal_z - robot_z
    goal_distance = math.hypot(goal_dx, goal_dz)

    if goal_distance < 0.85:
        goal_reached = True
        break

    goal_angle = math.atan2(goal_dz, goal_dx)
    goal_error = wrap_angle(goal_angle - heading)

    # Front, left, and right sensor readings
    front = ray_distance(heading)
    left = ray_distance(heading + 0.65)
    right = ray_distance(heading - 0.65)

    # Fuzzy steering output
    avoid_turn = fuzzy_controller(front, left, right)

    # Goal-following command
    goal_turn = max(-0.60, min(0.60, goal_error))

    # Give obstacle avoidance more influence near obstacles
    if front < 2.8:
        goal_weight = max(0.15, front / 2.8)
    else:
        goal_weight = 1.0

    turn_command = goal_turn * goal_weight + avoid_turn
    turn_command = max(-1.0, min(1.0, turn_command))

    # Update heading
    heading = wrap_angle(heading + turn_command * 0.035)

    # Reduce speed near obstacles
    move_speed = speed
    if front < 1.5:
        move_speed = speed * 0.45

    # Candidate movement
    next_x = robot_x + move_speed * math.cos(heading)
    next_z = robot_z + move_speed * math.sin(heading)

    if is_safe(next_x, next_z):
        robot_x, robot_z = next_x, next_z
    else:
        # Try a turn if the next position is blocked
        if left >= right:
            heading = wrap_angle(heading + 0.22)
        else:
            heading = wrap_angle(heading - 0.22)

    # Update robot and its parts
    update_robot_parts()

    # Draw sensor rays
    for i, relative_angle in enumerate(sensor_angles):
        angle = heading + relative_angle
        distance = ray_distance(angle)

        sensor_rays[i].clear()
        sensor_rays[i].append(
            vector(robot_x, 0.68, robot_z)
        )
        sensor_rays[i].append(
            vector(
                robot_x + distance * math.cos(angle),
                0.68,
                robot_z + distance * math.sin(angle)
            )
        )

    # Track the route
    if simulation_steps % path_update_interval == 0:
        path_line.append(vector(robot_x, 0.035, robot_z))

    # Live information
    status_label.text = (
        "Status: RUNNING | Goal distance: {:.2f} m".format(
            goal_distance
        )
    )

    sensor_label.text = (
        "Sensors | Front: {:.1f} m | Left: {:.1f} m | Right: {:.1f} m".format(
            front, left, right
        )
    )

    if abs(turn_command) < 0.12:
        steering_text = "Straight"
    elif turn_command > 0:
        steering_text = "Turning LEFT"
    else:
        steering_text = "Turning RIGHT"

    steering_label.text = (
        "Steering: {} | Speed: {:.2f} m/step".format(
            steering_text, move_speed
        )
    )

# -------------------- FINAL STATUS -------------------
if goal_reached:
    status_label.text = (
        "GOAL REACHED! | Steps: {}".format(simulation_steps)
    )
    status_label.color = color.green
    steering_label.text = "Simulation completed successfully"
else:
    status_label.text = (
        "Step limit reached | Goal distance: {:.2f} m".format(
            math.hypot(goal_x - robot_x, goal_z - robot_z)
        )
    )
    status_label.color = color.orange
    steering_label.text = "Simulation stopped"

print("Simulation finished.")
print("Steps:", simulation_steps)
print("Goal reached:", goal_reached)
print(
    "Final distance to goal:",
    round(math.hypot(goal_x - robot_x, goal_z - robot_z), 2),
    "m"
)
