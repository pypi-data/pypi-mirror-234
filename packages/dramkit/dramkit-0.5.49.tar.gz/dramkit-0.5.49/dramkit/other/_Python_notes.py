# -*- coding: utf-8 -*-

# Python笔记

# 参考：
# pip命令：https://blog.csdn.net/fancunshuai/article/details/124994040

py_notes = \
r'''
# spyder启动失败查找原因
在cmd中运行spyder，会看到报错信息

# conda查看镜像
conda config --show-sources

# conda设置镜像
# 首先用命令创建配置文件（或手动创建）.condarc：
conda config --set show_channel_urls yes # 设置搜索时显示通道地址
# 在.condarc中添加常用镜像源：
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
# conda清除索引缓存使新配置生效
conda clean -i
# conda命令行添加镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# pip查看镜像源
pip config list

# pip安装时带临时镜像
pip install pkgname -i https://mirror.baidu.com/pypi/simple
pip install pkgname -i https://pypi.org/simple # PYPI官方镜像

# pip设置镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 在pip.ini（windows）中设置镜像
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn

# pip常用镜像列表
https://pypi.tuna.tsinghua.edu.cn/simple # 清华
https://pypi.mirrors.ustc.edu.cn/simple # 中科大
https://pypi.hustunique.com/ # 华中科大
https://pypi.hustunique.com/ #  山东理工
https://mirror.baidu.com/pypi/simple/ # 百度
https://mirrors.aliyun.com/pypi/simple/ # 阿里
http://mirrors.sohu.com/Python/ # 搜狐
https//pypi.doubanio.com/simple # 豆瓣

# conda查看已有环境
conda env list
conda info -e

# conda创建虚拟环境
conda create -n envname python=x.x

# conda激活虚拟环境
conda activate envname

# conda退出虚拟环境
conda deactivate

# conda删除环境：
conda remove -n envname --all
# conda删除虚拟环境中的包（未验证）：
conda remove --name envname pkgname

# conda虚拟环境安装spyder
conda install spyder

# conda虚拟环境安装notebook
conda install nb_conda

# jupyter notebook添加支持conda虚拟环境
# 1. 打开终端并激活conda虚拟环境
conda activate your_env_name
# 2. 在终端中输入以下命令以安装ipykernel：
conda install ipykernel
# 3. 输入以下命令以将ipykernel添加到Jupyter Notebook中：
python -m ipykernel install --user --name=your_env_name
# 4. 最后，输入以下命令以启动Jupyter Notebook：
jupyter notebook

# conda修改默认进入的环境
conda config --set env_prompt '({env_name})'
# 例如:
conda config --set env_prompt '(py38)'

# conda删除缓存
conda clean --all

# pip删除缓存
pip cache purge

# pip安装忽略依赖
--no-dependencies
 
# pip强制重新安装所有软件包，即使它们已经是最新的
--force-reinstall

# pip批量安装文件夹下所有的whl包
pip install /dirpath/*.whl

# jupyter notebook cell转为markdown快捷键：Esc(命令模式)+m

# linux下安装talib
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
./configure --prefix=/usr
make
sudo make install
pip install TA-Lib

# jupyter导出笔记，隐藏源代码
pip install jupyter_contrib_nbextensions
jupyter nbconvert --to html --no-input xxx.ipynb

# '''