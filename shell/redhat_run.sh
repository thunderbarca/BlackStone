#!/usr/bin/env bash

yum remove -y docker docker-common docker-selinux docker-engine
yum install -y yum-utils gcc git libffi-devel device-mapper-persistent-data lvm2 wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel xz-devel
wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
yum makecache fast
yum install -y docker-ce

mkdir /etc/docker
echo '{"registry-mirrors": ["https://registry.docker-cn.com"]}' > /etc/docker/daemon.json
systemctl enable docker
systemctl daemon-reload
systemctl restart docker


# 安装pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
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

# 运行数据库并初始化poc
docker-compose up -d

sleep 3

python3 manage.py makemigrations
python3 manage.py migrate
# 引入数据
python3 manage.py loaddata  doc/sql.json

# 结束
echo "OK"
