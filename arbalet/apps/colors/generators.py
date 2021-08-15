from arbalet.colors import hsv_to_rgb


def gen_sweep_async(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    Browse the full color wheel (hue component)
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Unused
    :param n_frames_rand: Duration of fade + random seed
    :param colors: 1-element list containing the first color of the wheel
    """
    h0, s0, v0 = colors[0]

    # This loop fades up and is also the random seed
    for f in range(n_frames_rand):
        yield hsv_to_rgb(h0, s0, v0*f/n_frames_rand)

    # Infinite loop on color sequence
    while True:
        for f in range(n_frames):
            yield hsv_to_rgb((h0-f/n_frames) % 1., s0, v0)


def gen_sweep_rand(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    Fades all pixels from one color to the next one following a linear curve
    :param n_frames: Duration between two consecutive colors
    :param n_frames_fade: Duration of initial fade
    :param n_frames_rand: Random seed for this pixel, extra duration added to n_frames to get the total duration
    :param colors: list of colors to sweep
    """
    h0, s0, v0 = colors[0]
    num_cols = len(colors)
    n_frames = n_frames + n_frames_rand

    # This loop fades up and is also the random seed
    for f in range(n_frames_fade):
        yield hsv_to_rgb(h0, s0, v0*f/n_frames_fade)

    while True:
        # Selection of the next couple of colors (col_1, col_2)
        for col_1 in range(num_cols):
            col_2 = (col_1 + 1) % num_cols
            h1, s1, v1 = colors[col_1]
            h2, s2, v2 = colors[col_2]
            # Linearly fading col_1 to col_2
            for f in range(n_frames):
                factor_2 = f/n_frames
                factor_1 = 1 - factor_2
                yield hsv_to_rgb(h1*factor_1 + h2*factor_2,
                                 s1*factor_1 + s2*factor_2,
                                 v1*factor_1 + v2*factor_2)


def gen_random_flashing(n_frames, n_frames_fade, n_frames_rand, colors):
    """
    Fades all pixels to white (saturation = 0) following an exponential curve
    :param n_frames: Duration of two consecutive colors
    :param n_frames_fade: Duration of initial fade
    :param n_frames_rand: Random seed for this pixel, extra duration added to n_frames to get the total duration
    :param colors: At least 2 HSV elements to fade
    """
    h0, s0, v0 = colors[0]
    n_frames = n_frames + n_frames_rand

    # This loop fades up
    for f in range(n_frames_fade):
        yield hsv_to_rgb(h0, s0, v0*f/n_frames_fade)

    base = 1.1  # Exponential base. Higher the base is, lower the duration of fade will be

    def yield_exp(step):
        e = 1 - base**(step - n_frames//2 +1)  # e = 1..0
        return hsv_to_rgb(h0, e*s0, v0)

    while True:
        # Exponential rise
        for f in range(n_frames//2):
            yield yield_exp(f)
        # Exponential fall
        for f in range(n_frames//2, -1, -1):
            yield yield_exp(f)
