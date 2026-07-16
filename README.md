# Moveit2 Python Examples : [Reference](https://github.com/moveit/moveit2_tutorials/tree/main/doc/examples/motion_planning_python_api/scripts)

```bash
cd colcon_ws/src
git clone https://github.com/ipa-vsp/moveit_python_example.git
git clone -b jazzy-devel https://github.com/ipa-vsp/rqt_frame_editor_plugin.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
```
