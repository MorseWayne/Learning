#!/bin/bash

# Default variables
pr_list=""
project_list="window_window_manager"

# Function: Show help message
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -h, --help     Show help message"
    echo "  -t, --target   Specify build target"
    echo "  -f, --fast     Use incremental build"
}

# Function: Install dependencies
install_dependencies() {
    read -p "Install dependencies? (y/n) [n]: " install_deps
    if [[ $install_deps =~ ^[Yy]$ ]]; then
        echo "Installing dependencies..."
        packages="libxinerama-dev libxcursor-dev libxrandr-dev libxi-dev gcc-multilib"
        
        for package in $packages; do
            echo "Installing $package..."
            yes y | sudo apt install "$package"
        done
        echo "Dependencies installation completed!"
    else
        echo "Skipping dependencies installation..."
    fi
}

# Function: Clean and download prebuilts
clean_and_download() {
    read -p "Clean output and prebuilts, then download new prebuilts? (y/n) [n]: " clean_and_download
    if [[ $clean_and_download =~ ^[Yy]$ ]]; then
        echo "Cleaning output and prebuilts..."
        rm -rf out
        if [ -z "$pr_list" ]; then
            rm -rf prebuilts/ohos-sdk
            rm -rf prebuilts/build-tools/common/oh-command-line-tools
        fi
        
        echo "Downloading prebuilts..."
        bash build/prebuilts_download.sh
        rm -rf ./prebuilts/*.tar.gz ./prebuilt/windows
    fi
}

# Function: Set build target
set_build_target() {
    read -p "Enter build target (default: 'TDD$project_list'): " user_target
    if [[ -n $user_target ]]; then
        echo "$user_target"
    else
        echo "foundation/window/window_manager/wmserver:test"
    fi
}

# Function: Set environment variables
set_environment() {
    export CCACHE_MAXSIZE=100G
    export CCACHE_BASE="${PWD}"
    export NO_DEVTOOL=1
    export CCACHE_LOG_SUFFIX="dayu200-arm32"
    export CCACHE_NOHASHDIR="true"
    export CCACHE_SLOPPINESS="include_file_ctime"
}

# Function: Build command
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

# Function: Execute build
do_build() {
    local build_target=$1
    
    read -p "Use incremental build? (y/n) [y]: " incremental_build
    echo "Starting build..."
    
    local build_cmd=$(build_command "$build_target" "$incremental_build")
    eval "$build_cmd"
    
    echo "Build completed!"
}

# Main function
main() {
    # Parse command line arguments
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
                echo "Unknown parameter: $1"
                show_help
                exit 1
            ;;
        esac
    done
    
    # Execute main process
    install_dependencies
    clean_and_download
    
    # If build target not specified in command line, ask user
    if [[ -z $build_target ]]; then
        build_target=$(set_build_target)
    fi
    
    set_environment
    do_build "$build_target"
}

# Execute main function
main "$@"
