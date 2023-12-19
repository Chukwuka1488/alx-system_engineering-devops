### Firewall
1. Check if ufw is installed and inactive
```sh
sudo apt-get update
sudo apt-get install ufw
sudo ufw status
```
2. add firewall rule
```sh
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

3. create holes in firewall to allow ssh connections from the outside
```sh
sudo ufw allow 22/tcp
```

4. Allow http/https connections
```sh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

5. Now enable firewall
```sh
sudo ufw enable
sudo ufw status
```

**Port forwarding**

