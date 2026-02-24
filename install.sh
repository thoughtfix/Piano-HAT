#!/bin/bash

# Piano HAT Modern Installer
# For Raspberry Pi OS (64-bit and 32-bit)
# Python 3 only

set -e

SCRIPT_VERSION="2.0.0"
PRODUCT_NAME="Piano HAT"
LIB_NAME="pianohat"
PYTHON_MIN_VERSION="3.7"
IN_VENV=0

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in a virtual environment
check_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        IN_VENV=1
        info "Running in virtual environment: $VIRTUAL_ENV"
    fi
}

# Check if running on Raspberry Pi
check_platform() {
    if [ ! -f /proc/device-tree/model ]; then
        warn "Not running on Raspberry Pi. Some features may not work."
        return 0
    fi
    
    MODEL=$(cat /proc/device-tree/model 2>/dev/null | tr -d '\0')
    info "Detected: $MODEL"
}

# Check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed!"
        echo "Install with: sudo apt-get install python3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    info "Python version: $PYTHON_VERSION"
    
    # Simple version check (requires 3.7+)
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 7 ]); then
        error "Python $PYTHON_MIN_VERSION or higher is required"
        exit 1
    fi
}

# Check if I2C is enabled
check_i2c() {
    if ! grep -q "^dtparam=i2c_arm=on" /boot/config.txt && \
       ! grep -q "^dtparam=i2c_arm=on" /boot/firmware/config.txt 2>/dev/null; then
        warn "I2C may not be enabled"
        echo ""
        echo "Piano HAT requires I2C to be enabled."
        echo "You can enable it using:"
        echo "  sudo raspi-config"
        echo "  Then: Interface Options -> I2C -> Enable"
        echo ""
        read -p "Continue anyway? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        info "I2C appears to be enabled"
    fi
}

# Install system dependencies
install_dependencies() {
    if [ "$IN_VENV" -eq 1 ]; then
        info "Running in venv, skipping system package installation"
        info "Make sure system has: i2c-tools python3-smbus"
        return 0
    fi
    
    if ! command -v apt-get &> /dev/null; then
        warn "apt-get not found, skipping system dependencies"
        return 0
    fi
    
    info "Installing system dependencies..."
    
    # Update package list
    sudo apt-get update -qq || {
        warn "Failed to update package list"
    }
    
    # Install required system packages
    sudo apt-get install -y \
        python3-pip \
        python3-dev \
        python3-setuptools \
        i2c-tools \
        python3-smbus || {
            error "Failed to install system dependencies"
            exit 1
        }
    
    info "System dependencies installed"
}

# Install Python library
install_library() {
    info "Installing $PRODUCT_NAME library..."
    
    # Handle PEP 668 externally-managed environments
    if [ "$IN_VENV" -eq 0 ]; then
        # Not in a venv, check if system is externally managed
        if python3 -m pip install --dry-run pip 2>&1 | grep -q "externally-managed-environment"; then
            error "This system uses externally-managed Python packages (PEP 668)"
            echo ""
            echo "You have three options:"
            echo "  1. Create a virtual environment (RECOMMENDED):"
            echo "     python3 -m venv --system-site-packages ~/pianohat-env"
            echo "     source ~/pianohat-env/bin/activate"
            echo "     ./install.sh"
            echo ""
            echo "  2. Use --break-system-packages (NOT RECOMMENDED):"
            echo "     Edit this script and add --break-system-packages to pip commands"
            echo ""
            echo "  3. Use system packages only (LIMITED):"
            echo "     May not have latest version"
            echo ""
            exit 1
        fi
    fi
    
    # Check if we're in the repo
    if [ -f "library/pyproject.toml" ]; then
        info "Installing from local source..."
        cd library
        python3 -m pip install --upgrade pip setuptools wheel
        python3 -m pip install -e .
        cd ..
    else
        info "Installing from PyPI..."
        python3 -m pip install --upgrade "$LIB_NAME"
    fi
    
    info "$PRODUCT_NAME library installed"
}

# Install example dependencies (optional)
install_examples() {
    if [ "$INSTALL_EXAMPLES" == "yes" ]; then
        info "Installing example dependencies..."
        python3 -m pip install pygame numpy || {
            warn "Failed to install some example dependencies"
        }
    fi
}

# Copy examples
copy_examples() {
    if [ "$INSTALL_EXAMPLES" == "yes" ]; then
        INSTALL_DIR="$HOME/pianohat-examples"
        
        if [ -d "examples" ]; then
            info "Copying examples to $INSTALL_DIR..."
            mkdir -p "$INSTALL_DIR"
            cp -r examples/* "$INSTALL_DIR/"
            info "Examples copied to $INSTALL_DIR"
        fi
    fi
}

# Test I2C devices
test_i2c() {
    info "Checking for I2C devices..."
    
    if command -v i2cdetect &> /dev/null; then
        # Try both I2C buses
        for bus in 0 1; do
            if sudo i2cdetect -y $bus 2>/dev/null | grep -q "28\|2b"; then
                info "Piano HAT detected on I2C bus $bus"
                return 0
            fi
        done
        warn "Piano HAT not detected on I2C bus. Make sure it's properly connected."
    else
        warn "i2cdetect not available, skipping hardware check"
    fi
}

# Main installation
main() {
    echo ""
    echo "========================================="
    echo "  $PRODUCT_NAME Installer v$SCRIPT_VERSION"
    echo "========================================="
    echo ""
    
    # Parse arguments
    INSTALL_EXAMPLES="no"
    SKIP_DEPS="no"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --examples)
                INSTALL_EXAMPLES="yes"
                shift
                ;;
            --skip-deps)
                SKIP_DEPS="yes"
                shift
                ;;
            -y|--yes)
                # Auto-confirm
                shift
                ;;
            *)
                echo "Unknown option: $1"
                echo "Usage: $0 [--examples] [--skip-deps] [-y]"
                exit 1
                ;;
        esac
    done
    
    # Prompt for examples if not specified
    if [ "$INSTALL_EXAMPLES" == "no" ]; then
        read -p "Install examples and their dependencies? [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            INSTALL_EXAMPLES="yes"
        fi
    fi
    
    # Run checks
    check_venv
    check_platform
    check_python
    check_i2c
    
    # Install
    if [ "$SKIP_DEPS" == "no" ]; then
        install_dependencies
    fi
    
    install_library
    install_examples
    copy_examples
    test_i2c
    
    echo ""
    info "Installation complete!"
    echo ""
    
    if [ "$INSTALL_EXAMPLES" == "yes" ]; then
        info "Examples are in: $HOME/pianohat-examples"
        echo ""
    fi
    
    info "To use Piano HAT in Python:"
    echo "  import pianohat"
    echo ""
    info "Documentation: https://github.com/pimoroni/piano-hat"
    echo ""
}

main "$@"
