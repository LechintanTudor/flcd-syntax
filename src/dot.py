class DotType:
    """Dot type used in augmented grammars."""

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "</DOT>"


Dot: DotType = DotType()
