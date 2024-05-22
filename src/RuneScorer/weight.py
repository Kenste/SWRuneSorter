profiles = []


class WeightProfile:
    def __init__(self, name, stat_weights, innate_weights, triple_roll_scale, quad_roll_scale):
        """
        :param name: the name to identify this weight profile
        :param stat_weights: a dictionary to map the stat to a weight
        :param innate_weights: a dictionary to map the (innate) stat to a weight
        :param triple_roll_scale: the scale to multiply the triple rolled stat with
        :param quad_roll_scale: the scale to multiply the quad rolled stat with
        """
        self.name = name
        self.stat_weights = stat_weights
        self.innate_weights = innate_weights
        self.triple_roll_scale = triple_roll_scale
        self.quad_roll_scale = quad_roll_scale
        profiles.append(self)

    def normalize(self):
        # TODO: implement normalization of this profile
        pass
