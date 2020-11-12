# Configuration Files for Transmission Daemon
1. Stop the __transmission-service__
    ```BASH
    sudo systemctl stop transmission-daemon.service
    ```
2. Paste the [settings.json](./settings.json) file in `~/.config/transmission-daemon` directory.
    ```BASH
    mkdir -p ~/.config/transmission-daemon
    cp settings.json ~/.config/transmission-daemon
    sudo chown -R pi:pi ~/.config/transmission-daemon
    ```
3. Change the user with which __transmission__ runs by changing the line which startes with `USER=` in `/etc/init.d/transmission-daemon` to `USER=pi`
    ```BASH
    sudo nano /etc/init.d/transmission-daemon
    ```
4. Change the user is service files to `pi` as well.

    ```BASH
    sudo systemctl edit transmission-daemon.service
    ```
    
    Add the following line to `transmission-daemon.service`
    ```BASH
    [Service]
    User=pi
    ```
    
