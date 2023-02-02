# Exploring on Flat Area, Detecting and Approaching Green Objects

## What/How does it do?
 There two nodes. First one is detecting and publishing coordinates of green objects. Detection is accomplished with OpenCV libraries. Other node, handles navigation. While no objects detected, robot searches area with up and down moves. If it sees one, it approaches it after some time returns back to search state.

## How to run
### Run these commands below in order:
- Change directory to /search_green_ws at all 4 terminal
- Source necessary and catkin_make

    Then

- First terminal:
```
   $ roscore
```
- Second terminal:
```
 $ roslaunch sasi_solid_v12 gazebo.launch
```
- Third terminal:
```
 $ cd src/sasi_solid_v12/scripts/
 $ rosrun sasi_solid_v12 green_objects_center.py
```
- Fourth terminal:
```
 $ cd src/sasi_solid_v12/scripts/
 $ python3 search.py
 ```
 ### Note
 There are some file paths in code. You should change them first. Some communication done with help of these files.
