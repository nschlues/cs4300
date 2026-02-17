from task2 import integer, floater, string, boolean

def test_task2():
    assert integer == 3
    assert isinstance(integer, int)
    assert floater == 4.2
    assert isinstance(floater, float)
    assert string == "Soli Deo Gloria!"
    assert isinstance(string, str)
    assert boolean == True
    assert isinstance(boolean, bool)