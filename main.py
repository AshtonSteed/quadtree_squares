from matplotlib import pyplot as plt
from math import sin, cos
from celluloid import Camera

SEARCH_DEPTH = 3
PLOT_DEPTH = 9
N = 15
DRAW_QUADS = True
THRESHOLD = .1

COUNTER = 0

SAMPLED_POINTS = {}


def evaluate(point):
    # just an implicit function onto a point
    x = point[0]
    y = point[1]
    if y == 0:
        return float('NaN')
    value = x ** 2 + x * y + y ** 2
    return value


def radius(x, y, d):
    x = x + d / 2
    y = y + d / 2
    dx = cos(x + y) + y * sin(x * y)  # first order partial derivative with respect to x
    dx2 = -sin(x + y) + y ** 2 * cos(x * y)  # second order partial derivative with respect to x
    dy = cos(x + y) + x * sin(x * y)  # first order partial derivative with respect to y
    dy2 = -sin(x + y) + x ** 2 * cos(x * y)  # second order partial derivative with respect to y
    dxy = -sin(x + y) + x * y * cos(y * x) + sin(y * x)  # partial derivative with respect to x and y once
    try:
        r = (dx ** 2 + dy ** 2) ** 3 / 2 / (
                dy ** 2 * dx2 - 2 * dx * dy * dxy + dx ** 2 * dy2)  # radius of curvature formula
    except ZeroDivisionError:
        r = float('inf')
    return abs(r)


def contour_present(x, y, d, c):
    points = [(x, y), (x + d, y), (x, y + d), (x + d, y + d)]
    threshold = []
    for point in points:
        if point in SAMPLED_POINTS:
            value = SAMPLED_POINTS[point]
        else:
            value = evaluate(point)
            SAMPLED_POINTS[point] = value
        threshold.append(value > c)
    return threshold.count(threshold[0]) != len(threshold)


