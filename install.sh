#!/bin/bash

# SmartMan — Modern Linux Man Page Enhancer Installer
# This script automates the installation of SmartMan and its dependencies.

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  📖 SmartMan — Modern Linux Man Page Enhancer  ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    echo "Please install Python 3.11 or higher and try again."
    exit 1
fi

# 2. Configuration
INSTALL_ROOT=$(pwd)
REPO_URL="https://github.com/ambaskaryash/smartman-cli.git"

# Check if we are in a local repo or running remotely
if [ -f "pyproject.toml" ]; then
    INSTALL_SRC="."
else
    INSTALL_SRC="git+$REPO_URL"
fi

install_with_pipx() {
    echo -e "${BLUE}[1/2] Checking for pipx...${NC}"
    if ! command -v pipx &> /dev/null; then
        echo -e "${YELLOW}pipx not found. Attempting to install pipx...${NC}"
        
        # Detect OS for apt/dnf/pacman
        if command -v apt &> /dev/null; then
            sudo apt update && sudo apt install -y pipx
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y pipx
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python-pipx
        else
            echo -e "${YELLOW}Could not detect package manager. Trying to install pipx via pip...${NC}"
            python3 -m pip install --user pipx || true
        fi
    fi

    echo -e "${BLUE}[2/2] Installing SmartMan from ${YELLOW}$INSTALL_SRC${BLUE}...${NC}"
    pipx ensurepath
    pipx install "$INSTALL_SRC" --force
    
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Successfully installed SmartMan!${NC}"
    echo -e "You might need to restart your terminal or run: ${YELLOW}source ~/.bashrc${NC}"
    echo -e "Then run: ${BLUE}smartman grep${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

install_with_venv() {
    echo -e "${BLUE}[1/2] Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    
    echo -e "${BLUE}[2/2] Installing dependencies and SmartMan...${NC}"
    pip install . --force
    
    echo -e "${GREEN}Successfully installed SmartMan in a virtual environment!${NC}"
    echo -e "To use it, first run: ${YELLOW}source venv/bin/activate${NC}"
    echo -e "Then run: ${BLUE}smartman grep${NC}"
}

setup_shell_integration() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Shell Integration (Highly Recommended)${NC}"
    echo -e "Would you like to alias ${BLUE}'man'${NC} to ${BLUE}'smartman'${NC}?"
    echo -e "This allows you to just type ${YELLOW}man <cmd>${NC} to get the SmartMan experience."
    read -p "Apply this change to your shell config? [y/N]: " alias_choice

    if [[ "$alias_choice" =~ ^[Yy]$ ]]; then
        # Detect shell config file
        if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
            CONF_FILE="$HOME/.zshrc"
        else
            CONF_FILE="$HOME/.bashrc"
        fi

        if grep -q "alias man=" "$CONF_FILE"; then
            echo -e "${YELLOW}An alias for 'man' already exists in $CONF_FILE. Skipping...${NC}"
        else
            echo -e "\n# SmartMan Shell Integration\nalias man='smartman'" >> "$CONF_FILE"
            echo -e "${GREEN}Added alias to $CONF_FILE${NC}"
            echo -e "Please run: ${YELLOW}source $CONF_FILE${NC} or restart your terminal."
        fi
    else
        echo -e "${YELLOW}Skipping shell integration.${NC}"
    fi
}

# Ask user for preference
echo -e "How would you like to install SmartMan?"
echo "1) Global (Recommended - via pipx)"
echo "2) Local  (Virtual Environment - venv)"
read -p "Select an option [1-2]: " choice

case $choice in
    1)
        install_with_pipx
        setup_shell_integration
        ;;
    2)
        install_with_venv
        # We don't alias in venv mode as it's meant to be local
        ;;
    *)
        echo "Invalid option. Defaulting to pipx..."
        install_with_pipx
        setup_shell_integration
        ;;
esac
