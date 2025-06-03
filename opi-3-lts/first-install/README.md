# Orange Pi 3 LTS — Базовая прошивка и настройка

В этом документе описаны основные шаги по ручной прошивке и первичной настройке Orange Pi 3 LTS с Armbian.  
Цель — получить рабочее устройство с автологином, автоподключением Bluetooth-клавиатуры и окружением GNOME.

---

## Прошивка Armbian через Android

Прошивка выполнялась с телефона, используя терминал и карту памяти.

1. Очистка первых 100 МБ карты памяти:

dd if=/dev/zero of=/dev/block/mmcblk1 bs=1048576 count=100

2. Запись образа Armbian на карту:

dd if=/storage/emulated/0/armbian.img of=/dev/block/mmcblk1 bs=4194304

---

## Настройка локали

Локаль:

ru-UTF-8

---

## Установка mosh

apt install mosh -y

---

## Автологин в TTY

sudo mkdir -p /etc/systemd/system/getty@.service.d

sudo nano /etc/systemd/system/getty@.service.d/autologin.conf

Вставить:

[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin axialix --noclear %I $TERM

---

## Автоматическое подключение Bluetooth-клавиатуры

sudo nano /etc/systemd/system/bt_autoconnect.service

Вставить:

[Unit]
Description=Bluetooth Auto Connect Keyboard
After=bluetooth.service
Requires=bluetooth.service

[Service]
Type=simple
ExecStart=/usr/local/bin/bt_autoconnect.sh
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target

---

sudo nano /usr/local/bin/bt_autoconnect.sh

Вставить:

#!/bin/bash

MAC="DC:2C:26:E9:EE:BB"

until bluetoothctl info "$MAC" | grep -q "Connected: yes"; do
    echo "Пробую подключиться к $MAC..."
    bluetoothctl connect "$MAC"
    sleep 2
done

echo "Подключено."

---

sudo chmod +x /usr/local/bin/bt_autoconnect.sh

sudo systemctl enable bt_autoconnect.service

sudo /usr/local/bin/bt_autoconnect.sh   # запуск вручную для теста

sudo setcap cap_net_raw+ep /usr/bin/bluetoothctl

---

## Установка GNOME

sudo apt update && sudo apt upgrade -y

sudo apt install gnome-session gnome-terminal gdm3 nautilus gnome-control-center gnome-settings-daemon gnome-tweaks -y
