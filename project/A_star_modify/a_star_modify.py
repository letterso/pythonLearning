"""
A*优化
将人工势场值作为启发函数比例系数
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
show_animation = True

class AStarPlanner:

    def __init__(self, ox, oy, resolution, rr):
        """
        Initialize grid map for a star planning

        ox: x position list of Obstacles [m]
        oy: y position list of Obstacles [m]
        resolution: grid resolution [m]
        rr: robot radius[m]
        """

        # A star参数
        self.resolution = resolution
        self.rr = rr
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0
        self.ox = ox
        self.oy = oy
        self.obstacle_map = None
        self.x_width, self.y_width = 0, 0
        self.motion = self.get_motion_model()
        self.calc_obstacle_map(ox, oy)

    class Node:
        def __init__(self, x, y, cost, parent_index):
            self.x = x  # index of grid
            self.y = y  # index of grid
            self.cost = cost
            self.parent_index = parent_index

        def __str__(self):
            return str(self.x) + "," + str(self.y) + "," + str(
                self.cost) + "," + str(self.parent_index)

    def planning(self, sx, sy, gx, gy):
        """
        A star path search

        input:
            s_x: start x position [m]
            s_y: start y position [m]
            gx: goal x position [m]
            gy: goal y position [m]

        output:
            rx: x position list of the final path
            ry: y position list of the final path
        """

        # potential_field参数
        self.calc_potential_field(gx,gy, self.ox, self.oy,self.resolution,self.rr)

        start_node = self.Node(self.calc_xy_index(sx, self.min_x),
                               self.calc_xy_index(sy, self.min_y), 0.0, -1)
        goal_node = self.Node(self.calc_xy_index(gx, self.min_x),
                              self.calc_xy_index(gy, self.min_y), 0.0, -1)

        open_set, closed_set = dict(), dict()
        open_set[self.calc_grid_index(start_node)] = start_node

        while 1:
            if len(open_set) == 0:
                print("Open set is empty..")
                break

            c_id = min(
                open_set,
                key=lambda o: open_set[o].cost + self.calc_heuristic(goal_node,
                                                                     open_set[
                                                                         o]))
            current = open_set[c_id]

            # show graph
            if show_animation:  # pragma: no cover
                plt.plot(self.calc_grid_position(current.x, self.min_x),
                         self.calc_grid_position(current.y, self.min_y), "xc")
                # for stopping simulation with the esc key.
                plt.gcf().canvas.mpl_connect('key_release_event',
                                             lambda event: [exit(
                                                 0) if event.key == 'escape' else None])
                if len(closed_set.keys()) % 10 == 0:
                    plt.pause(0.001)

            if current.x == goal_node.x and current.y == goal_node.y:
                print("Find goal")
                goal_node.parent_index = current.parent_index
                goal_node.cost = current.cost
                break

            # Remove the item from the open set
            del open_set[c_id]

            # Add it to the closed set
            closed_set[c_id] = current

            # expand_grid search grid based on motion model
            for i, _ in enumerate(self.motion):
                node = self.Node(current.x + self.motion[i][0],
                                 current.y + self.motion[i][1],
                                 current.cost + self.motion[i][2], c_id)
                n_id = self.calc_grid_index(node)

                # If the node is not safe, do nothing
                if not self.verify_node(node):
                    continue

                if n_id in closed_set:
                    continue

                if n_id not in open_set:
                    open_set[n_id] = node  # discovered a new node
                else:
                    if open_set[n_id].cost > node.cost:
                        # This path is the best until now. record it
                        open_set[n_id] = node

        rx, ry = self.calc_final_path(goal_node, closed_set)

        return rx, ry

    def calc_final_path(self, goal_node, closed_set):
        # generate final course
        rx, ry = [self.calc_grid_position(goal_node.x, self.min_x)], [
            self.calc_grid_position(goal_node.y, self.min_y)]
        parent_index = goal_node.parent_index
        while parent_index != -1:
            n = closed_set[parent_index]
            rx.append(self.calc_grid_position(n.x, self.min_x))
            ry.append(self.calc_grid_position(n.y, self.min_y))
            parent_index = n.parent_index

        return rx, ry

    def calc_heuristic(self, n1, n2):
        """[summary]

        Args:
            n1 ([double]): [goal_node]
            n2 ([double]): [open_set]

        Returns:
            [double]: [heuristic]
        """
        w = 1.0  # weight of heuristic
        d = w * math.hypot(n1.x - n2.x, n1.y - n2.y) * self.pmap[n2.x][n2.y]

        return d

    def calc_grid_position(self, index, min_position):
        """
        calc grid position

        :param index:
        :param min_position:
        :return:
        """
        pos = index * self.resolution + min_position
        return pos

    def calc_xy_index(self, position, min_pos):
        return round((position - min_pos) / self.resolution)

    def calc_grid_index(self, node):
        return (node.y - self.min_y) * self.x_width + (node.x - self.min_x)

    def verify_node(self, node):
        px = self.calc_grid_position(node.x, self.min_x)
        py = self.calc_grid_position(node.y, self.min_y)

        if px < self.min_x:
            return False
        elif py < self.min_y:
            return False
        elif px >= self.max_x:
            return False
        elif py >= self.max_y:
            return False

        # collision check
        if self.obstacle_map[node.x][node.y]:
            return False

        return True

    def calc_obstacle_map(self, ox, oy):
        self.min_x = round(min(ox))
        self.min_y = round(min(oy))
        self.max_x = round(max(ox))
        self.max_y = round(max(oy))
        print("min_x:", self.min_x)
        print("min_y:", self.min_y)
        print("max_x:", self.max_x)
        print("max_y:", self.max_y)

        self.x_width = round((self.max_x - self.min_x) / self.resolution)
        self.y_width = round((self.max_y - self.min_y) / self.resolution)
        print("x_width:", self.x_width)
        print("y_width:", self.y_width)

        # obstacle map generation
        self.obstacle_map = [[False for _ in range(self.y_width)]
                             for _ in range(self.x_width)]
        for ix in range(self.x_width):
            x = self.calc_grid_position(ix, self.min_x)
            for iy in range(self.y_width):
                y = self.calc_grid_position(iy, self.min_y)
                for iox, ioy in zip(ox, oy):
                    d = math.hypot(iox - x, ioy - y)
                    if d <= self.rr:
                        self.obstacle_map[ix][iy] = True
                        break

    def calc_potential_field(self, gx, gy, ox, oy, reso, rr):
        """计算势力图，当终点和障碍物确定后，势力图也可以确定

        Args:
            gx (double): [目标点x]
            gy (double): [目标点y]
            ox (list): [障碍物x]
            oy (list): [障碍物y]
            reso (double): [网格分辨率m]
            rr (double): [机器人半径m]

        Returns:
            [list]: [势力图]
        """
        self.pmap = [[0.0 for i in range(self.y_width)] for i in range(self.x_width)]

        for ix in range(self.x_width):
            x = ix * reso +self.min_x

            for iy in range(self.y_width):
                y = iy * reso + self.min_y
                ug = self.calc_attractive_potential(x, y, gx, gy)
                uo = self.calc_repulsive_potential(x, y, ox, oy, rr)
                uf = ug + uo
                self.pmap[ix][iy] = uf


        # 归一化
        pmin = min(min(row) for row in self.pmap)
        pmax = max(max(row) for row in self.pmap)

        for ix in range(len(self.pmap)):
            for iy in range(len(self.pmap[0])):
                self.pmap[ix][iy] = (self.pmap[ix][iy]-pmin)/(pmax-pmin)
        
        #print(self.pmap)

        self.draw_heatmap(self.pmap)
        

    def calc_attractive_potential(self, cx, cy, gx, gy):
        """计算引力

        Args:
            cx (double): 当前点x
            cy (double): 当前点y
            gx (double): 目标点x
            gy (double): 目标点y

        Returns:
            [double]: 返回欧几里德范数sqrt(x*x + y*y)
        """
        return 0.5 * KP * np.hypot(cx - gx, cy - gy)

    def calc_repulsive_potential(self,cx, cy, ox, oy, rr):
        """计算斥力

        Args:
            cx (double): 当前点x
            cy (double): 当前点y
            ox (list): 障碍物x
            oy (list)): 障碍物y
            rr (double): 机器人半径

        Returns:
            [double]: 斥力
        """
        # 获取最近的障碍物
        minid = -1
        dmin = float("inf")
        for i, _ in enumerate(ox):
            d = np.hypot(cx - ox[i], cy - oy[i])
            if dmin >= d:
                dmin = d
                minid = i

        # 计算与最近障碍物的欧式距离
        dq = np.hypot(cx - ox[minid], cy - oy[minid])
        
        # 判断是否小于机器人半径
        if dq <= rr:
            if dq <= 0.1:
                dq = 0.1

            # 计算斥力
            return 0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2
        else:
            return 0.0

    def draw_heatmap(self, data):
        data = np.array(data)  
        #data = np.array(data).T
        x_data = np.zeros([len(data),len(data[0])])
        y_data = np.zeros([len(data),len(data[0])])
        for y in range(len(data)):
            for x in range(len(data[0])):
                x_data[x][y] = self.calc_grid_position(x,self.min_x)
                y_data[x][y] = self.calc_grid_position(y,self.min_y)

        #data = data[:-1, :-1]
        plt.pcolor(x_data, y_data, data, vmax=0.1,cmap=plt.cm.Blues)

    @staticmethod
    def get_motion_model():
        # dx, dy, cost
        motion = [[1, 0, 1],
                  [0, 1, 1],
                  [-1, 0, 1],
                  [0, -1, 1],
                  [-1, -1, math.sqrt(2)],
                  [-1, 1, math.sqrt(2)],
                  [1, -1, math.sqrt(2)],
                  [1, 1, math.sqrt(2)]]

        return motion


def main():
    print(__file__ + " start!!")

    # start and goal position
    sx = 10.0  # [m]
    sy = 10.0  # [m]
    gx = 50.0  # [m]
    gy = 50.0  # [m]
    grid_size = 2.0  # [m]
    robot_radius = 1.0  # [m]

    # set obstacle positions
    ox, oy = [], []
    for i in range(-10, 60):
        ox.append(i)
        oy.append(-10.0)
    for i in range(-10, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(-10, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(-10, 61):
        ox.append(-10.0)
        oy.append(i)
    
    for i in range(-10, 40):
        ox.append(20.0)
        oy.append(i)
    for i in range(0, 40):
        ox.append(40.0)
        oy.append(60.0 - i)
    for i in range(30, 40):
        ox.append(i)
        oy.append(20.0)
    for i in range(40, 50):
        ox.append(i)
        oy.append(40.0)
    for i in range(0, 20):
        ox.append(i)
        oy.append(40.0)
    for i in range(20, 40):
        ox.append(0)
        oy.append(i)

    if show_animation:  # pragma: no cover
        plt.plot(ox, oy, ".k")
        plt.plot(sx, sy, "og")
        plt.plot(gx, gy, "xb")
        plt.grid(True)
        plt.axis("equal")

    a_star = AStarPlanner(ox, oy, grid_size, robot_radius)
    rx, ry = a_star.planning(sx, sy, gx, gy)

    if show_animation:  # pragma: no cover
        plt.plot(rx, ry, "-r")
        plt.pause(0.001)
        plt.show()


if __name__ == '__main__':
    main()
