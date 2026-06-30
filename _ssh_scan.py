import paramiko, sys, json

HOST = "149.88.72.233"
USER = "root"
PWD  = "LYHlyhnb5201314"

def run(c, cmd, t=30):
    stdin, stdout, stderr = c.exec_command(cmd, timeout=t)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    return out, err

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, port=22, username=USER, password=PWD, timeout=20, look_for_keys=False, allow_agent=False)

print("=== uname / uptime ===")
o,e = run(c, "uname -a; echo; uptime; echo; cat /etc/os-release 2>/dev/null | head -5")
print(o, e)

print("=== top cpu procs ===")
o,e = run(c, "ps -eo pid,ppid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head -20")
print(o, e)

print("=== top mem procs ===")
o,e = run(c, "ps -eo pid,ppid,user,%cpu,%mem,etime,cmd --sort=-%mem | head -20")
print(o, e)

print("=== load / mem / disk ===")
o,e = run(c, "cat /proc/loadavg; echo; free -h; echo; df -h | grep -vE 'tmpfs|overlay|udev'")
print(o, e)

print("=== suspicious dirs in /tmp /var/tmp /dev/shm ===")
o,e = run(c, "ls -la /tmp /var/tmp /dev/shm 2>/dev/null")
print(o, e)

print("=== network estab ===")
o,e = run(c, "ss -tnp 2>/dev/null | head -40 || netstat -tnp 2>/dev/null | head -40")
print(o, e)

print("=== listening ===")
o,e = run(c, "ss -tlnp 2>/dev/null | head -40")
print(o, e)

print("=== crontabs ===")
o,e = run(c, "for u in root $(cut -d: -f1 /etc/passwd 2>/dev/null); do crontab -u $u -l 2>/dev/null | sed \"s/^/$u: /\"; done; echo '--- /etc/cron* ---'; ls -la /etc/cron* 2>/dev/null; cat /etc/crontab 2>/dev/null")
print(o, e)

print("=== systemd timers ===")
o,e = run(c, "systemctl list-timers --all --no-pager 2>/dev/null | head -30")
print(o, e)

print("=== recent files in /tmp /var/tmp ===")
o,e = run(c, "find /tmp /var/tmp /dev/shm -type f -mmin -1440 2>/dev/null | head -40")
print(o, e)

print("=== hidden in home ===")
o,e = run(c, "ls -la /root /home 2>/dev/null")
print(o, e)

print("=== hosts ===")
o,e = run(c, "cat /etc/hosts | head -30")
print(o, e)

c.close()
