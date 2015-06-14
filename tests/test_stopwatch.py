from com.github.jonfreedman.interactivepython import stopwatch

def test_format():
    assert stopwatch.format(0) == "0:00.0"
    assert stopwatch.format(7) == "0:00.7"
    assert stopwatch.format(17) == "0:01.7"
    assert stopwatch.format(60) == "0:06.0"
    assert stopwatch.format(63) == "0:06.3"
    assert stopwatch.format(214) == "0:21.4"
    assert stopwatch.format(599) == "0:59.9"
    assert stopwatch.format(600) == "1:00.0"
    assert stopwatch.format(602) == "1:00.2"
    assert stopwatch.format(667) == "1:06.7"
    assert stopwatch.format(1325) == "2:12.5"
    assert stopwatch.format(4567) == "7:36.7"
    assert stopwatch.format(5999) == "9:59.9"