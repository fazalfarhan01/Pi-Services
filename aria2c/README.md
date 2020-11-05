# aria2c
This directory contains files for setting up aria2c web interface as a service

### Setting up the web-ui

1. Download the statis web files from [this github repo](https://github.com/ziahamza/webui-aria2)
2. Place the files in the `/var/www/aria2c/` directory
3. Copy the file [aria2c-webui.conf](website/apache2/aria2c-webui.conf) and paste it into `/etc/apache2/sites-available/`
4. Then run `sudo a2ensite aria2x-webui.conf`
5. This should do it. You'll now have the web-ui enabled at `http://hostname/aria2/`

### Setting up aria2c service

1. Copy the [aria2c.conf](aria2c/aria2c.conf) to `/etc/aria2c/`
2. Copy the [aria2c.service](aria2c/aria2c.service) to `/etc/systemd/system/`
3. Run `sudo systemctl enable aria2c.service`
4. Run `sudo systemctl start aria2c.service`

## Note - Change the following lines in [aria2c.conf](aria2c/aria2c.conf) accordingly
- rpc-secret=\<CHANGE ME\>
- rpc-certificate=\<CHANGE OR COMMENT ME OUT\>
- rpc-private-key=\<CHANGE OR COMMENT ME OUT\>
