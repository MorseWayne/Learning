#!/bin/bash

# 设置默认变量
pr_list=""
project_list="window_window_manager"

# 函数：显示帮助信息
show_help() {
    echo "使用方法: $0 [选项]"
    echo "选项:"
    echo "  -h, --help     显示帮助信息"
    echo "  -t, --target   指定编译目标"
    echo "  -f, --fast     使用增量编译"
}

# 函数：安装依赖包
install_dependencies() {
    echo "安装依赖包..."
    local packages=(
        "libxinerama-dev"
        "libxcursor-dev"
        "libxrandr-dev"
        "libxi-dev"
        "gcc-multilib"
    )
    
    for package in "${packages[@]}"; do
        echo "安装 $package..."
        yes y | sudo apt install "$package"
    done
}

# 函数：清理和下载预构建文件
clean_and_download() {
    read -p "是否清理输出目录和预构建文件，并重新下载预构建文件？(y/n): " clean_and_download
    if [[ $clean_and_download =~ ^[Yy]$ ]]; then
        echo "清理输出目录和预构建文件..."
        rm -rf out
        if [ -z "$pr_list" ]; then
            rm -rf prebuilts/ohos-sdk
            rm -rf prebuilts/build-tools/common/oh-command-line-tools
        fi
        
        echo "下载预构建文件..."
        bash build/prebuilts_download.sh
        rm -rf ./prebuilts/*.tar.gz ./prebuilt/windows
    fi
}

# 函数：设置编译目标
set_build_target() {
    read -p "请输入编译目标(直接回车将使用默认值 'TDD$project_list'): " user_target
    if [[ -n $user_target ]]; then
        echo "$user_target"
    else
        echo "TDD$project_list"
    fi
}

# 函数：设置环境变量
set_environment() {
    export CCACHE_MAXSIZE=100G
    export CCACHE_BASE="${PWD}"
    export NO_DEVTOOL=1
    export CCACHE_LOG_SUFFIX="dayu200-arm32"
    export CCACHE_NOHASHDIR="true"
    export CCACHE_SLOPPINESS="include_file_ctime"
}

# 函数：构建编译命令
build_command() {
    local build_target=$1
    local is_incremental=$2
    
    local cmd="./build.sh --product-name rk3568 \
           --ccache \
           --build-target $build_target \
           --gn-args enable_notice_collection=false \
           --disable-package-image \
           --gn-flags=\"--export-compile-commands\" \
           --gn-args skip_generate_module_list_file=true \
           --disable-part-of-post-build output_part_rom_status \
           --disable-part-of-post-build get_warning_list \
           --disable-part-of-post-build compute_overlap_rate \
           --get-warning-list=false \
           --compute-overlap-rate=false \
           --deps-guard=true \
           --gn-args use_thin_lto=false \
           --ninja-args=-j16 \
           --gn-args archive_ndk=false \
           --gn-args enable_process_notice=false"

    if [[ $is_incremental =~ ^[Yy]$ ]]; then
        cmd="$cmd --fast-rebuild"
    fi
    
    echo "$cmd"
}

# 函数：执行编译
do_build() {
    local build_target=$1
    
    read -p "是否需要增量编译？(y/n): " incremental_build
    echo "开始编译..."
    
    local build_cmd=$(build_command "$build_target" "$incremental_build")
    eval "$build_cmd"
    
    echo "编译完成！"
}

# 主函数
main() {
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -t|--target)
                build_target="$2"
                shift 2
                ;;
            -f|--fast)
                incremental_build="y"
                shift
                ;;
            *)
                echo "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # 执行主要流程
    install_dependencies
    clean_and_download
    
    # 如果命令行没有指定编译目标，则询问用户
    if [[ -z $build_target ]]; then
        build_target=$(set_build_target)
    fi
    
    set_environment
    do_build "$build_target"
}

# 执行主函数
main "$@"
