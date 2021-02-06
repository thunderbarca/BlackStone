#!/usr/bin/env bash

# 判断是否为root用户
if [[ $EUID -ne 0 ]]; then
    echo "请使用root账户运行该脚本"
    exit 1
fi

# shellcheck disable=SC2046
# 获取当前的绝对路径
current_path=$(pwd)

# 安装docker-ce和依赖
curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/debian/gpg | apt-key add -
echo 'deb [arch=amd64] https://mirrors.ustc.edu.cn/docker-ce/linux/debian buster stable' > /etc/apt/sources.list.d/docker.list
apt update && apt install docker-ce -y && apt install build-essential supervisor libffi-dev zlib1g-dev gcc libbz2-dev libpcre3 libpcre3-dev libssl-dev libreadline-dev libsqlite3-dev -y

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
# shellcheck disable=SC1090
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
pip3 install docker-compose daphne

# 安装pipenv
#pip3 install pipenv
#pipenv install

# 安装依赖
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple


# 运行数据库并初始化
docker-compose up -d

# 下载测试题目
docker pull ap0llo/transcript:latest
docker pull ap0llo/easy:latest

sleep 3

python3 manage.py makemigrations
python3 manage.py migrate
# 引入数据
python3 manage.py loaddata  doc/sql.json

# 部署nginx服务器
groupadd nginx
useradd -g nginx -s "/usr/sbin/nologin" nginx
wget http://nginx.org/download/nginx-1.18.0.tar.gz -P /tmp
tar -zxvf /tmp/nginx-1.18.0.tar.gz -C /tmp
# shellcheck disable=SC2164
cd /tmp/nginx-1.18.0
./configure --prefix=/usr/local/nginx \
--user=nginx \
--group=nginx \
--with-http_ssl_module \
--with-http_v2_module \
--with-http_realip_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-pcre \
--with-stream \
--with-stream_ssl_module \
--with-stream_realip_module
make
make install

# shellcheck disable=SC2164
cd "$current_path"
# shellcheck disable=SC2230
daphne_path=$(which daphne)

sed -i "s@/opt/docker/Finisher@$current_path@g" doc/config/nginx.conf
sed -i "s@/opt/docker/Finisher@$current_path@g" doc/config/daphne_supervisor.conf
sed -i "s@keyword@$daphne_path@g" doc/config/daphne_supervisor.conf
sed -i "s@dev@prod@g" asgi.py

cp doc/config/nginx.conf /usr/local/nginx/conf/nginx.conf
cp doc/config/nginx_supervisor.conf /etc/supervisor/conf.d/nginx.conf
cp doc/config/daphne_supervisor.conf /etc/supervisor/conf.d/daphne.conf

supervisorctl reload

# 收尾工作
rm -rf /tmp/nginx*

# 结束
echo "OK"