def plot(x, y, d, c):
    points = [(x, y), (x + d, y), (x, y + d), (x + d, y + d)]
    values = [SAMPLED_POINTS[point] for point in points]
    threshold = [value > c for value in values]

    def find_contour_vert(xtemp, y1, y2, v1, v2, guess):
        if v1 == v2:
            return None
        value = evaluate((xtemp, guess)) - c
        top = y2
        bottom = y1
        while abs(value) > THRESHOLD:
            point1 = (guess + bottom) / 2
            value1 = evaluate((xtemp, point1)) - c
            point2 = (guess + top) / 2
            value2 = evaluate((xtemp, point2)) - c
            if abs(value) + abs(value1) != abs(value + value1):
                top = guess
                guess = point1
                value = value1
            elif abs(value) + abs(value2) != abs(value + value2):
                bottom = guess
                guess = point2
                value = value2
            else:
                if abs(value1) < abs(value2):
                    top = guess
                    guess = point1
                    value = value1
                else:
                    bottom = guess
                    guess = point2
                    value = value2
        return guess

    def find_contour_horiz(ytemp, x1, x2, v1, v2, guess):
        if v1 == v2:
            return None
        value = evaluate((guess, ytemp)) - c
        top = x2
        bottom = x1
        while abs(value) > THRESHOLD:
            point1 = (guess + bottom) / 2
            value1 = evaluate((point1, ytemp)) - c
            point2 = (guess + top) / 2
            value2 = evaluate((point2, ytemp)) - c
            if abs(value) + abs(value1) != abs(value + value1):
                top = guess
                guess = point1
                value = value1
            elif abs(value) + abs(value2) != abs(value + value2):
                bottom = guess
                guess = point2
                value = value2
            else:
                if abs(value1) < abs(value2):
                    top = guess
                    guess = point1
                    value = value1
                else:
                    bottom = guess
                    guess = point2
                    value = value2
        return guess

    bottomx = x + d * (c - values[0]) / (values[1] - values[0])
    lefty = y + d * (c - values[0]) / (values[2] - values[0])
    topx = x + d * (c - values[2]) / (values[3] - values[2])
    righty = y + d * (c - values[1]) / (values[3] - values[1])
    # bottomx = find_contour_horiz(y, x, x + d, threshold[0], threshold[1], bottomx)
    # topx = find_contour_horiz(y + d, x, x + d, threshold[2], threshold[3], topx)
    # lefty = find_contour_vert(x, y, y + d, threshold[0], threshold[2], lefty)
    # righty = find_contour_vert(x + d, y, y + d, threshold[1], threshold[3], righty)
    # hellish condition checking time
    if threshold == [False, False, False, False]:  # condition 1
        pass
    elif threshold == [True, False, False, False]:  # 2
        plt.plot([bottomx, x], [y, lefty], 'w')
    elif threshold == [False, True, False, False]:  # 3
        plt.plot([bottomx, x + d], [y, righty], 'w')
    elif threshold == [True, True, False, False]:  # 4
        plt.plot([x, x + d], [lefty, righty], 'w')
    elif threshold == [False, False, True, False]:  # 5
        plt.plot([x, topx], [lefty, y + d], 'w')
    elif threshold == [True, False, True, False]:  # 6
        plt.plot([bottomx, topx], [y, y + d], 'w')
    elif threshold == [False, True, True, False]:  # 7
        plt.plot([x, bottomx], [lefty, y], 'w')
        plt.plot([topx, x + d], [y + d, righty], 'w')
    elif threshold == [True, True, True, False]:  # 8
        plt.plot([topx, x + d], [y + d, righty], 'w')
    elif threshold == [False, False, False, True]:  # 9
        plt.plot([topx, x + d], [y + d, righty], 'w')
    elif threshold == [True, False, False, True]:  # 10
        plt.plot([x, topx], [lefty, y + d], 'w')
        plt.plot([bottomx, x + d], [y, righty], 'w')
    elif threshold == [False, True, False, True]:  # 11
        plt.plot([bottomx, topx], [y, y + d], 'w')
    elif threshold == [True, True, False, True]:  # 12
        plt.plot([x, topx], [lefty, y + d], 'w')
    elif threshold == [False, False, True, True]:  # 13
        plt.plot([x, x + d], [lefty, righty], 'w')
    elif threshold == [True, False, True, True]:  # 14
        plt.plot([bottomx, x + d], [y, righty], 'w')
    elif threshold == [False, True, True, True]:  # 15
        plt.plot([x, bottomx], [lefty, y], 'w')
    elif threshold == [True, True, True, True]:  # 16
        pass


def draw_square(x, y, d):
    plt.plot([x, x + d, x + d, x], [y, y, y + d, y + d], 'r', alpha=.3)


def create_tree(depth, x, y, d, c):
    global COUNTER
    COUNTER += 1

    def subdivide():
        create_tree(depth + 1, x, y, d / 2, c)
        create_tree(depth + 1, x + d / 2, y, d / 2, c)
        create_tree(depth + 1, x, y + d / 2, d / 2, c)
        create_tree(depth + 1, x + d / 2, y + d / 2, d / 2, c)

    if DRAW_QUADS:
        draw_square(x, y, d)
    if depth < SEARCH_DEPTH:
        subdivide()
    elif contour_present(x, y, d, c):
        # print(depth)
        # if radius(x, y, d) < N ** 2 * d:
        # print('fdfa')
        # subdivide()
        if depth < PLOT_DEPTH:
            subdivide()

            # plot(x, y, d, c)
        else:
            plot(x, y, d, c)


def main():
    plt.style.use('dark_background')
    fig = plt.figure()
    plt.axes().set_aspect('equal')
    camera = Camera(fig)
    xmin = -2.01
    ymin = 0
    d = 4
    clevel = 2

    '''camera = Camera(fig)
    for i in range(20):
        plt.clf()
        create_tree(0, xmin, ymin, d, clevel + i / 20)
        camera.snap()
    animation = camera.animate()
    animation.save('poggie.gif', writer='imagemagick')
    #create_tree(0, xmin, ymin, d, clevel)'''

    create_tree(0, xmin, ymin, d, clevel)
    print(COUNTER)
    plt.show()


main()
