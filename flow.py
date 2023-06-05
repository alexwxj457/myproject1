import random
import traci
# 生成车辆或车流
def  flow(num,car):#生成的车辆数和车辆类型
# 生成包含90个1和10个0的列表
    my_list = [1] * num + [0] * (60-num)#每分钟生成的车辆数，1为生成，0不生成
    n=0
    time=0#车辆生成时间
# 随机打乱列表中元素的顺序
    random.shuffle(my_list)#随机结果
    for i in my_list:
        if i==1:
           vehicle_id = f"{car}{n}"#车辆名称
           n+=1
           traci.vehicle.add(vehicle_id, "r1", typeID=car,depart=time, departLane="best",departSpeed=10)#生成车辆
           print(time)
        time+=1


