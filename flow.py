import random
import traci
def  flow(num,car):
# 生成包含90个1和10个0的列表
    my_list = [1] * num + [0] * (60-num)
    n=0
    time=0
# 随机打乱列表中元素的顺序
    random.shuffle(my_list)
    for i in my_list:
        if i==1:
           vehicle_id = f"{car}{n}"
           n+=1
           traci.vehicle.add(vehicle_id, "r1", typeID=car,depart=time, departLane="best",departSpeed=10)
           print(time)
        time+=1

