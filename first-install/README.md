
# Axialix Lab — OPI Bootstrapping & Custom Setup

Этот раздел репозитория документирует мои шаги по ручной прошивке и первоначальной настройке Orange Pi 3 LTS. Цель — создать стабильную и автономную ARM-машину с автологином, автоподключением Bluetooth-клавиатуры, и окружением GNOME с аппаратным ускорением через Panfrost.

---

## 📦 Прошивка Armbian через Android

> Процесс выполнялся прямо с телефона, используя терминал Android и карту памяти, вставленную в сам телефон.

**Очистка карты памяти:**

```bash
dd if=/dev/zero of=/dev/block/mmcblk1 bs=1048576 count=100

Заливка образа Armbian:

dd if=/storage/emulated/0/armbian.img of=/dev/block/mmcblk1 bs=4194304


---

🛠 Первичная настройка на OPI

Локаль:

locale-gen ru_RU.UTF-8
update-locale LANG=ru_RU.UTF-8

Автологин в TTY:

sudo mkdir -p /etc/systemd/system/getty@.service.d
sudo nano /etc/systemd/system/getty@.service.d/autologin.conf

[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin axialix --noclear %I $TERM


---

🔗 Bluetooth: автоподключение клавиатуры

Создание systemd-сервиса:

sudo nano /etc/systemd/system/bt_autoconnect.service

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

Скрипт автоподключения:

sudo nano /usr/local/bin/bt_autoconnect.sh
sudo chmod +x /usr/local/bin/bt_autoconnect.sh

#!/bin/bash

MAC="XX:XX:XX:XX:XX:XX"  # Заменить на MAC-адрес устройства

until bluetoothctl info "$MAC" | grep -q "Connected: yes"; do
    echo "Пробую подключиться к $MAC..."
    bluetoothctl connect "$MAC"
    sleep 2
done

echo "Подключено."

Разрешения и запуск:

sudo setcap cap_net_raw+ep /usr/bin/bluetoothctl
sudo systemctl enable bt_autoconnect.service
sudo /usr/local/bin/bt_autoconnect.sh  # Тестовый запуск вручную


---

🖥 Установка GNOME

sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  gnome-session gnome-terminal gdm3 nautilus \
  gnome-control-center gnome-settings-daemon \
  gnome-tweaks


---

> Этот набор шагов проверен вручную на Orange Pi 3 LTS с Armbian и может быть использован как основа для автоматизации или деплой-скрипта.
