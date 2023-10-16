## smb_server 模块是smartnotebook 管理服务模块，前端交互服务模块

### notebook 管理
### ds 数据源配置管理
### user 用户管理



## 打包
python setup.py sdist upload -r  http://127.0.0.1:8080/
## 安裝
pip install snb_server -i http://127.0.0.1:8080/
pip install snb_server -i http://127.0.0.1:8080/ --force
## 卸載
pip uninstall snb_server -y

## 運行
python -m snb_server


## 
apt-get install  libnfs-dev/stable

apt search  libnfs