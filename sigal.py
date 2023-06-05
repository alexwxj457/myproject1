def light(phase_list,phase_time_list):#设置信号灯
    yellow_list=[x.replace('G','y') for x in phase_list]#将绿灯变为黄灯
    light_list=[]
    time_gap_list=[0]
    time_list=[]
    for i in range(len(yellow_list)):
        light_list.append(phase_list[i])
        light_list.append(yellow_list[i])
        time_gap_list.append(phase_time_list[i])
        time_gap_list.append(3)
    for i in range(len(time_gap_list)-1):
        x=time_gap_list[:i+1]
        time_list.append(sum(x))


    return light_list,time_list#输出相位和时间的组合
x=[ "rrrrrGGGrrrrrrrGGGrr","rrrrrrrrGGrrrrrrrrGG","GGGrrrrrrrGGGrrrrrrr","rrrGGrrrrrrrrGGrrrrr"]
y=[33,6,33,6]
print(light(x,y))