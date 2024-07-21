# mazeCommRL-CORE
A communication-efficient reinforcement learning algorithm for solving maze exploration problems by a coordinated group of swarm robots in CORE simulation environment.

This repository contains the open-sourced codes and datasets from the below paper.

# Publication/Citation
If you use this work, please cite our paper:
Latif E, Song W, Parasuraman R. Communication-efficient reinforcement learning in swarm robotic networks for maze exploration. In Proceedings of IEEE INFOCOM 2023-IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS) 2023 May 20 (pp. 1-6). IEEE.

IEEE Published version:  https://ieeexplore.ieee.org/abstract/document/10226167

Preprint available at: https://arxiv.org/pdf/2305.17087


## Quick Start Guide
**courtesy of Dr. Wenzhan Song Micromouse [Repository](https://github.com/wsonguga/Micromouse.git)**

Run in CORE   - Quick Guide
First, make sure that CORE has been installed. If you have not installed CORE, follow CORE Tutorial to install.
Also, Install python3-tk:

    $ sudo apt-get install python3-tk
Download the MazeCommRL framework from MazeCommRL Github Page. 

    $ cd ~
    $ git clone https://github.com/herolab-uga/MazeCommRL.git
    $ cd MazeCommRL
 
Configure the CORE environment for running core_demo.py

    $ sudo ./setCORE.sh
 
If you encounter any problems running the above script, you may need to manually configure the environment for CORE.
Open the framework/gui.py before starting a session:

    $ cd framework
    $ python3 gui.py
 
Open CORE to demonstrate:

    $ core-gui
 
Then open maze.xml, click the Start button.

## Module Description
    MazeCommRL
    ├── backservice.sh          //starting program in MyService
    ├── __init__.py             //module automatically read by CORE when core-gui opens
    ├── preload.py              //MyService class as an extra service that can be added into CORE, pointered by __init__.py
    │                             and it specifies the starting program - backservice.sh
    │                             Calling Relations: CORE -> __init__.py -> preload.py -> backservice.sh -> demo_core.py
    ├── framework               //framework written in Python3
    ├── icons                   //folder for icons of mice shown in CORE
    ├── mazes                   //folder for maze examples that png files are pictures for backgrounds and txt files 
    │                             are corresponding maze presented in (*, |, etc) which should be parsed by a function. 
    │                             See map.py -> readFromFile as a parser example.
    ├── maze.xml                //layout file opened and saved by CORE v4.8
    └── README.md

## Several Notes for understanding the code

### auto-start design
It is based on 6.2 of CORE tutorial (https://docs.google.com/document/d/1LPkPc2lbStwFtiukYfCxhcW7KewD028XzNfMd20uFFA/edit#heading=h.2clxcd487uk4) as written in framework/demo_core.py. When we open a CORE GUI, it looks for the __init__.py in current fold whose path we have put in /etc/core/core.conf. __init__py then loads preload.py. Then preload.py then loads backservice.sh. And then backservice.sh runs demo_core.py

### Change Maze for simulation
In  (https://github.com/herolab-uga/MazeCommRL/tree/main/mazes), you will see a number of mazes to simulate. Use the following steps to change the maze for simulation:
1. In (https://github.com/herolab-uga/MazeCommRL/tree/main/maze.xml) line 93
> <parameter name="canvas c1">{name {Canvas1}} {wallpaper-style {scaled}} {wallpaper {~/mazeCommRL/tree/main/mazes/<maze_image>}} {size {1158 772}}</parameter>
    
replace <maze_image> with one of the maze file names you find in the mazes folder. For example, 2012japan-ef.png.
    
2. In (https://github.com/herolab-uga/MazeCommRL/tree/main/framework/demo_core.py)  line 12:
> mazeMap.readFromFile('~/MazeCommRL/tree/main/mazes/<maze_text_file>')
    
replace <maze_text_file> with the corresponding maze text file associated with your replace maze image. For example, 2012japan-ef.txt

### Change Maze Coverage Strategy
We have implemented DFS and RL-based strategies; you can test both of them by changing strategy call in In  (https://github.com/herolab-uga/MazeCommRL/tree/main/framework/demo_core.py) line 18:
> micromouse.addTask(StrategyCommMazeRL(micromouse))

### node send message to host for moving itself
In  (https://github.com/herolab-uga/MazeCommRL/tree/main/framework/demo_core.py) line 16:
> micromouse.setMotorController(COREController(index, initPoint[index], controlNet='10.0.0.254'))

In framework/controller_core.py (https://github.com/herolab-uga/MazeCommRL/tree/main/framework/controller_core.py)
    
In goStraight() function:
> os.system("coresendmsg -a " + self.controlNet + " node number=" + self.index + " xpos=" + str(self.xpos) + " ypos=" + str(self.ypos))


## Core contributors

* **Ehsan Latif** - PhD Candidate

* **Prof. Ramviyas Parasuraman** - HeRoLab, University of Georgia

* In collaboration with **Prof. WenZhan Song** - SensorWeb Lab, University of Georgia


## Heterogeneous Robotics (HeRoLab)

**Heterogeneous Robotics Lab (HeRoLab), School of Computing, University of Georgia.**  

For further information, contact Prof. Ramviyas Parasuraman ramviyas @ uga.edu

https://hero.uga.edu/

<p align="center">
<img src="https://herolab.org/wp-content/uploads/2021/04/herolab_newlogo_whitebg.png" width="300">
</p>
