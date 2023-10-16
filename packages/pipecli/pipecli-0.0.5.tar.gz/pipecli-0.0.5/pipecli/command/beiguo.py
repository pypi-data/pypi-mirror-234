#! -*- coding: utf-8 -*-
# 根据pid找所属container（docker）

import docker

def find_container(pid):   
    # 创建 Docker 客户端对象
    client = docker.from_env()
      
    # 获取 Docker 容器列表
    containers = client.containers.list()
    
    # 遍历容器，检查是否与指定的 PID 相关联
    for container in containers:
        container_info = container.top()
        container_pid_list = [process[1] for process in container_info['Processes']]
        
        if pid in container_pid_list:
            print(f"容器 {container.name} ({container.id}) 与 PID {pid} 相关联。")
