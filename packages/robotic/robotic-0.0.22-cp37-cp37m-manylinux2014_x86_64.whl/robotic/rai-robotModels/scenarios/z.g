world: {  }
table(world): { rel: [0, 0, 0.6, 1, 0, 0, 0], shape: ssBox, size: [2.5, 2.5, 0.1, 0.02], color: [0.3, 0.3, 0.3], contact: 1, logical: {  }, friction: 0.1 }
cameraTop(world): { rel: [-0.01, -0.2, 1.8, 0.965926, 0.258819, 0, 0], shape: marker, size: [0.1], color: [0.8, 0.8, 0.8], focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100] }
l_panda_base(table): { rel: [0, -0.2, 0.05, 0.707107, 0, 0, 0.707107], joint: rigid, multibody: True }
l_panda_link0(l_panda_base): {  }
l_panda_link0_0(l_panda_link0): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link0.ply>, visual: True }
l_panda_joint1_origin(l_panda_link0): { rel: [0, 0, 0.333, 1, 0, 0, 0] }
l_panda_coll0(l_panda_link0): { rel: [-0.04, 0, 0.03, 0.707107, 0, 0.707107, 0], shape: capsule, size: [0.1, 0.15], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_coll0b(l_panda_link0): { rel: [-0.2, -0.12, 0, 0.707107, 0, 0.707107, 0], shape: capsule, size: [0.2, 0.1], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_joint1(l_panda_joint1_origin): { joint: hingeZ, limits: [-2.8973, 2.8973, 2.175, -1, 87, 2.175, -1, 87], ctrl_limits: [2.175, -1, 87] }
l_panda_link1(l_panda_joint1): {  }
l_panda_coll1(l_panda_joint1): { rel: [0, 0, -0.15, 1, 0, 0, 0], shape: capsule, size: [0.2, 0.08], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_link1_0(l_panda_link1): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link1.ply>, visual: True }
l_panda_joint2_origin(l_panda_link1): { rel: [0, 0, 0, 0.707107, -0.707107, 0, 0] }
l_panda_joint2(l_panda_joint2_origin): { rel: [0, 0, 0, 0.968912, 0, 0, -0.247404], joint: hingeZ, limits: [-1.7628, 1.7628, 2.175, -1, 87, 2.175, -1, 87], ctrl_limits: [2.175, -1, 87] }
l_panda_link2(l_panda_joint2): {  }
l_panda_coll2(l_panda_joint2): { shape: capsule, size: [0.12, 0.11], color: [1, 1, 1, 0.2], contact: -2 }
bellybutton(l_panda_joint2): { rel: [0.0545, 0, 0.0184, 0.707107, 0, 0.707107, 0], shape: cylinder, size: [0.001, 0.0125], color: [0, 0, 1] }
l_panda_link2_0(l_panda_link2): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link2.ply>, visual: True }
l_panda_joint3_origin(l_panda_link2): { rel: [0, -0.316, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint3(l_panda_joint3_origin): { joint: hingeZ, limits: [-2.8973, 2.8973, 2.175, -1, 87, 2.175, -1, 87], ctrl_limits: [2.175, -1, 87] }
l_panda_link3(l_panda_joint3): {  }
l_panda_coll3(l_panda_joint3): { rel: [0, 0, -0.15, 1, 0, 0, 0], shape: capsule, size: [0.2, 0.08], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_link3_0(l_panda_link3): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link3.ply>, visual: True }
l_panda_joint4_origin(l_panda_link3): { rel: [0.0825, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint4(l_panda_joint4_origin): { rel: [0, 0, 0, 0.540302, 0, 0, -0.841471], joint: hingeZ, limits: [-3.0718, -0.0698, 2.175, -1, 87, 2.175, -1, 87], ctrl_limits: [2.175, -1, 87] }
l_panda_link4(l_panda_joint4): {  }
l_panda_coll4(l_panda_joint4): { shape: capsule, size: [0.12, 0.08], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_link4_0(l_panda_link4): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link4.ply>, visual: True }
l_panda_joint5_origin(l_panda_link4): { rel: [-0.0825, 0.384, 0, 0.707107, -0.707107, 0, 0] }
l_panda_joint5(l_panda_joint5_origin): { joint: hingeZ, limits: [-2.8973, 2.8973, 2.61, -1, 12, 2.61, -1, 12], ctrl_limits: [2.61, -1, 12] }
l_panda_link5(l_panda_joint5): {  }
l_panda_coll5(l_panda_joint5): { rel: [0, 0.02, -0.2, 1, 0, 0, 0], shape: capsule, size: [0.22, 0.09], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_link5_0(l_panda_link5): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link5.ply>, visual: True }
l_panda_joint6_origin(l_panda_link5): { rel: [0, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint6(l_panda_joint6_origin): { rel: [0, 0, 0, 0.540302, 0, 0, 0.841471], joint: hingeZ, limits: [0.5, 3, 2.61, -1, 12], ctrl_limits: [2.61, -1, 12] }
l_panda_link6(l_panda_joint6): {  }
l_panda_coll6(l_panda_joint6): { rel: [0, 0, -0.04, 1, 0, 0, 0], shape: capsule, size: [0.1, 0.07], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_link6_0(l_panda_link6): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link6.ply>, visual: True }
l_panda_joint7_origin(l_panda_link6): { rel: [0.088, 0, 0, 0.707107, 0.707107, 0, 0] }
l_panda_joint7(l_panda_joint7_origin): { rel: [0, 0, 0, 0.968912, 0, 0, -0.247404], joint: hingeZ, limits: [-2.8973, 2.8973, 2.61, -1, 12, 2.61, -1, 12], ctrl_limits: [2.61, -1, 12] }
l_panda_link7(l_panda_joint7): {  }
l_panda_coll7(l_panda_joint7): { rel: [0, 0, 0.01, 1, 0, 0, 0], shape: capsule, size: [0.1, 0.07], color: [1, 1, 1, 0.2], contact: -2 }
l_gripper(l_panda_joint7): { rel: [-2.69422e-17, 0, 0.22, 2.34326e-17, 0.92388, 0.382683, 5.65713e-17], shape: marker, size: [0.03], color: [0.9, 0.9, 0.9], logical: { is_gripper: True } }
cameraWrist(l_panda_joint7): { rel: [0.0587342, -0.0132086, 0.157056, 0.0118089, 0.376934, -0.925754, -0.0275978], shape: camera, size: [0.1], color: [0.8, 0.8, 0.8], focalLength: 0.895, width: 640, height: 360, zRange: [0.1, 10] }
l_panda_link7_0(l_panda_link7): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/link7.ply>, visual: True }
l_panda_joint8_origin(l_panda_link7): { rel: [0, 0, 0.107, 1, 0, 0, 0] }
l_panda_joint8(l_panda_joint8_origin): {  }
l_panda_link8(l_panda_joint8): {  }
l_panda_hand_joint_origin(l_panda_link8): { rel: [0, 0, 0, 0.92388, 0, 0, -0.382683] }
l_panda_hand_joint(l_panda_hand_joint_origin): {  }
l_panda_hand(l_panda_hand_joint): {  }
l_palm(l_panda_hand_joint): { rel: [0, 0, 0, 0.707107, 0.707107, 0, 0], shape: capsule, size: [0.14, 0.07], color: [1, 1, 1, 0.2], contact: -3 }
l_panda_hand_0(l_panda_hand): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/hand.ply>, visual: True }
l_panda_finger_joint1_origin(l_panda_hand): { rel: [0, 0, 0.0584, 1, 0, 0, 0] }
l_panda_finger_joint2_origin(l_panda_hand): { rel: [0, 0, 0.0584, 1, 0, 0, 0] }
l_panda_finger_joint1(l_panda_finger_joint1_origin): { rel: [0, 0.05, 0, 1, 0, 0, 0], joint: transY, limits: [0, 0.04, 0.2, -1, 20, 0.2, -1, 20], ctrl_limits: [0.2, -1, 20], joint_active: False }
l_panda_finger_joint2(l_panda_finger_joint2_origin): { rel: [-0, -0.05, -0, -1, 0, 0, 0], joint: transY, joint_scale: -1, limits: [0, 0.04, 0.2, -1, 20, 0.2, -1, 20], mimic: "l_panda_finger_joint1", ctrl_limits: [0.2, -1, 20] }
l_panda_leftfinger(l_panda_finger_joint1): {  }
l_finger1(l_panda_finger_joint1): { rel: [0, 0.028, 0.035, 1, 0, 0, 0], shape: capsule, size: [0.02, 0.03], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_rightfinger(l_panda_finger_joint2): {  }
l_finger2(l_panda_finger_joint2): { rel: [0, -0.028, 0.035, 1, 0, 0, 0], shape: capsule, size: [0.02, 0.03], color: [1, 1, 1, 0.2], contact: -2 }
l_panda_leftfinger_0(l_panda_leftfinger): { shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/finger.ply>, visual: True }
l_panda_rightfinger_0(l_panda_rightfinger): { rel: [0, 0, 0, -1.03412e-13, 0, 0, 1], shape: mesh, color: [0.9, 0.9, 0.9], mesh: </home/mtoussai/git/rai-python/rai-robotModels/panda/meshes/visual/finger.ply>, visual: True }