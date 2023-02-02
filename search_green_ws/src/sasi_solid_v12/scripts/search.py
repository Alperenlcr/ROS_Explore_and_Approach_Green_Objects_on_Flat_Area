#!/usr/bin/env python
#--coding: utf-8 --
 
from re import T
from numpy.lib.function_base import average
import rospy
import numpy as np
import time
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from time import sleep
import os

os.path.isfile('./final_data.csv')

def zigzag():
    #print(time.time())
    hareket = Twist()
    #dosya var mi
        #yok ise dosya olustur ileri time time +1 yaz ilerlet
        #var ise ileri mi donme mi diye kontrol et
            #ileri ise 10 saniye olmus mu diye bak
                #olmamis ise son time'i guncelle          ilerlemeye devam ettir
                #olmus ise donme time time+1 yaz         dondur
            #donme ise 2.6 saniye olmus mu diye bak
                #olmamis ise son time'i guncelle          dondurmeye devam ettir
                #olmus ise ileri time time+1 yaz         ilerlet    yon.txt guncelle
    #if os.path.exists('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt'):
    if True:
        with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt', 'r') as filex:
            data = filex.read().split()
        #data = ileri sure sure
        if data[0] == "ileri":
            if float(data[2]) - float(data[1]) > 15:
                data[0] = "donme"
                data[1] = str(round(time.time(),2))
                data[2] = str(round(time.time()+1,2))

                with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt', 'r') as file:
                    temp = file.read()
                    if temp == "sol":
                        #saga gidecek
                        hareket.linear.x = 3
                        hareket.angular.z = 5
                    else:
                        #sola gidecek
                        hareket.linear.x = 3
                        hareket.angular.z = -5
            else:
                data[2] = round(time.time(),2)
                hareket.linear.x = 1.5  #roverin kendi onu
                hareket.angular.z = 0
        else:
            if float(data[2]) - float(data[1]) > 3:
                data[0] = "ileri"
                data[1] = str(round(time.time(),2))
                data[2] = str(round(time.time()+1,2))

                hareket.linear.x = 1  #roverin kendi onu
                hareket.angular.z = 0
                sag = 0
                with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt', 'r') as file:
                    temp = file.read()
                    if temp == "sag":
                        sag += 1
                with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt', 'w') as file:
                    if sag == 1:
                        file.write("sol")
                    else:
                        file.write("sag")

            else:
                data[2] = round(time.time(),2)
                with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt', 'r') as file:
                    temp = file.read()
                    if temp == "sag":
                        #saga gidecek
                        hareket.linear.x = 3
                        hareket.angular.z = 5
                    else:
                        #sola gidecek
                        hareket.linear.x = 3
                        hareket.angular.z = -5
    #else:
    #    with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt', 'w') as file:
    #        file.write("ileri {} {}".format(round(time.time(),2), round(time.time()+1,2)))
    #        hareket.linear.x = 1  #roverin kendi onu
    #        hareket.angular.z = 0
    pub.publish(hareket)
    with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt', 'w') as file:
        #print(data)
        file.write("{} {} {}".format(data[0], data[1], data[2]))


def yaklas(center):
    hareket = Twist()
    temp = center.split()
    x = int(temp[0])
    y = int(temp[1])
    if x > 700:
        hareket.angular.z=1
        #print("sol")
    elif x < 580:
        hareket.angular.z=-1
        #print("sag")
    else:
        hareket.angular.z=0
        #print("solsag degil")


    if y > 550:
        hareket.linear.x=-0.5
        #print("geri")
    elif y < 500:
        hareket.linear.x=0.5
        #print("ileri")
    else:
        hareket.linear.x=0
        #print("geriileri degil")

    pub.publish(hareket)

    if hareket.linear.x == 0 and hareket.angular.z == 0:
        print("\n\n\n\n\n[hareket]        ATES EDIYORUM 2 saniye verin bana\n\n\n\n\n\n\n")
        rospy.sleep(2)
        hareket.linear.x=2
        hareket.angular.z=0
        pub.publish(hareket)
        rospy.sleep(3)
        with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt', 'w') as file:
            file.write("ileri {} {}".format(round(time.time(),2), round(time.time()+1,2)))


def decision_maker(center):
    center = str(center)
    center = center[7:-1]
    temp = center.split()
    x = int(temp[0])
    y = int(temp[1])
    print("[hareket]     ", x, y)
    if x == 0 and y == 0:
        zigzag()
    else:
        yaklas(center)


if __name__=="__main__":
    with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/time.txt', 'w') as file:
            file.write("ileri {} {}".format(round(time.time(),2), round(time.time()+1,2)))
    if not os.path.isfile('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt'):
        with open('/home/alperenlcr/sifirdan/src/sasi_solid_v12/scripts/yon.txt', 'w') as file:
            file.write("sol")
    rospy.init_node("hareket", anonymous=False)
    center_coordinates = rospy.Subscriber("/center", String, decision_maker, queue_size=10)
    pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
    rospy.spin()

#txt de donus ve duz gitmelerin son saniyeleri olacak bi de etiketi olmali donus mu duz mu
#kod spin ile calisacak devamli centera sub olacak / txt de okunmali zigzag fonksiyonu basinda
#zigzagta if ile bunlara bakacak
#yaklasma tamamlandiginda 1-2 sn duz gidecek uyuyarak

#Txt ye ne zaman yazmasi lazim
#ilk kod calistiginda zigzaga girdiyse yazmali
#yaklas bittikten sonra yazmali
#donme ve duz gitmelerin degisiminde yazmali
