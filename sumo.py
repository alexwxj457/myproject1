# coding=utf-8

import sys

import random

import sumolib

import traci # noqa

import csv

# 指定启动SUMO的命令和参数
sumoCmd = ['sumo-gui', '-c',  "try.sumocfg"]

traci.start(sumoCmd)
junction_id = "J2"


# 设置信号灯的状态
# 红灯：rrrr, 绿灯：GGGG, 黄灯：yyyy
traci.trafficlight.setRedYellowGreenState(junction_id, "GGGrrrrrrrGGGrrrrrrr")  # 设置为绿灯状态

# 启动SUMO仿真并连接到SUMO进程
# 车流量参数
num_vehicles = 10  # 要添加的车辆数量
depart_time = 0  # 初始出发时间
depart_speed = 10  # 初始出发速度
depart_lane = "best"  # 初始出发车道
# 启动 SUMO 仿真
for i in range(num_vehicles):
    vehicle_id = f"vehicle{i}"
    traci.vehicle.add(vehicle_id, "r1", typeID="bus",depart=depart_time, departLane=depart_lane,departSpeed=depart_speed)
    depart_time += 1  # 调整出发时间
# 添加车辆
n=0#仿真周期数
simulation_steps = 1000000  # 总共运行的仿真步数
for step in range(simulation_steps):
    traci.simulationStep()
    time0 = traci.simulation.getCurrentTime()
    time1=time0/1000
    time=time1-n*90
    # 获取信号灯状态
    print(time)
    if time==90:
        n+=1

    tls_state = traci.trafficlight.getRedYellowGreenState(junction_id)
    if time==0:
        tls_state = "GGGrrrrrrrGGGrrrrrrr"
    if time==33:
        tls_state = "yyyrrrrrrryyyrrrrrrr"
    if time == 36:
        tls_state = "rrrGGrrrrrrrrGGrrrrr"
    if time == 42:
        tls_state = "rrryyrrrrrrrryyrrrrr"

    if time == 45:
        tls_state = "rrrrrGGGrrrrrrrGGGrr"
    if time == 78:
        tls_state = "rrrrryyyrrrrrrryyyrr"
    if time == 81:
         tls_state = "rrrrrrrrGGrrrrrrrrGG"
    if time == 87:
        tls_state = "rrrrrrrryyrrrrrrrryy"
    speed = traci.vehicle.getSpeed("vehicle1")
    print("Vehicle speed:", speed)
        # 改变信号灯状态
    traci.trafficlight.setRedYellowGreenState(junction_id, tls_state)

traci.close()