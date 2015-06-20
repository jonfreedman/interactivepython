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
    assert ball.get_x() == 1
    assert ball.get_y() == 51

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

def test_ball_changes_direction_on_reset():
    ball = pong.Ball([0,50], 1)
    assert ball.direction == pong.LEFT
    ball.reset()
    assert ball.direction == pong.RIGHT

def test_point_scoring():
    game = pong.Game()
    assert game.score == [0, 0]
    game.score_point(pong.LEFT)
    assert game.score == [1, 0]
    game.score_point(pong.RIGHT)
    assert game.score == [1, 1]

def test_game_reset_sets_score_to_zero():
    game = pong.Game()
    game.score_point(pong.LEFT)
    assert game.score == [1, 0]
    game.reset()
    assert game.score == [0, 0]

def test_game_starts_paused():
    game = pong.Game()
    assert game.pause == 20

def test_checking_if_game_is_paused_decrements_pause_timer():
    game = pong.Game()
    assert game.pause == 20
    game.is_paused()
    assert game.pause == 19

def test_game_reset_sets_pause():
    game = pong.Game()
    assert game.pause == 20
    game.is_paused()
    assert game.pause == 19
    game.reset()
    assert game.pause == 20
