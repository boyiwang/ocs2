# OCS2 Toolbox

## Usage on Raspberry Pi 4B
Jump over unused packages
```shell
catkin config --skiplist ocs2_mpcnet ocs2_pinocchio ocs2_raisim ocs2_legged_robot ocs2_legged_robot_ros ocs2_mobile_manipulator ocs2_mobile_manipulator_ros ocs2_perceptive_anymal ocs2_raisim_core ocs2_raisim_ros ocs2_legged_robot_raisim
```
Compile configuration
```shell
catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-march=native -mtune=native"
```
When installing hpipm_catkin, hpipm will be downloaded automatically in /build/hpipm_catkin/download
copy the folder to src/ocs2/ocs2_sqp/hpipm_catkin/hpipm
Edit its CMakeLists, uncomment the line "set(TARGET GENERIC CACHE STRING "Set CPU architecture target")" and uncomment "AVX"
Edit the CMakeLists of hpipm_catkin, comment "FetchContent_Declare，FetchContent_MakeAvailable"
Add the line "add_subdirectory(${HPIPM_DOWNLOAD_DIR} ${HPIPM_BUILD_DIR})"
Recompile again.

## Summary
OCS2 is a C++ toolbox tailored for Optimal Control for Switched Systems (OCS2). The toolbox provides an efficient implementation of the following algorith

* SLQ: Continuous-time domin DDP
* iLQR: Discrete-time domain DDP
* SQP: Multiple-shooting algorithm based on HPIPM
* PISOC: Path integral stochatic optimal control

![legged-robot](https://leggedrobotics.github.io/ocs2/_static/gif/legged_robot.gif)

OCS2 handles general path constraints through Augmented Lagrangian or relaxed barrier methods. To facilitate the application of OCS2 in robotic tasks, it provides the user with additional tools to set up the system dynamics (such as kinematic or dynamic models) and cost/constraints (such as self-collision avoidance and end-effector tracking) from a URDF model. The library also provides an automatic differentiation tool to calculate derivatives of the system dynamics, constraints, and cost. To facilitate its deployment on robotic platforms, the OCS2 provides tools for ROS interfaces. The toolbox’s efficient and numerically stable implementations in conjunction with its user-friendly interface have paved the way for employing it on numerous robotic applications with limited onboard computation power.

For more information refer to the project's [Documentation Page](https://leggedrobotics.github.io/ocs2/) 
