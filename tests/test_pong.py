from com.github.jonfreedman.interactivepython import pong

def test_paddle_cannot_leave_table():
    # create paddle centered on pixel 2 covering pixels [1,3)
    paddle = pong.Paddle([0, 2], 2, 1, (0, 4))

    paddle.change_velocity(-1 * 60)

    assert paddle.get_y() == 2
    paddle.move()
    assert paddle.get_y() == 1
    paddle.move()
    assert paddle.get_y() == 1

    paddle.change_velocity(1 * 60)

    paddle.move()
    assert paddle.get_y() == 2
    paddle.move()
    assert paddle.get_y() == 3
    paddle.move()
    assert paddle.get_y() == 3

def test_paddle_touches_ball():
    # create paddle centered on pixel 50 covering pixels [40,60)
    paddle = pong.Paddle([0, 50], 20, 1, (0, 99))

    assert paddle.touching_ball(pong.Ball([0,50], 1))
    assert paddle.touching_ball(pong.Ball([0,40], 1))
    assert paddle.touching_ball(pong.Ball([0,59], 1))
    assert not paddle.touching_ball(pong.Ball([0,39], 1))
    assert not paddle.touching_ball(pong.Ball([0,60], 1))

def test_paddle_not_moving_after_reset():
    paddle = pong.Paddle([0, 2], 2, 1, (0, 4))
    paddle.change_velocity(-1 * 60)
    assert(paddle.velocity == -60)
    paddle.reset()
    assert(paddle.velocity == 0)

def test_ball_can_move():
    ball = pong.Ball([0,50], 1)
    ball.velocity = [1 * 60, 1 * 60]
    ball.move()
    assert ball.position == [1, 51]

def test_ball_can_freeze():
    ball = pong.Ball([0,50], 1)
    ball.velocity = [1 * 60, 1 * 60]
    ball.freeze()
    assert ball.velocity == [0, 0]

def test_ball_can_bounce_vertically():
    ball = pong.Ball([0,50], 1)
    ball.velocity = [1, 1]
    ball.bounce_vertical()
    assert ball.velocity == [1, -1]
    ball.bounce_vertical()
    assert ball.velocity == [1, 1]

def test_ball_can_bounce_horizontally_and_speeds_up():
    ball = pong.Ball([0,50], 1)
    ball.velocity = [1, 1]
    ball.bounce_horizontal()
    assert ball.velocity == [-1 * 1.1, 1]
    ball.bounce_horizontal()
    assert ball.velocity == [1 * (1.1 ** 2), 1]