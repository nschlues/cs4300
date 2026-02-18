from task5 import books, student_ids, get_first_three_books

def test_books():
    assert isinstance(books, list)

def test_get_first_three_books():
    assert get_first_three_books(books) == ['Brandon Sanderson: Mistborn', 'N. D. Wilson: Ashtown Burials', 'God: The Bible']
    

def student_ids():
    assert isinstance(student_ids, dict)