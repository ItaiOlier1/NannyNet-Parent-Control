import time
import threading
from ParentControlDatabase import MyDatabase


class Timer:

    def __init__(self, DB : MyDatabase, kid_id, logic_q):
        """
        init
        :param DB: the database object
        :param kid_id: the kid's id
        :param logic_q: the logic q
        """
        self.DB = DB  # the data base
        self.kid_id = kid_id  # kid id
        self.remaining_time = self.DB.getRemainingTime(self.kid_id)  # remaining time
        self.run = True  # a flag that is on as long as the kid is active
        self.logic_q = logic_q  # the q with the logic
        threading.Thread(target=self._timer,).start()

    def kill(self):
        """
        kill the Timer
        :return: None
        """
        self.run = False
        self.DB.setRemainingTime(self.kid_id, self.remaining_time)
        print(f"change made in the data base, the new remaining time is: {self.DB.getRemainingTime(self.kid_id)}")

    def _get_time_limit_in_seconds(self, time_str):
        """
        get the time limit from {hh:mm:ss} to seconds
        :param time_str: {hh:mm:ss}
        :return:time limit in seconds
        """
        # split the time string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, time_str.split(":"))

        # Calculate the time limit in seconds
        time_limit = (hours * 60 + minutes) * 60 + seconds
        return time_limit

    def _timer(self):
        """
        the Timer method
        :return: None
        """
        print("started a new timer")
        # Define the time limit in seconds
        time_limit = self._get_time_limit_in_seconds(str(self.remaining_time))  # ####1 hour

        # Get the current time
        start_time = time.time()

        # Keep checking the remaining time until it reaches the time limit
        while time.time() - start_time < time_limit:

            if not self.run:
                print("the user disconnected, so close the timer")
                break

            # calculate the remaining time by subtracting the elapsed time from the time limit
            remaining_time = time_limit - (time.time() - start_time)

            # calculate the remaining hours, minutes, and seconds
            remaining_hours = int(remaining_time // 3600)  # remaining hours
            remaining_minutes = int((remaining_time % 3600) // 60)  # remaining minutes
            remaining_seconds = int(remaining_time % 60)  # remaining seconds

            # print the remaining time in the format "hh:mm:ss"
            self.remaining_time = f"{remaining_hours:02d}:{remaining_minutes:02d}:{remaining_seconds:02d}"

            # check if a minute has passed
            if int(remaining_time) % 60 == 0:
                print(self.remaining_time)
                self.logic_q.put([self.kid_id, self.remaining_time])

            # wait for one second before checking the time again
            time.sleep(1)



