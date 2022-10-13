import math 
# 根据已知两点坐标，求过这两点的直线解析方程： a*x+b*y+c = 0  (a >= 0)
def LE(p1x, p1y, p2x, p2y):
    sign = 1
    LE_a = p2y - p1y
    if LE_a < 0:
        sign = -1
        LE_a = sign * LE_a
    LE_b = sign * (p1x - p2x)
    LE_c = sign * (p1y * p2x - p1x * p2y)
    return [LE_a, LE_b, LE_c]
 
 
# 根据直线的起点与终点计算出平行距离D的平行线的方程
def LE_D(p1x, p1y, p2x, p2y, distance):
    """
    :param p1x: 起点X
    :param p1y: 起点Y
    :param p2x: 终点X
    :param p2y: 终点Y
    :param distance: 平距
    :param left_right: 向左还是向右
    """
    e = LE(p1x, p1y, p2x, p2y)
    # print(e)
    f = distance * math.sqrt(e[0] * e[0] + e[1] * e[1])
    m1 = e[2] + f
    m2 = e[2] - f
    # result = 值1 if 条件 else 值2
    c2 = m1 if p2y - p1y < 0 else m2
    return [e[0], e[1], c2]

# print(LE(-1,0,0,2))

