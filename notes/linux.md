# Linux cheat sheet

## Files
- `ls -lah` list files with sizes and hidden files
- `du -sh *` size of each item in the current folder
- `df -h` free disk space per filesystem
- `find / -name "*.log" -mtime -1` log files changed in the last day
- `tail -f /var/log/syslog` follow a log file live

## Permissions
- `chmod 600 ~/.ssh/id_ed25519` private key readable only by you
- `chown -R app:app /opt/app` change owner recursively
- `sudo usermod -aG docker $USER` let a user run docker (log out and back in)

## Processes and ports
- `ps aux | grep nginx` find a process
- `sudo ss -tulpn` which process listens on which port
- `sudo lsof -i :8080` who is using port 8080
- `kill -9 <pid>` force-kill a process

## Services (systemd)
- `sudo systemctl status nginx` check a service
- `sudo systemctl enable --now nginx` start now and on boot
- `journalctl -u nginx -f` follow a service's logs

## Firewall (ufw)
- `sudo ufw allow OpenSSH` then `sudo ufw enable`
- `sudo ufw allow 80/tcp` open HTTP
- `sudo ufw status verbose`

## SSH
- `ssh-keygen -t ed25519` create a key pair
- `ssh-copy-id user@host` install your public key on a server
- Disable password login: set `PasswordAuthentication no` in `/etc/ssh/sshd_config`, then `sudo systemctl restart ssh`
