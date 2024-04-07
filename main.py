import threading
import time
import queue

class MissionControl:
    def __init__(self, r, s):
        self.regular_citizens = r
        self.super_citizens = s
        self.regular_queue = queue.Queue()
        self.super_queue = queue.Queue()
        self.teams = []
        self.team_id = 1
        self.lock = threading.Lock()
        self.super_count = 0
        self.regular_count = 0
        self.launch_event = threading.Event()

    def signup_regular_citizen(self, rc_id):
        with self.lock:
            print(f"Regular Citizen {rc_id} is signing up")
            self.regular_queue.put(rc_id)

    def signup_super_citizen(self, sc_id):
        with self.lock:
            print(f"Super Citizen {sc_id} is signing up")
            self.super_queue.put(sc_id)

    def form_team(self):
        with self.lock:
            regulars_needed = 4 - self.regular_count
            supers_needed = min(2 - self.super_count, self.super_queue.qsize())
            
            if regulars_needed <= 0 or supers_needed <= 0:
                return False
            
            team = []
            for _ in range(supers_needed):
                team.append(self.super_queue.get())
                self.super_count += 1
            
            for _ in range(regulars_needed):
                team.append(self.regular_queue.get())
                self.regular_count += 1
            
            self.teams.append((self.team_id, team))
            self.team_id += 1
            return True

    def launch_teams(self):
        while True:
            if not self.form_team():
                break
            time.sleep(1)  # Simulating team formation time
            if self.launch_event.is_set():
                break
        self.launch_event.set()
        self.print_summary()

    def print_summary(self):
        for team_id, team in self.teams:
            super_count = sum(1 for citizen in team if citizen.startswith("sc"))
            regular_count = sum(1 for citizen in team if citizen.startswith("rc"))
            print(f"team {team_id} is ready and now launching to battle (sc: {super_count} | rc: {regular_count})")

        print(f"Total teams sent: {len(self.teams)}")
        print(f"Regular Citizens not sent: {self.regular_queue.qsize()}")
        print(f"Super Citizens not sent: {self.super_queue.qsize()}")

def main():
    r = int(input("Enter the number of Regular Citizens: "))
    s = int(input("Enter the number of Super Citizens: "))

    mission_control = MissionControl(r, s)

    # Create and start threads for regular and super citizen signups
    regular_threads = [threading.Thread(target=mission_control.signup_regular_citizen, args=(f"rc{i}",)) for i in range(r)]
    super_threads = [threading.Thread(target=mission_control.signup_super_citizen, args=(f"sc{i}",)) for i in range(s)]

    for thread in regular_threads + super_threads:
        thread.start()

    # TODO: Create and start a thread to launch teams
    launch_thread = threading.Thread(target=mission_control.launch_teams)
    launch_thread.start()

    # Wait for all signups to complete
    for thread in regular_threads + super_threads:
        thread.join()

    # Wait for team formation and launch to complete
    launch_thread.join()

if __name__ == "__main__":
    main()
