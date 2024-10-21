import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random as random

fig, ax = plt.subplots()

ax.set_xlim(0,25)
ax.set_ylim(0,25)
ax.set_aspect('equal')
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])

e1 = patches.Rectangle((5,7), 2, 16, edgecolor='black', facecolor='black')
e2 = patches.Rectangle((5,0), 2, 5, edgecolor='black', facecolor='black')
w1 = patches.Rectangle((7,18), 12, 3, edgecolor='grey', facecolor='grey')
w2 = patches.Rectangle((17,22.5), 8, 0.5, edgecolor='grey', facecolor='grey')
t = patches.Polygon([(12,0), (21, 3), (10,6) ], closed =True, edgecolor='black', facecolor='brown')
s = patches.Circle((17,12), 4.5, edgecolor='black', facecolor='gray')
pat = [e1, e2,s, w1, t, w2]
for i in pat:
    ax.add_patch(i)

ax.plot(1, 1, 'g^', label="Start", markersize=10)
ax.plot(18.5, 1, 'r^', label="End", markersize=10)

#olist = pat

class Node():
    def __init__(self, p, parent=None):
        self.p = np.array(p)
        self.parent = parent

step_length = 2
increments = 0.25

class Journey():
    def __init__(self, start, end, obstacle_list, x_dim, y_dim): #olist = obstacle list nlist = node list
        self.start = np.array(start)
        self.end = np.array(end)
        self.olist = obstacle_list
        self.nlist = [Node(start)]
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.complete = False

    def in_plot(self, pt):
        if 0<pt[0]<self.x_dim and 0<pt[1]<self.y_dim:
            return True
        else:
            return False

    def get_new_node(self):
        pt_found = False
        while not pt_found:
            if random.random() <= 0.1:
                x = self.end[0]
                y = self.end[1]
            else:
                x = random.random()*self.x_dim
                y = random.random()*self.y_dim
            for i in self.olist:
                if not i.contains_point(ax.transData.transform((x,y))):
                    pt_found = True

        n = np.array((x,y))
        nearest_node = None
        min_dist = self.x_dim+self.y_dim # just to create a value ST it will always be greater than distance between anytwo points in plot
        for i in self.nlist:
            dist = np.absolute(np.linalg.norm(n-i.p))
            if dist <= min_dist:
                min_dist = dist
                nearest_node = i

        collision = False
        #theta = np.arctan((y - nearest_node.p[1]) / (x - nearest_node.p[0]))
        #increment_vector = np.array(((increments)*np.cos(theta), (increments)*np.sin(theta)))
        increment_vector = np.array(increments*(n-nearest_node.p)/np.linalg.norm(n-nearest_node.p))
        for j in range(1,int(step_length/increments)+1):
            for k in self.olist:
                if k.contains_point(ax.transData.transform((nearest_node.p+increment_vector*j))) or k.contains_point(ax.transData.transform((nearest_node.p+increment_vector*j+increment_vector))) or not self.in_plot((nearest_node.p+increment_vector*j)):
                    collision = True
        if not collision:
            self.nlist.append(Node((nearest_node.p+step_length*increment_vector/np.linalg.norm(increment_vector)),nearest_node))

        if np.linalg.norm(self.nlist[-1].p - self.end) < 1:
            self.complete = True



rrt1 = Journey((1,1), (18.5,1), pat, 25, 25)

#c = 0
while not rrt1.complete:
    rrt1.get_new_node()
    # c +=1
    # if c%150 == 0:
    #     print(c)

for i in rrt1.nlist:
    plt.plot(i.p[0], i.p[1], 'ro', markersize = "4" )

# for i in rrt1.nlist:
#     print(i.p)
#     print(i.parent)

node1 = rrt1.nlist[-1]
p1 = node1.p
p2 = rrt1.end
c = True
while c:
    ax.plot([p2[0], p1[0]], [p2[1], p1[1]], marker='o', linestyle='-', color='b')
    if np.linalg.norm(p1-rrt1.start) == 0:
        c = False
    else:
        node2 = node1
        node1 = node1.parent
        p1 = node1.p
        p2 = node2.p



plt.show()
# circle = patches.Circle((5, 5), radius=3)
# pat.append(circle)
#
# for i in ax.patches:
#     print(i)
#     if i.contains_point((13,3)):
#         print("Yes")
#     else:
#         print("no")

