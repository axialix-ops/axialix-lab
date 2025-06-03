#!/bin/bash

set -e

echo "[1/6] Обновление системы..."
sudo apt update && sudo apt upgrade -y

echo "[2/6] Удаляю Xorg и fbturbo (если был)..."
sudo apt purge -y xserver-* x11-* xinit x11-utils x11-xserver-utils xserver-xorg-video-fbturbo* || true
sudo apt autoremove -y

echo "[3/6] Установка GNOME Wayland, Mesa и Panfrost..."
sudo apt install -y \
gnome-session gdm3 gnome-shell gnome-control-center gnome-terminal nautilus \
gnome-tweaks gnome-shell-extension-prefs gnome-settings-daemon \
fonts-dejavu fonts-noto-color-emoji \
mesa-va-drivers mesa-vdpau-drivers mesa-vulkan-drivers \
libgl1-mesa-dri vulkan-tools glmark2 \
pulseaudio pavucontrol \
network-manager network-manager-gnome \
policykit-1-gnome gvfs gvfs-backends gvfs-fuse

echo "[4/6] Установка мультимедиа (GPU-декод)..."
sudo apt install -y \
ffmpeg vlc mpv \
gstreamer1.0-vaapi gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly

echo "[5/6] Установка полезных утилит..."
sudo apt install -y git build-essential htop neofetch inxi

echo "[6/6] Переключение GDM в Wayland (по умолчанию)..."
sudo sed -i 's/^#WaylandEnable=false/WaylandEnable=true/' /etc/gdm3/daemon.conf

echo "[Готово] Перезагрузи систему: sudo reboot"
