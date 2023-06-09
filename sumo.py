# coding=utf-8

import traci # noqa
from flow import flow
from sigal import light,youxian

# 指定启动SUMO的命令和参数
sumoCmd = ['sumo-gui', '-c',  "try.sumocfg"]

traci.start(sumoCmd)
#交叉口名称
junction_id = "J2"
#设置车流，10为数量
flow(10,car="car")
# 设置公交车
flow(2,car="bus")
    # depart_time += 1  # 调整出发时间
# 添加车辆
simulation_steps = 88888  # 总共运行的仿真步数
time=0
y=0#保证一次赋值
sg=0#优先情况，1开启
vehicle_position = traci.vehicle.getPosition("car0")
# print(vehicle_position[0])
phase_list = ["rrrrrGGGrrrrrrrGGGrr", "rrrrrrrrGGrrrrrrrrGG", "GGGrrrrrrrGGGrrrrrrr", "rrrGGrrrrrrrrGGrrrrr"]
phase_time_list = [33, 15, 33, 15]
light_set, time_set = light(phase_list, phase_time_list)
print(time_set)
in_put=int(input("优先时间"))
for step in range(simulation_steps):
    traci.simulationStep()
    queue_length = traci.lanearea.getLastStepHaltingNumber("e2det_-E7_2")#道路检测器
    # print("Queue Length:", queue_length)
    time0 = traci.simulation.getCurrentTime()#获取仿真时间，ms
    time1=time0/1000#转化为s
    time = time1%time_set[-1]#确定周期数
    # if t==0:
    try:
        vehicle_position = traci.vehicle.getPosition("car0")#获取车辆位置信息
        # print(vehicle_position[0])
    except:
        vehicle_position=1000000000#检测不到车辆时，距离为无穷大
    # tls_state = traci.trafficlight.getRedYellowGreenState(junction_id)#获取信号灯
    # print(vehicle_position[0])
    if time==in_put:
        sg=1
    if sg==0:
        closest_number = max([x for x in time_set if x <= time])#获取时间列表内当前时间（time）左侧的第一个时间
        tls_state=light_set[time_set.index(closest_number)]#找到对应位置的相位
    if sg==1:
        y+=1#用于获取优化时刻的时间
        if y==1:
            a=time
            new_light,new_time=youxian(a,6,youxian_light='rrrrrrrrGGrrrrrrrrGG',light_list=light_set,time_list=time_set)
        # t=time_set[light_set.index('rrrrrrrrGGrrrrrrrrGG')+int(len(light_set)/2)]
        closest_number = max([x for x in new_time if x <= time])
        tls_state = new_light[new_time.index(closest_number)]#同上
        if time==new_time[-1]-1:#优化结束，复位
            y=0
            sg=0

    # speed = traci.vehicle.getSpeed("vehicle1")
    # if speed<0:
    #     print("Vehicle speed:", 0)
    # else:
    #     print("Vehicle speed:", speed)
        # 改变信号灯状态
    traci.trafficlight.setRedYellowGreenState(junction_id, tls_state)#获取信号灯状态

traci.close()