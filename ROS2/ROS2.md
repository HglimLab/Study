#ROS2 유튜브 강의

https://puzzling-cashew-c4c.notion.site/ROS-2-Launch-launch-file-55c2125808ef4b64bade278852b37d6e

# ROS2 Foxy 설치 - Linux20.04
```
$ sudo apt update
# terminator 설치
$ sudo apt install terminator -y
```
- Terminator (다중 분할 터미널을 위한 인터페이스)

- `sudo` 관리자 권한으로 실행
- `apt` 우분투 패키지 관리자

- `ctrl` + `shift` + `e` : 가로 분할
- `ctrl` + `shift` + `o` : 세로 분할
- `ctrl` + `shift` + `w` : 창 닫기
- `alt` + 화살표 : 창 간 이동

```
$ locale  # check for UTF-8

$ sudo apt update && sudo apt install locales
$ sudo locale-gen en_US en_US.UTF-8
$ sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
$ export LANG=en_US.UTF-8

locale  # verify settings

$ sudo apt update && sudo apt install curl gnupg2 lsb-release -y
$ sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg

$ sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'
$ sudo apt update

# Desktop Install (Recommended): ROS, RViz, demos, tutorials.
$ sudo apt install ros-foxy-desktop -y

# Install argcomplete (optional)
$ sudo apt install -y python3-pip
$ pip3 install -U argcomplete
```
- optional 부분은 설치 안 해도 됨.

### Gazebo 11 설치

``` 
$ sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
$ wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
$ sudo apt update

$ sudo apt install gazebo11 libgazebo11-dev -y

# Gazebo ROS 패키지들도 설치해줍니다.
$ sudo apt install ros-foxy-gazebo-ros-pkgs -y

# 설치 이후 실행을 통해 확인해 보세요!
$ gazebo

```

```
# 장착된 장치 확인
$ ubuntu-drivers devices
== /sys/devices/pci0000:00/0000:00:03.1/0000:1c:00.0 ==
modalias : pci:v000010DEd00001C03sv000010DEsd000011D7bc03sc00i00
vendor   : NVIDIA Corporation
model    : GP106 [GeForce GTX 1060 6GB]
driver   : nvidia-driver-460 - distro non-free recommended
driver   : nvidia-driver-450-server - distro non-free
driver   : nvidia-driver-390 - distro non-free
driver   : nvidia-driver-418-server - distro non-free
driver   : nvidia-driver-460-server - distro non-free
driver   : nvidia-driver-450 - distro non-free
driver   : xserver-xorg-video-nouveau - distro free builtin

>> 1060 and nvidia-driver-450 recommended

# 해당 장치에 맞는 드라이버 자동 설치
$ sudo ubuntu-drivers autoinstall
# 수동 설치
$ sudo apt install nvidia-driver-440 -y

# 설치 이후 재부팅
$ sudo reboot

```

- 추가 패키지 설치
```
$ sudo apt install ros-foxy-rqt*
$ sudo apt install ros-foxy-image-view
$ sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup 
$ sudo apt install ros-foxy-joint-state-publisher-gui
$ sudo apt install ros-foxy-xacro
```

### 중간 점검
```
# terminal 1
$ source /opt/ros/foxy/setup.bash
$ ros2 run demo_nodes_cpp talker
[INFO] [1615095938.051048376] [talker]: Publishing: 'Hello World: 1'
[INFO] [1615095939.051065032] [talker]: Publishing: 'Hello World: 2'
[INFO] [1615095940.051099193] [talker]: Publishing: 'Hello World: 3'
[INFO] [1615095941.051135001] [talker]: Publishing: 'Hello World: 4'
(...)

# terminal 2
$ source /opt/ros/foxy/setup.bash
$ ros2 run demo_nodes_py listener
[INFO] [1615095962.061778153] [listener]: I heard: [Hello World: 1]
[INFO] [1615095963.052502132] [listener]: I heard: [Hello World: 2]
[INFO] [1615095964.052535749] [listener]: I heard: [Hello World: 3]
[INFO] [1615095965.052742932] [listener]: I heard: [Hello World: 4]
(...)
```
- 터미널 2개에서 위에서 보낸 값을 아래에서 받고 있다면 성공적으로 설치 완료

## 개발 환경 Setup

