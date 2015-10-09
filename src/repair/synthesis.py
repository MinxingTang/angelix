class SynthesisTimeout(Exception):
    pass


class Synthesizer:

    def __init__(self, config, extracted):
        self.config = config
        self.extracted = extracted

    def __call__(self, angelic_forest):
        raise SynthesisTimeout
        return None
