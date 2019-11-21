# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 12:34:24 2019

@author: bilin
"""
import networkx as nx
import random
import time
import matplotlib.pyplot as plt


class car:
    def __init__(self, id, currentPoss):
        self.id = id
        self.currentPoss = currentPoss
        self.route = []
        self.speed = (30 * 1000) / 60
        self.cM = 0
        self.tM = 7500
        self.wastedTime = 0

    def changePoss(self, newPoss):
        self.currentPoss = newPoss
        self.wastedTime = self.wastedTime

    def addTrash(self, M):
        self.cM = self.cM + int(M)

    def clearCar(self):
        self.cM = 0

    def getcM(self):
        return (self.cM)

    def gettM(self):
        return (self.tM)

    def getSpeed(self):
        return (self.speed)

    def getPoss(self):
        return (self.currentPoss)

    def getId(self):
        return (self.id)

    # для 1 машинки. что бы учитывать движение других машинок, нужно завести второй граф в глобали
    # и изменять его (типа прогназируемый графф)
    def calcRoute(self, graph, distance):
        poss = self.getPoss()
        for i in range(distance):
            pathList = list(graph.edges(poss))
            if len(pathList) == 1:
                self.route.append(pathList[0])
                poss = pathList[0][1]
                # temp = (pathList[0])
            else:
                maxMass = 0
                labels1 = [e for e in labels]
                for n in pathList:
                    if int(labels1[n[1]]) > maxMass:
                        labels1[n[1]] = 0
                        maxMass = int(labels1[n[1]])
                        poss = n[1]
                        maxIndex = n
                self.route.append(maxIndex)
        # print(self.route)
        return self.route


    def getRoute(self, graph):
        if not self.route:
            self.calcRoute(graph, 3)
        route = self.route.pop(0)
        # if len(route[0]) == 2:
        #     self.calcRoute(graph, 1)
        return route

    def setRoute(self, new_route):
        self.route = new_route


# class town_model:
#     def __init__(self, graph, labels, node_sizes, max_time=14400):
#         self.graph = graph
#         self.labels = labels
#         self.node_sizes = node_sizes
#         self.current_time = 0
#         self.max_time = max_time
#
#     def addTresh(self):
#         for n in labels.keys():
#             labels[n] = str(int(labels[n]) + delta * 5)
#         node_sizes.clear()
#         for n in nodes:
#             randTrash = int(float(labels[n]))
#             node_sizes.append(randTrash)
#             labels[n] = str(randTrash)
#         labels[0] = 0
#         node_sizes[0] = 0




def updateDraw(Graph, pos, labels, nodes):
    plt.clf()
    nx.draw(G, pos=pos, node_size=node_sizes, labels=labels, with_labels=True)
    plt.show()


G = nx.Graph()
G.add_edge(0, 1, weight=870)
G.add_edge(1, 2, weight=870)
G.add_edge(2, 3, weight=680)
G.add_edge(2, 4, weight=870)
G.add_edge(2, 5, weight=690)
G.add_edge(3, 4, weight=790)
G.add_edge(4, 5, weight=520)
G.add_edge(4, 7, weight=460)
G.add_edge(5, 6, weight=630)
G.add_edge(6, 7, weight=570)
G.add_edge(7, 9, weight=590)
G.add_edge(6, 8, weight=590)
G.add_edge(8, 9, weight=480)
G.add_edge(9, 11, weight=550)
G.add_edge(8, 10, weight=520)
G.add_edge(10, 11, weight=280)
G.add_edge(4, 12, weight=670)
G.add_edge(12, 13, weight=440)
G.add_edge(13, 14, weight=620)
G.add_edge(3, 14, weight=430)
G.add_edge(12, 15, weight=1110)
G.add_edge(15, 11, weight=570)
G.add_edge(15, 16, weight=500)
G.add_edge(16, 13, weight=1200)
G.add_edge(12, 7, weight=560)

nodes = range(len(G.nodes))
node_sizes = []
labels = {}
for n in nodes:
    randTrash = random.randint(700, 1300)
    node_sizes.append(randTrash)
    labels[n] = str(randTrash)
labels[0] = 0
node_sizes[0] = 0


def addTresh(labels, node_sizes, delta):
    for n in labels.keys():
        labels[n] = str(int(labels[n]) + delta * 10)
    node_sizes.clear()
    for n in nodes:
        randTrash = int(float(labels[n]))
        node_sizes.append(randTrash)
        labels[n] = str(randTrash)
    labels[0] = 0
    node_sizes[0] = 0


pos = nx.spring_layout(G)
car1 = car(1, 0)


def wheretogo(car, G, labels):
    pathList = list(G.edges(car.getPoss()))
    if len(pathList) == 1:
        return (pathList[0][1])
    else:
        maxMass = 0
        for n in pathList:
            if int(labels[n[1]]) > maxMass:
                maxMass = int(labels[n[1]])
                maxIndex = n[1]
        return (maxIndex)

#
flag = True
trashMass = 0
car1.calcRoute(G, 5)
for x in range(20):
    # updateDraw(G, pos, labels, node_sizes)
    # target = wheretogo(car1, G, labels)
    # s = G[car1.getPoss()][target]['weight']
    # deltatime = int(s / car1.getSpeed())
    # print(car1.getcM())
    # car1.changePoss(target)
    #

    print(f"car route: {car1.route}")
    updateDraw(G, pos, labels, node_sizes)
    target = car1.getRoute(G)
    s = G[target[0]][target[1]]['weight']
    deltatime = int(s / car1.getSpeed())
    car1.changePoss(target[1])
    print(f"current car mass: {car1.getcM()}")

    addTresh(labels, node_sizes, deltatime)
    deltatime = 0
    if int(labels[car1.getPoss()]) > 750:
        car1.addTrash(labels[car1.getPoss()])
        labels[car1.getPoss()] = 0
        deltatime = 5
    if car1.getcM() > car1.gettM() * 0.7:
        car1.changePoss(0)
        car1.calcRoute(G, 5)
        way = nx.dijkstra_path_length(G, car1.getPoss(), 0)
        deltatime = deltatime + (way / 1000) / car1.getSpeed()
        trashMass = trashMass + car1.getcM()
        car1.clearCar()

        deltatime = deltatime + 3
    addTresh(labels, node_sizes, deltatime)
    if deltatime == 0:
        addTresh(labels, node_sizes, 1)
    print(f"tresh mass: {trashMass}")

