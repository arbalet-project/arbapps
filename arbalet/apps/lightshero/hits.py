from threading import RLock

class UserHits():
    """
    This is the class counting the score of the user and returning pressed keys
    This is normally pretty simple but since it is not possible to read keys from no window, this is a hack to
    get x11 events making the class less understandable. A X11 event recorder is started in a thread and updates self.keys

    TODO: add some tolerance with the hit window
    """
    #hit_window = {'easy': 0.2, 'medium': 0.18, 'difficult': 0.16, 'expert': 0.14 }
    # More precise hit window: https://raw.githubusercontent.com/fofix/fofix/master/doc/old/hitwindows.htm

    def __init__(self, num_lanes, events, sound, simulate_player):
        self.simulate_player = simulate_player
        self.sound = sound
        self.sliding_failures = -50  # Starting with negative will give some extra time before starting
        self.window_failures = 25  # Number of consecutive errors accepted
        self.score = 0
        self.events = events
        self.max_score = 0  # measures the maximum score that the user could have
        self.num_lanes = num_lanes
        self.active_notes = [False]*num_lanes
        self.keys = [False]*num_lanes
        self.keys_lock = RLock()

    def close(self):
        pass

    def set_note(self, num_lane, active):
        self.active_notes[num_lane] = active

    def update_keys(self, reply=None):
        """
        Update the map self.keys according to user inputs.
        It uses either the x11 method or the pygame events
        :reply: If the x11 method is used, this is the message returned from x11
        """
        with self.keys_lock:
            for event in self.events.get():
                if event['key'] == 'F1':
                    self.keys[0] = event['pressed']
                elif event['key'] == 'F2':
                    self.keys[1] = event['pressed']
                elif event['key'] == 'F3':
                    self.keys[2] = event['pressed']
                elif event['key'] == 'F4':
                    self.keys[3] = event['pressed']
                elif event['key'] == 'F5':
                    self.keys[4] = event['pressed']
                elif event['key'] == 'action' and event['pressed']:
                    self.switch_simulation()

    def switch_simulation(self):
        self.simulate_player = not self.simulate_player
        if self.simulate_player:
            self.set_playing_well(True)

    def set_playing_well(self, playing_well):
        """
        Call this method each time a note must be played,
        :param sucess: True if the user has correctly played this song, False otherwise
        :return:
        """
        if playing_well:
            self.sliding_failures = 0
            self.sound.set_playing_well(True)
        else:
            self.sliding_failures = min(self.sliding_failures + 1, self.window_failures)
            if self.sliding_failures == self.window_failures:
                self.sound.set_playing_well(False)

    def get_pressed_keys(self):
        """
        Count score and return the pressed lanes
        :return: vector of one boolean per lane True if the corresponding lane is being pressed
        """
        # 1. Get pressed keys
        self.update_keys()

        # 2. Update the score and the maximum score
        playing_well = True
        must_update = False
        for lane in range(self.num_lanes):
            if self.keys[lane] and self.active_notes[lane]:
                # Playing while he must
                self.score += 10
                must_update = True
            elif self.keys[lane] and not self.active_notes[lane]:
                # Playing while he must not
                self.score -= 2
                playing_well = False
                must_update = True
            elif not self.keys[lane] and self.active_notes[lane]:
                # Not playing while he must
                playing_well = False
                must_update = True

            if self.active_notes[lane]:
                self.max_score += 10
        if must_update and not self.simulate_player:
            self.set_playing_well(playing_well)
        return self.keys


