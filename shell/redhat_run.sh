#!/usr/bin/env bash

# shellcheck disable=SC2046
# 获取当前的绝对路径
current_path=$(pwd)

yum remove -y docker docker-common docker-selinux docker-engine
yum install -y yum-utils epel-release
yum install -y supervisor gcc pcre-devel git libffi-devel device-mapper-persistent-data lvm2 wget zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel xz-devel
wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
yum makecache fast
yum install -y docker-ce

mkdir /etc/docker
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

# 更换为pypi阿里镜像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ pip -U
pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 安装docker-compose
pip3 install docker-compose daphne

# 安装pipenv
#pip3 install pipenv
#pipenv install

# 安装依赖
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 运行数据库并初始化poc
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

rm -rf /usr/local/nginx/conf/nginx.conf
cp -f doc/config/nginx.conf /usr/local/nginx/conf/nginx.conf
cp doc/config/nginx_supervisor.conf /etc/supervisord.d/nginx.ini
cp doc/config/daphne_supervisor.conf /etc/supervisord.d/daphne.ini

systemctl enable supervisord # 开机自启动
systemctl start supervisord # 启动supervisord服务
supervisorctl reload

# 收尾工作
rm -rf /tmp/nginx*

# 结束
echo "OK"
