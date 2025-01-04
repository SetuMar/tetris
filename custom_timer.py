import time

class CustomTimer:
    def __init__(self, wait_time:float):
        self.wait_time = wait_time

        self._current_time = time.time()
        self._previous_time = time.time()

    def check_for_time_up(self):
        self._current_time = time.time()

        # must reset the timer immediately after
            # this is done for more control
        if self._current_time - self._previous_time > self.wait_time:
            return True

        return False

    def get_time_left(self):
        return self.wait_time - (self._current_time - self._previous_time)

    def reset_timer(self):
        self._current_time = time.time()
        self._previous_time = time.time()