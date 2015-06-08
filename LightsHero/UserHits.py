from pygame import K_F1, K_F2, K_F3, K_F4, K_F5, KEYDOWN, KEYUP, event

class UserHits():
    """
    This is the class counting the score of the user and returning pressed keys
    TODO: add some tolerance with the hit window
    """
    hit_window = {'easy': 0.2, 'medium': 0.18, 'difficult': 0.16, 'expert': 0.14 }
    # More precise hit window: https://raw.githubusercontent.com/fofix/fofix/master/doc/old/hitwindows.htm

    def __init__(self, num_lanes):
        self.score = 0
        self.max_score = 0  # measures the maximum score that the user could have
        self.num_lanes = num_lanes
        self.active_notes = [False]*num_lanes
        self.keys = [False]*num_lanes

    def set_note(self, num_lane, active):
        self.active_notes[num_lane] = active

    def get_pressed_keys(self):
        """
        Count score and return the pressed lanes
        :return: vector of one boolean per lane True if the corresponding lane is being pressed
        """
        # 1. Get pressed keys
        for evt in event.get():
            if evt.type in [KEYDOWN, KEYUP]:
                if evt.key==K_F1:
                    self.keys[0] = evt.type==KEYDOWN
                elif evt.key==K_F2:
                    self.keys[1] = evt.type==KEYDOWN
                elif evt.key==K_F3:
                    self.keys[2] = evt.type==KEYDOWN
                elif evt.key==K_F4:
                    self.keys[3] = evt.type==KEYDOWN
                elif evt.key==K_F5:
                    self.keys[4] = evt.type==KEYDOWN

        # 2. Update the score and the maximum score
        for lane in range(self.num_lanes):
            if self.keys[lane] and self.active_notes[lane]:
                self.score += 10
            elif self.keys[lane] and not self.active_notes[lane]:
                self.score -= 2

            if self.active_notes[lane]:
                self.max_score += 10
        return self.keys


