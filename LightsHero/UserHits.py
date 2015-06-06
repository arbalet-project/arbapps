from pygame import key, K_F1, K_F2, K_F3, K_F4, K_F5, error

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

    def set_note(self, num_lane, active):
        self.active_notes[num_lane] = active

    def get_pressed_keys(self):
        """
        Count score and return the pressed lanes
        :return: vector of one boolean per lane True if the corresponding lane is being pressed
        """
        # 1. Get pressed keys
        try:
            keys = [key.get_pressed()[K_F1], key.get_pressed()[K_F2], key.get_pressed()[K_F3], key.get_pressed()[K_F4], key.get_pressed()[K_F5]]
        except error:
            # An error occurs if pygame is stopped
            keys = [False]*self.num_lanes

        # 2. Update the score and the maximum score
        for lane in range(self.num_lanes):
            if keys[lane] and self.active_notes[lane]:
                self.score += 10
            elif keys[lane] and not self.active_notes[lane]:
                self.score -= 2

            if self.active_notes[lane]:
                self.max_score += 10
        return keys


