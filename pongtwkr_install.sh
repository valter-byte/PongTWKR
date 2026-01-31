#!/bin/bash
INSTALL_DIR="/usr/local/share/pongtwkr"
BIN_LINK="/usr/local/bin/pongtwkr"
echo "🚀 Welcome to the PongTWKR v0.8 Installer!"
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please re-run this with sudo..."
  exit
fi
echo "⌛ We are now starting with the installation... Hold tight!"
echo "📦 Detecting OS and installing dependencies..."

if command -v apt &> /dev/null; then
    apt update && apt install -y -qq ethtool python3-pip git
elif command -v pacman &> /dev/null; then
    pacman -Sy --noconfirm --needed ethtool python-pip git
elif command -v dnf &> /dev/null; then
    dnf install -y -q ethtool python3-pip git
else
    echo "⚠️ Distro unknown. You'll have to manually install psutil and ethtool..."
fi
echo "📥 Fetching the source from the repository..."
rm -rf /tmp/pong_tmp
git clone https://github.com/valter-byte/PongTWKR.git /tmp/pong_tmp
echo "🚚 Moving files to $INSTALL_DIR..."
rsync -a --exclude='README.md' \
        --exclude='LICENSE' \
        --exclude='CODE_OF_CONDUCT.md' \
        --exclude='CODE-OF-CONDUCT.md' \
        --exclude='CONTRIBUTING.md' \
        --exclude='docs/' \
        --exclude='.git/' \
        --exclude=".gitignore/"\
        --exclude="old_source/"\
        /tmp/pong_tmp/ "$INSTALL_DIR/"


echo "🔐 Setting permissions..."
chmod +x "$INSTALL_DIR/pongtwkr.py"
ln -sf "$INSTALL_DIR/pongtwkr.py" "$BIN_LINK"
echo "--------------------------------------------------"
echo "✅ PongTWKR v0.8 INSTALLED!"
echo "🚀 Run it with: sudo pongtwkr"
echo "ℹ️ Need help? Check documentation at the repository!"
echo "⚠️ Note: This v0.8 version does NOT include GPU Tweaks"
echo "💖 If you enjoy PongTWKR, please consider giving us a star or feedback. Any error you'll bring to us, we will fix it."
echo "--------------------------------------------------"

rm -rf /tmp/pong_tmp
