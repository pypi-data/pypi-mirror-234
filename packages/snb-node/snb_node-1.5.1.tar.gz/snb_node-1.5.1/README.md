# 打包
- python setup.py sdist upload  -r  http://127.0.0.1:8080/
# 安裝
pip install snb_node  -i http://127.0.0.1:8080/ --user --user
# 卸载
pip uninstall snb_node -y
# 运行测试
python -m snb_node

pypi-server run -p 801 /home/pipserver -P . -a . -o
1. snb_plugin
    ```
   python3 setup.py sdist upload -r http://172.30.81.116:801/
   ``` 

##### pipreqs  --encoding utf8 .  --force
1. 检查requirements.txt 中的波浪线 ，去除
2. 包冲突，
3. pycryptodome 代替 pycrypto


## docker build -t snb/node:v1 .
## docker run -p 8000:8888 -v /var/lib/jenkins/workspace/snb_node:/snb_node --name snb-node snb/node:v1

## 多核测试
docker run -p 8888:8888 -v /data02/snb-node-m:/home --name snb-node-m snb-node:mkernel221216

## nginx服务  
### 容器网络模式--net :host	容器没有自己的任何独立的网络资源(比如：容器的IP、网卡和端口)，完全和宿主机共享网络空间	弊端：同一个端口只能同时被一个容器服务绑定
docker run --net=host  -v /home/nginx/snb_nginx.conf:/etc/nginx/nginx.conf -v /var/lib/jenkins/workspace/snb_web/dist:/usr/share/nginx/html --name snb-nginx nginx:1.17.10

# Release  2023/10/07 
docker stop snb-node-231007 
docker rm snb-node-231007 
docker rmi snb/node:v1.5
docker build -t snb/node:v1.5 . --no-cache
docker run -p 8000:8888 -v /data01/snb-node/home:/home --name snb-node-231007 snb/node:v1.5