### Colcon Build system 설치
```
$ sudo apt update
$ sudo apt install python3-colcon-common-extensions
```
## workspace 생성
- command에서 workspace 생성 가능
```
$ source /opt/ros/foxy/setup.bash

$ mkdir -p ~/gcamp_ros2_ws/src
$ cd ~/gcamp_ros2_ws/src

$ mkdir -p ~/test_ros2_ws/src
$ cd ~/test_ros2_ws/src
```
- `mkdir` 폴더 생성

```
$ git clone https://github.com/ros/ros_tutorials.git -b foxy-devel
$ ls ros_tutorials
> roscpp_tutorials  rospy_tutorials  ros_tutorials  turtlesim
```
- 패키지 설치

```
$ cd ../
$ rosdep install -i --from-path src --rosdistro foxy -y
> All required rosdeps installed successfully
```
- `-y` 미리 yes라고 지정
- `sudo apt install -y python3-rosdep2 설치 먼저
- `rosdep` 설치 되어있는지 확인 후, 미설치 시 설치 작업 

```
$ colcon build --symlink-install
$ ls
> build  install  log  src
```
- colcon을 이용하여 빌드 진행
- 만약 command not found error 발생 시, `sudo apt install python3-colcon-common-extensions` 하기

### ~/.bashrc 수정(단축키 설정)
- 터미널에서 `$ gedit ~/.bashrc` 입력
- 파일 마지막 부분에 다음과 같은 내용 입력

```
alias eb='gedit ~/.bashrc'
alias sb='source ~/.bashrc'

alias cba='colcon build --symlink-install'
alias cbp='colcon build --symlink-install --packages-select'
alias killg='killall -9 gzserver && killall -9 gzclient && killall -9 rosmaster'

alias rosfoxy='source /opt/ros/foxy/setup.bash && source ~/gcamp_ros2_ws/install/local_setup.bash'

source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=~/gcamp_ros2_ws
```


- rosfoxy라는 단축어로 ros2 환경 set up 실행 가능

# ROS 2 Node, Package와 기본 커멘드

- 노드 실행
```
$ rosfoxy
$ ros2 run turtlesim turtlesim_node

# 패키지가 무엇인지는 조금만 기다려 주세요!!
$ ros2 run <패키지 이름> <실행 프로그램 이름>
```
- 실행 중인 Node 리스트 확인

```
$ ros2 launch gcamp_gazebo gcamp_world.launch.py
$ ros2 node list
# 아래와 같은 Warning은 무시하셔도 좋습니다.
WARNING: Be aware that are nodes in the graph that share an exact name, this can have unintended side effects.
/gazebo
/rviz
/skidbot/camera_controller
/skidbot/gazebo_ros_head_hokuyo_controller
/skidbot/gazebo_ros_head_hokuyo_controller
/skidbot/skid_steer_drive_controller
/transform_listener_impl_5630ae791c60
```
- `ros2 node info 노드이름`으로 정확한 정보 얻기

```
$ ros2 node info /skidbot/skid_steer_drive_controller
/skidbot/skid_steer_drive_controller
  Subscribers:
    /clock: rosgraph_msgs/msg/Clock
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /skidbot/cmd_vel: geometry_msgs/msg/Twist
  Publishers:
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /rosout: rcl_interfaces/msg/Log
    /skidbot/odom: nav_msgs/msg/Odometry
    /tf: tf2_msgs/msg/TFMessage
  Service Servers:
    /skidbot/skid_steer_drive_controller/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /skidbot/skid_steer_drive_controller/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /skidbot/skid_steer_drive_controller/get_parameters: rcl_interfaces/srv/GetParameters
    /skidbot/skid_steer_drive_controller/list_parameters: rcl_interfaces/srv/ListParameters
    /skidbot/skid_steer_drive_controller/set_parameters: rcl_interfaces/srv/SetParameters
    /skidbot/skid_steer_drive_controller/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
  Service Clients:

  Action Servers:
동영상
  Action Clients:
  ```
  

### Rqt_Graph
- 실행 중인 Node들을 그래프로 시각화하여 살펴봄
```
# rqt 관련 패키지 설치
$ sudo apt install ros-foxy-rqt*
# 실행
$ rqt_graph
```

```
$ ros2 pkg create --build-type ament_cmake  <패키지이름> --dependencies rclcpp <종속성> 
$ ros2 pkg create --build-type ament_python <패키지이름> --dependencies rclpy <종속성> 
```
- 파이썬으로 pkg 빌드 시 `--dependencies rclpy` 꼭 넣어줘야함

- 이후 cba, cbp르 통해 빌드  하면 build 폴더에 바로가기 생성

# ROS 2 Launch, launch file 작성

- launch 명령어 구성

```
`ros2 launch gcamp_gazebo gcamp_world.launch.py`

