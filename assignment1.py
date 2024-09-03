from __future__ import print_function
import time
import sys
import csv
import os
from sr.robot import *

R = Robot()
""" instance of the class Robot"""
a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4


start_position = R.location
start_heading = R.heading
has_moved = False

crash_count = 0
min_distance = float('inf')
# Initialize the counter for missed silver tokens
missed_silver_tokens = 0


# Record start time (before entering the loop)
start_time = time.time()

max_time_limit = 240  # Maximum time allowed for the circuit in seconds

def drive_rot(speed, seconds):
    """
    Function for setting a linear velocity and an angular velocity
    """
    R.motors[0].m0.power = speed*2
    R.motors[0].m1.power = 0
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.rot_y<30.0 and token.rot_y>-30.0:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return 100, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD and ((token.dist < dist and token.rot_y<25 and token.rot_y>-25) or (token.dist < 0.5 and token.rot_y<90.0 and token.rot_y>-90.0)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return 100, -1
    else:
   	return dist, rot_y
   	
def check_right_side():
    dist = 100
    #print (R.see())
    for token in R.see():
         if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.rot_y<90.0 and token.rot_y>60.0:
             dist=token.dist
             #print(token.rot_y)
    if dist==100:
	return 100
    else:
   	return dist
   	
def check_left_side():
    dist = 100
    #print (R.see())
    for token in R.see():
         if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.rot_y>-90.0 and token.rot_y<-60.0:
             dist=token.dist
             #print(token.rot_y)
    if dist==100:
	return 100
    else:
   	return dist
   	
def has_completed_circuit():
    global has_moved
    current_position = R.location
    current_heading = R.heading

    # Minimum distance the robot must move away from the start before considering the circuit
    min_move_distance = 0.9  # Adjust as necessary
    position_tolerance = 0.7  # meters
    heading_tolerance = 0.5  # radians

    # Calculate the distance from the start position
    distance_from_start = ((current_position[0] - start_position[0]) ** 2 +
                           (current_position[1] - start_position[1]) ** 2) ** 0.5

    # Check if the robot has moved away from the starting position
    if distance_from_start > min_move_distance:
        has_moved = True

    # Check if the robot has returned to the start after moving
    position_close = (abs(current_position[0] - start_position[0]) < position_tolerance and
                      abs(current_position[1] - start_position[1]) < position_tolerance)

    heading_close = abs(current_heading - start_heading) < heading_tolerance

    # Circuit is only complete if the robot has moved away and then returned
    return has_moved and position_close and heading_close
  	
def save_results(elapsed_time, completed=False):
    """Saves the results to a CSV file."""
    file_exists = os.path.isfile('simulation_results.csv')
    with open('simulation_results.csv', 'a') as csvfile:
        headers = ['script_name', 'elapsed_time', 'crash_count', 'min_distance', 'missed_silver_tokens', 'completed_circuit']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow({
            'script_name': "assignment1.py",
            'elapsed_time': elapsed_time,
            'crash_count': crash_count,
            'min_distance': min_distance,
            'missed_silver_tokens': missed_silver_tokens,
            'completed_circuit': completed
        })

  	
while 1:
    # Robot movement logic
    dist, rot_y = find_silver_token()
    
    go = True
    if dist < 2.0:
        go = False
        dist2, rot2_y = find_golden_token()
        
        # Update the minimum distance to golden tokens
        if dist2 < min_distance:
            min_distance = dist2
            
        # Handle potential crashes
        if dist2 < 0.1:
            crash_count += 1
            
        if dist2 > 0.0 and dist2 < 0.8:
            go = True
        if dist == -1:  # if no token is detected, we make the robot turn
            pass
        elif dist < d_th:  # if we are close to the token, we try to grab it.
            print("Found it!")
            if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
                turn(30, 2)
                # drive(20,2)
                R.release()
                # drive(-20,2)
                turn(-30, 2)
            else:
                print("Aww, I'm not close enough.")
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(50, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
    if go:
        drive(50, .05)  # we move the robot forward
        dist, rot_y = find_golden_token()
        
        # Update the minimum distance to golden tokens
        if dist < min_distance:
            min_distance = dist
            
        # Handle potential crashes
        if dist < 0.1:
            crash_count += 1
        
        init = True
        left = True
        if dist > 0.0 and dist < 0.8:
            
            while True:
                if init:
                    dist_r = check_right_side()
                    dist_l = check_left_side()
                    print(dist_r)
                    print(dist_l)
                    if dist_r > dist_l:
                        left = True
                    else:
                        left = False
                    init = False

                if left:
                    turn(10, 0.1)
                else:
                    turn(-10, 0.1)
                dist, rot_y = find_golden_token()
                
                # Update the minimum distance to golden tokens
                if dist < min_distance:
                    min_distance = dist
                    
                # Handle potential crashes
                if dist < 0.1:
                    crash_count += 1
                    
                if dist > 2.0:
                    break
                    
                # Check if the robot has exceeded the maximum allowed time
                if time.time() - start_time > max_time_limit:
                    print("Time limit of 300 seconds exceeded. Ending simulation.")
                    elapsed_time = time.time() - start_time
                    # Save results to CSV even if the circuit is not completed
                    save_results(elapsed_time, completed=False)
                    sys.exit(0)  # Exit the script cleanly
                    break


     # Check if the circuit is completed
    if has_completed_circuit():
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Circuit completed!")
        print("Elapsed Time: ", elapsed_time)
        print("Crashes: ", crash_count)
        print("Min Distance to Golden Token: {:.2f}".format(min_distance))
        print("Missed Silver Tokens: ", missed_silver_tokens)
        print("Time to complete the circuit: {:.2f} seconds".format(elapsed_time))
            
        # Save results to CSV
        save_results(elapsed_time, completed=True)
        sys.exit(0)  # Exit the script cleanly
        break
        
    # Check if the robot has exceeded the maximum allowed time
    if time.time() - start_time > max_time_limit:
        print("Time limit of 300 seconds exceeded. Ending simulation.")
        elapsed_time = time.time() - start_time
        # Save results to CSV even if the circuit is not completed
        save_results(elapsed_time, completed=False)
        sys.exit(0)  # Exit the script cleanly
        break
         
        

	
