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
flow(100,car="car")
# 设置公交车
# flow(5,car="bus")
traci.vehicle.add("bus0", "r0", typeID="bus",depart=20, departLane="best",departSpeed=20)#生成车辆
traci.vehicle.add("bus1", "r0", typeID="bus",depart=60, departLane="best",departSpeed=20)#生成车辆
traci.vehicle.add("bus32", "r0", typeID="bus",depart=160, departLane="best",departSpeed=20)#生成车辆
    # depart_time +=b 1  # 调整出发时间
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
# in_put=int(input("优先时间"))
ti=0
mmm=0
lm_t=0
for step in range(simulation_steps):
    traci.simulationStep()
    queue_length = traci.lanearea.getLastStepHaltingNumber("e2det_-E7_2")#道路检测器
    time0 = traci.simulation.getCurrentTime()#获取仿真时间，ms
    time1=time0/1000#转化为s
    time = time1%time_set[-1]#确定周期数
    try:
        if mmm==0:
            vehicle_position0 = traci.vehicle.getPosition("bus0")#获取车辆位置信息
            v0=vehicle_position0[0]
        if mmm<=1:
            vehicle_position1=traci.vehicle.getPosition("bus1")
            v1=vehicle_position1[0]
            vehicle_position=min([x for x in [-100-v0,-100-v1] if x>-100])
    except:
        if mmm==0:
            v0=1000000
        if mmm==1:
            vehicle_position=10000
        mmm+=1
        pass
    # tls_state = traci.trafficlight.getRedYellowGreenState(junction_id)#获取信号灯
    # print(vehicle_position[0])
    tls_state = traci.trafficlight.getRedYellowGreenState(junction_id)
    print(vehicle_position, tls_state[6], ti)
    if -20<vehicle_position<10 and tls_state[6] =="r" and ti==0:
        sg=1#控制优先信号打开
        ti=1#保证一个周期内只进行一次优化
    if ti==1:
        print(lm_t,ti)
        lm_t+=1
        if lm_t==time_set[-1]:
            ti=0
            lm_t=0
    if sg==0:
        closest_number = max([x for x in time_set if x <= time])#获取时间列表内当前时间（time）左侧的第一个时间
        tls_state=light_set[time_set.index(closest_number)]#找到对应位置的相位

    if sg==1:
        if y==0:
            a=time
            y+=1
            new_light,new_time=youxian(a,8,youxian_light='rrrrrGGGrrrrrrrGGGrr',light_list=light_set,time_list=time_set)
        closest_number = max([x for x in new_time if x <= time])
        tls_state = new_light[new_time.index(closest_number)]#同上
        if time==new_time[-1]-1 :#优化结束，复位
            sg=0
            y=0
    traci.trafficlight.setRedYellowGreenState(junction_id, tls_state)#获取信号灯状态

traci.close()