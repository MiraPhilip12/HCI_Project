import time
import math

class SelectionState:
    def __init__(self, options_count):
        self.options = options_count
        self.last_index = None
        self.locked = False
        self.confirmed = False
        self.last_confirm_time = 0

    def angle_to_index(self, angle_rad):
        angle_deg = (math.degrees(angle_rad) + 360) % 360
        slice_angle = 360 / self.options
        index = int(((90 - angle_deg) % 360) / slice_angle)
        return index

    def update_angle(self, angle_rad):
        if self.locked:
            return None

        idx = self.angle_to_index(angle_rad)
        self.last_index = idx
        return idx

    def confirm(self):
        now = time.time()
        if now - self.last_confirm_time < 1.2:
            return None

        self.last_confirm_time = now
        self.locked = True
        self.confirmed = True
        return self.last_index
