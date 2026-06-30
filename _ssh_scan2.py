import paramiko

HOST = "149.88.72.233"; USER = "root"; PWD = "LYHlyhnb5201314"

def run(c, cmd, t=30):
    _, out, err = c.exec_command(cmd, timeout=t)
    return out.read().decode("utf-8","replace"), err.read().decode("utf-8","replace")

c = paramiko.SSHClient(); c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, 22, USER, PWD, timeout=20, look_for_keys=False, allow_agent=False)

print("=== xhv incident file ===")
o,e = run(c, "ls -la /root/xhv* /root/.xhv 2>/dev/null; echo '--- content ---'; cat /root/xhv_incident_20260617_012031.txt 2>/dev/null | head -200")
print(o, e)

print("=== /root/.xhv tree ===")
o,e = run(c, "find /root/.xhv -maxdepth 4 -printf '%M %u %s %TY-%Tm-%Td %TH:%TM %p\\n' 2>/dev/null | head -60")
print(o, e)

print("=== /tmp/network_script ===")
o,e = run(c, "file /tmp/network_script; ls -la /tmp/network_script; echo '--- head ---'; head -100 /tmp/network_script 2>/dev/null")
print(o, e)

print("=== proc 1133 (defunct) ===")
o,e = run(c, "ls -la /proc/1133 2>/dev/null | head -3; echo; cat /proc/1133/cmdline 2>/dev/null | tr '\\0' ' '; echo; cat /proc/1133/status 2>/dev/null | head -20; echo; ls -la /proc/1133/exe /proc/1133/cwd 2>/dev/null")
print(o, e)

print("=== proc 1133 env / fd ===")
o,e = run(c, "cat /proc/1133/environ 2>/dev/null | tr '\\0' '\\n' | head -30; echo '--- fds ---'; ls -la /proc/1133/fd 2>/dev/null | head -20")
print(o, e)

print("=== /app dir ===")
o,e = run(c, "ls -la /app 2>/dev/null; echo; ls -la /app/* 2>/dev/null | head -60")
print(o, e)

print("=== axonhub proc 7845 ===")
o,e = run(c, "cat /proc/7845/cmdline 2>/dev/null | tr '\\0' ' '; echo; ls -la /proc/7845/exe /proc/7845/cwd 2>/dev/null; echo; cat /proc/7845/status 2>/dev/null | head -10")
print(o, e)

print("=== disk usage top ===")
o,e = run(c, "du -h --max-depth=1 / 2>/dev/null | sort -rh | head -25")
print(o, e)

print("=== docker ps ===")
o,e = run(c, "docker ps -a --format 'table {{.ID}}\\t{{.Image}}\\t{{.Status}}\\t{{.Names}}' 2>/dev/null | head -40")
print(o, e)

print("=== docker images ===")
o,e = run(c, "docker images 2>/dev/null | head -30")
print(o, e)

print("=== bash_history tail ===")
o,e = run(c, "tail -60 /root/.bash_history 2>/dev/null")
print(o, e)

print("=== last logins ===")
o,e = run(c, "last -a 2>/dev/null | head -15; echo '---'; lastb -a 2>/dev/null | head -15")
print(o, e)

print("=== auth log recent ===")
o,e = run(c, "tail -60 /var/log/auth.log 2>/dev/null")
print(o, e)

c.close()
