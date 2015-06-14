from com.github.jonfreedman.interactivepython.stopwatch import format

def test_format():
    assert format(0) == "0:00.0"
    assert format(7) == "0:00.7"
    assert format(17) == "0:01.7"
    assert format(60) == "0:06.0"
    assert format(63) == "0:06.3"
    assert format(214) == "0:21.4"
    assert format(599) == "0:59.9"
    assert format(600) == "1:00.0"
    assert format(602) == "1:00.2"
    assert format(667) == "1:06.7"
    assert format(1325) == "2:12.5"
    assert format(4567) == "7:36.7"
    assert format(5999) == "9:59.9"