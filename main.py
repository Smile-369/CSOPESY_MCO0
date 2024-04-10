from threading import Thread, Lock
from time import sleep
import random

rc = []
sc = []
team = []
team_counter = 1  # Starting team number
data_lock = Lock()
r = 0
s = 0
total_citizens = 0

def recruit_rc(rc_id):
    global team_counter
    global total_citizens
    while True:
        data_lock.acquire()
        if len(rc) < r and len(team) < 4: # Check if there's room for more RC and the team is not full
            sleep(0.1)
            print(f"Regular Citizen {rc_id} is signing up")
            rc.append(rc_id)
            team.append(rc_id)
            total_citizens += 1
            print(f"RC {rc_id} joined team {team_counter}")
            data_lock.release()
            break
        else:
            sleep(0.1)
            print(f"Regular Citizen {rc_id} is waiting")
            data_lock.release()
            break
    if len(team) == 4:
        data_lock.acquire()
        super_count = sum(1 for member in team if member.startswith('SC'))
        regular_count = sum(1 for member in team if member.startswith('RC'))
        if super_count >= 1 and super_count <= 2:
            print(f"Team {team_counter} is ready and now launching to battle (sc:{super_count} | rc:{regular_count})")
            team_counter += 1
        else:
            print(f"Team {team_counter} cannot be formed. Sending remaining citizens home.")
            rc.clear()  # Clear the RC list
            sc.clear()  # Clear the SC list
            team.clear()  # Clear the team list
            if total_citizens == r + s:
                data_lock.release()
                return
        data_lock.release()

def recruit_sc(sc_id):
    global team_counter
    global total_citizens
    while True:
        data_lock.acquire()
        if len(sc) < s and len(team) < 4: # Check if there's room for more SC and the team is not full
            sleep(0.1)
            print(f"Super Citizen {sc_id} is signing up")
            sc.append(sc_id)
            team.append(sc_id)
            total_citizens += 1
            print(f"SC {sc_id} joined team {team_counter}")
            data_lock.release()
            break
        else:
            sleep(0.1)
            print(f"Super Citizen {sc_id} is waiting")
            data_lock.release()
            break
    if len(team) == 4:
        data_lock.acquire()
        super_count = sum(1 for member in team if member.startswith('SC'))
        regular_count = sum(1 for member in team if member.startswith('RC'))
        if super_count >= 1 and super_count <= 2:
            print(f"Team {team_counter} is ready and now launching to battle (sc:{super_count} | rc:{regular_count})")
            team_counter += 1
        else:
            print(f"Team {team_counter} cannot be formed. Sending remaining citizens home.")
            rc.clear()  # Clear the RC list
            sc.clear()  # Clear the SC list
            team.clear()  # Clear the team list
            if total_citizens == r + s:
                data_lock.release()
                return
        data_lock.release()

def main():
    global r
    global s
    
    r = int(input("Enter the number of Regular Citizens: "))
    s = int(input("Enter the number of Super Citizens: "))
    
    rc_ids = [f"RC_{i}" for i in range(1, r + 1)] # Generate regular citizen IDs
    sc_ids = [f"SC_{i}" for i in range(1, s + 1)] # Generate super citizen IDs
    random.shuffle(rc_ids) # Shuffle regular citizen IDs
    random.shuffle(sc_ids) # Shuffle super citizen IDs
    
    rc_threads = [Thread(target=recruit_rc, args=(rc_id,)) for rc_id in rc_ids]
    sc_threads = [Thread(target=recruit_sc, args=(sc_id,)) for sc_id in sc_ids]
    
    all_threads = rc_threads + sc_threads
    random.shuffle(all_threads)  # Shuffle all threads to randomize the order
    
    for t in all_threads:
        t.start()
    
    for t in all_threads:
        t.join()

    print(f"Total number of teams produced: {team_counter - 1}")  # Subtract 1 to get the correct total number of teams
    print(f"Regular Citizens not sent: {len(rc)}")
    print(f"Super Citizens not sent: {len(sc)}")

if __name__ == "__main__":
    main()