⇒ `ros2 launch <패키지 이름> <launch 파일 이름>`
```

- 런치 파일 예시(gcamp_world.launch.py 아래 부분)
```
    # create and return launch description object
    return LaunchDescription(
        [
            # robot state publisher allows robot model spawn in RVIZ
            robot_state_publisher_node,
            # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
            # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
            ExecuteProcess(
                cmd=["gazebo", "--verbose", world, "-s", "libgazebo_ros_factory.so"],
                output="screen",
            ),
            # tell gazebo to spwan your robot in the world by calling service
            ExecuteProcess(
                cmd=[ "ros2", "service", "call", "/spawn_entity", "gazebo_msgs/SpawnEntity", spwan_args ],
                output="screen",
            ),
            ExecuteProcess(
                cmd=["ros2", "run", "rviz2", "rviz2", "-d", rviz], output="screen"
            ),
        ]
    )
```
- launch 파일 실행을 통해 gazebo, robot, rviz 동시 실행(ExecuteProcess 3가지 입력)
- ExecuteProcess는 개별 커멘드로 실행 가능
- ` cmd=["ros2", "run", "rviz2", "rviz2", "-d", rviz], output="screen" ` 마지막 문단


```
  # full  path to urdf and world file
  world = os.path.join(
      get_package_share_directory(package_name), "worlds", world_file_name
  )
  urdf = os.path.join(get_package_share_directory(package_name), "urdf", robot_file)
  rviz = os.path.join(get_package_share_directory(package_name), "rviz", rviz_file)
  ```
  -위 처럼 커맨드 라인 만들어두면 두고 두고 쓸 수 있음
  
  ### ExecuteProcess 방식 
  
#### rviz만을 동작시키는 launch file 

```
$ cd ~/gcamp_ros2_ws/src/gcamp_ros2_basic/gcamp_gazebo/launch
$ touch first_launch.launch.py
$ gedit first_launch.launch.py
```
- `touch` 새 파일 만들기
- first_launch.launch.py에 아래 내용 복붙 후 저장
```
#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():

    # create and return launch description object
    return LaunchDescription(
        [
            ExecuteProcess(
                cmd=["ros2", "run", "rviz2", "rviz2"], output="screen"
            ),
        ]
    )
```
이후

```
$ cd ~/gcamp_ros2_ws
$ cbp gcamp_gazebo
$ ros2 launch gcamp_gazebo first_launch.launch.py
```
성공적으로 rviz 실행

#### ExecuteProcess 문법

- ` generate_launch_description` :  ros2 launch 커멘드를 통해 launch file을 실행시키면, 이 이름을 가진 함수를 찾아들어갑니다. 그래서 모든 launch file에는 빠지지 않고 제일 먼저 등장하는 함수입니다.
- `LaunchDescription` : 필수 중 하나
- `ExecuteProcess` : 프로세스 하나를 실행시킨다는 구분의 개념으로 생각하시면 좋습니다.
- `cmd` : 앞에서 살펴본 바와 같이 터미널에서 입력하는 커멘드를 그대로 실행하고자 할 시에 사용 됩니다.  입력은 list 형태로 주어지며, space를 기점으로 나누어 주면 됩니다. `cmd = ["ros2", "run", ~ -- 띄어쓰기 단위로 콤마]
- `output` : Error log 등의 output이 출력되는 수단을 입력합니다.

### Node 방식

- launch 파일 만들어서 아래 스크립트 복사

```
#!/usr/bin/env python3

import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

# this is the function launch  system will look for
def generate_launch_description():

    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        parameters=[],
        arguments=[],
        output="screen",
    )

    turtlesim_teleop_node = Node(
        package='turtlesim',
        executable='draw_square',
        parameters=[],
        arguments=[],
        output="screen",
    )

    # create and return launch description object
    return LaunchDescription(
        [
            turtlesim_node,
            turtlesim_teleop_node,
        ]
    )
```
- package 실행 파일 2개 확인 가능


