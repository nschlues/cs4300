def test_task1(capsys):
    exec(open("../src/task1.py").read())
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"