# OpenHarmony主干编译指南

## 1 环境准备

### 1.1 虚拟机准备

1. 下载虚拟机宿主机软件 [Vmware](https://softwareupdate.vmware.com/cds/vmw-desktop/ws/17.6.1/24319023/windows/core/) 完成安装；

2. 下载[Ubuntu 22.04](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)版本lts镜像;

3. 完成虚拟机的安装，虚拟机安装时请保证设置内存不低于**16GB**，磁盘空间不少于**200GB**；

   虚拟机的安装步骤这里不再做过多赘述，个人虚拟机配置截图如下图：

   ![vmware_configuration](figures\vmware_configuration.png)

### 1.2 虚拟机配置

#### 1.2.1 shell配置

终端输入命令: `ls -l /bin/sh`
显示结果是：` /bin/sh -> dash`
需要执行以下命令：

```bash
sudo dpkg-reconfigure dash
```

然后选择**No**

#### 1.2.2 替换镜像源

配置 `/etc/apt/sources.list`，替换为下面的内容，更多详情可参考[ustc镜像信息](https://mirrors.ustc.edu.cn/repogen/)
然后执行 `sudo apt update`

```bash
deb https://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-security main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse

## Not recommended
# deb https://mirrors.ustc.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ jammy-proposed main restricted universe multiverse
```

#### 1.2.3 安装必备工具

```bash
sudo apt-get install binutils binutils-dev git git-lfs gnupg flex bison gperf build-essential zip curl zlib1g-dev   libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z1-dev ccache libgl1-mesa-dev libxml2-utils xsltproc unzip m4 bc gnutls-bin python3 python3-pip ruby genext2fs device-tree-compiler make libffi-dev e2fsprogs pkg-config perl openssl libssl-dev libelf-dev libdwarf-dev u-boot-tools mtd-utils cpio doxygen liblz4-tool openjdk-8-jre gcc g++ texinfo dosfstools mtools default-jre default-jdk libncurses5 apt-utils wget scons python3-distutils tar rsync git-core libxml2-dev lib32z-dev grsync xxd libglib2.0-dev libpixman-1-dev kmod jfsutils reiserfsprogs xfsprogs squashfs-tools pcmciautils quota ppp libtinfo-dev libtinfo5 libncurses5-dev libncursesw5 libstdc++6 gcc-arm-none-eabi vim ssh locales libxinerama-dev libxcursor-dev libxrandr-dev libxi-dev
```

```bash
sudo apt-get install gcc-arm-linux-gnueabi gcc-9-arm-linux-gnueabi
```

#### 1.2.4 配置pip软件源

```bash
mkdir ~/.pip
pip3 config set global.index-url https://mirrors.huaweicloud.com/repository/pypi/simple
pip3 config set global.trusted-host mirrors.huaweicloud.com
pip3 config set global.timeout 120
```

#### 1.2.5 git相关配置

```bash
# 安装git-lfs
sudo apt install git-lfs

# 安装repo和requests
wget https://gitee.com/oschina/repo/raw/fork_flow/repo-py3
sudo mv repo-py3 /usr/local/bin/repo
sudo chmod a+x /usr/local/bin/repo
pip3 install -i https://repo.huaweicloud.com/repository/pypi/simple requests

# 配置自己的git账户名和邮箱
git config --global user.email "your_name"
git config --global user.name "your_email@huawei.com"
git config --global credential.helper store
git config --global --add safe.directory "*"
```

### 1.3 拉取master分支代码

选择一个本地目录
```bash
repo init -u https://gitee.com/openharmony/manifest.git -b master --no-repo-verify
repo sync -c
repo start master --all
repo forall -c 'git lfs pull'
bash build/prebuilts_download.sh
```

## 2 TDD编译

源码根目录下创建一个bash脚本，例如`build_tdd.sh`，内容如下：

```bash
#!/bin/bash

# 设置变量
pr_list=""

# 你需要编译的项目名
project_list="window_window_manager"

build_target=""

# 清理输出目录和预构建文件
echo "清理输出目录和预构建文件..."
rm -rf out
if [ -z "$pr_list" ]; then
    rm -rf prebuilts/ohos-sdk
    rm -rf prebuilts/build-tools/common/oh-command-line-tools
fi

# 安装依赖包
echo "安装依赖包..."
yes y | sudo apt install libxinerama-dev libxcursor-dev libxrandr-dev libxi-dev
yes y | sudo apt install gcc-multilib

# 下载预构建文件
echo "下载预构建文件..."
bash build/prebuilts_download.sh
rm -rf ./prebuilts/*.tar.gz ./prebuilt/windows

# 设置编译目标
if [[ -z $project_list ]]; then
    build_target='build/ohos/packages:build_all_test_pkg'
else
    build_target="TDD$project_list"
fi

# 设置环境变量
echo "设置环境变量..."
export CCACHE_MAXSIZE=100G
export CCACHE_BASE="${PWD}"
export NO_DEVTOOL=1
export CCACHE_LOG_SUFFIX="dayu200-arm32"
export CCACHE_NOHASHDIR="true"
export CCACHE_SLOPPINESS="include_file_ctime"

# 开始编译
echo "开始编译..."
./build.sh --product-name rk3568 \
           --ccache \
           --build-target $build_target \
           --gn-args enable_notice_collection=false \
           --disable-package-image \
           --gn-args enable_lto_O0=true \
           --gn-args skip_generate_module_list_file=true \
           --disable-part-of-post-build output_part_rom_status \
           --disable-part-of-post-build get_warning_list \
           --disable-part-of-post-build compute_overlap_rate \
           --get-warning-list=false \
           --compute-overlap-rate=false \
           --deps-guard=true \
           --gn-args use_thin_lto=false \
           --ninja-args=-j60 \
           --gn-args archive_ndk=false \
           --gn-args enable_process_notice=false

echo "编译完成！"
```

如果需要更改项目，请修改变量 `project_list`（`gitee`上的项目名，多个项目使用逗号分割, 然后执行`sh build_tdd.sh`开始编译，接下来需要的就是漫长的等待了~

## 3 参考文档

[OpenHarmony 编译避坑](https://forums.openharmony.cn/forum.php?mod=viewthread&tid=2075)
[O喷Harmony 4.0编译指南](https://forums.openharmony.cn/forum.php?mod=viewthread&tid=897)

