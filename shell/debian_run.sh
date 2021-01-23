#!/usr/bin/env bash

# 判断是否为root用户
if [[ $EUID -ne 0 ]]; then
    echo "请使用root账户运行该脚本"
    exit 1
fi

# 安装docker-ce和依赖
curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/debian/gpg | apt-key add -
echo 'deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/debian buster stable' > /etc/apt/sources.list.d/docker.list
apt update && apt install docker-ce -y && apt install build-essential libffi-dev zlib1g-dev libbz2-dev libssl-dev libreadline-dev libsqlite3-dev -y

# 更换为中科大仓库镜像
echo '{"registry-mirrors": ["https://registry.docker-cn.com"]}' > /etc/docker/daemon.json
systemctl enable docker
systemctl daemon-reload
systemctl restart docker

# 安装pyenv
git clone https://gitee.com/mirrors/pyenv.git ~/.pyenv
# shellcheck disable=SC2129
# shellcheck disable=SC2016
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
# shellcheck disable=SC2016
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# shellcheck disable=SC2016
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

if [ ! -f "$HOME/.pyenv/cache/Python-3.9.1.tar.xz" ]; then
# 使用pyenv淘宝镜像源安装python3.9.1
wget https://npm.taobao.org/mirrors/python/3.9.1/Python-3.9.1.tar.xz -P ~/.pyenv/cache/;pyenv install 3.9.1
fi

pyenv global 3.9.1

# 更换为pypi清华镜像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pip -U
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 安装docker-compose
pip3 install docker-compose

# 安装pipenv
#pip3 install pipenv
#pipenv install

# 安装依赖
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


# 运行数据库并初始化
docker-compose up -d

sleep 3

python3 manage.py makemigrations
python3 manage.py migrate
# 引入数据
python3 manage.py loaddata  doc/sql.json

# 结束
echo "OK"
