import pytest

class NotInRange(Exception):
    def __init__(self, message='Value not in the correct range'):
        self.message = message
        super().__init__(self.message)

def test_generic():
    # a=5
    # b=5
    # assert a==b
    a=2
    with pytest.raises(NotInRange):
        if a not in range(10,20):
            raise NotInRange