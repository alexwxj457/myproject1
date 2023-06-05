# coding=utf-8

import sys

import random

import sumolib

import traci # noqa
from flow import flow
from sigal import light
import csv

# 指定启动SUMO的命令和参数
sumoCmd = ['sumo-gui', '-c',  "try.sumocfg"]

traci.start(sumoCmd)
junction_id = "J2"


# 设置信号灯的状态
# 红灯：rrrr, 绿灯：GGGG, 黄灯：yyyy
traci.trafficlight.setRedYellowGreenState(junction_id, "rrrrrGGGrrrrrrrGGGrr")  # 设置为绿灯状态

# 启动SUMO仿真并连接到SUMO进程
# 车流量参数
# num_vehicles = 10  # 要添加的车辆数量
# depart_time = 30  # 初始出发时间
# depart_speed = 10  # 初始出发速度
# depart_lane = "best"  # 初始出发车道
# # 启动 SUMO 仿真
# # for i in range(num_vehicles):
# vehicle_id = f"vehicle1"
# traci.vehicle.add(vehicle_id, "r1", typeID="bus",depart=depart_time, departLane=depart_lane,departSpeed=depart_speed)
flow(10,car="car")
flow(2,car="bus")
    # depart_time += 1  # 调整出发时间
# 添加车辆
n=0#仿真周期数
simulation_steps = 88888  # 总共运行的仿真步数
time=0
sg=0
for step in range(simulation_steps):
    traci.simulationStep()
    queue_length = traci.lanearea.getLastStepHaltingNumber("e2det_-E7_2")
    # print("Queue Length:", queue_length)
    time0 = traci.simulation.getCurrentTime()
    time1=time0/1000
    time = time1 - n * 90

    # 获取信号灯状态（信号灯为四相位，直行相位为33s，左转相位为6s）
    tls_state = traci.trafficlight.getRedYellowGreenState(junction_id)
    vehicle_position = traci.vehicle.getPosition("car0")
    print(vehicle_position[0])
    # if tls_state[8]=='r' and -vehicle_position[0]<50:
    #     sg=1

    phase_list=[ "rrrrrGGGrrrrrrrGGGrr","rrrrrrrrGGrrrrrrrrGG","GGGrrrrrrrGGGrrrrrrr","rrrGGrrrrrrrrGGrrrrr"]
    phase_time_list=[33,15,33,15]
    light_set,time_set=light(phase_list,phase_time_list)
    if sg==0:
        closest_number = max([x for x in time_set if x <= time])
        tls_state=light_set[time_set.index(closest_number)]
    # if sg==1:
    #         tls_state="rrrrrrrrGGrrrrrrrrGG"

    if time==89:
        n+=1
    # speed = traci.vehicle.getSpeed("vehicle1")
    # if speed<0:
    #     print("Vehicle speed:", 0)
    # else:
    #     print("Vehicle speed:", speed)
        # 改变信号灯状态
    traci.trafficlight.setRedYellowGreenState(junction_id, tls_state)

traci.close()