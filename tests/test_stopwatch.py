from com.github.jonfreedman.interactivepython import stopwatch

def test_format():
    assert stopwatch.format_time(0) == "0:00.0"
    assert stopwatch.format_time(7) == "0:00.7"
    assert stopwatch.format_time(17) == "0:01.7"
    assert stopwatch.format_time(60) == "0:06.0"
    assert stopwatch.format_time(63) == "0:06.3"
    assert stopwatch.format_time(214) == "0:21.4"
    assert stopwatch.format_time(599) == "0:59.9"
    assert stopwatch.format_time(600) == "1:00.0"
    assert stopwatch.format_time(602) == "1:00.2"
    assert stopwatch.format_time(667) == "1:06.7"
    assert stopwatch.format_time(1325) == "2:12.5"
    assert stopwatch.format_time(4567) == "7:36.7"
    assert stopwatch.format_time(5999) == "9:59.9"

def test_starts_at_zero():
    timer = stopwatch.Timer()
    assert timer.time == 0
    assert not timer.running

def test_start_stop_recorded():
    timer = stopwatch.Timer()
    timer.start()
    assert timer.running
    timer.stop()
    assert not timer.running

def test_timer_can_tick():
    timer = stopwatch.Timer()
    timer.tick()
    assert timer.time == 1
    timer.tick()
    assert timer.time == 2

def test_timer_can_reset():
    timer = stopwatch.Timer()
    timer.tick()
    assert timer.time == 1
    timer.reset()
    assert timer.time == 0
