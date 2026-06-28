# Practical 9: Secure the Management Plane

## What this practical means
The management plane is the router's front door. This practical is about locking that door properly so only the right people can log in and manage the device.

## What to protect
- Console access
- Telnet/SSH remote access
- Passwords
- Privileged mode
- Management interfaces

## Basic setup
```text
enable
configure terminal
hostname R1
enable secret class123
service password-encryption
banner motd #Unauthorized access prohibited#
```

## Console line
```text
line console 0
password cisco
login
logging synchronous
```

## SSH setup
```text
ip domain-name lab.local
username admin secret Admin@123
crypto key generate rsa
ip ssh version 2
line vty 0 4
login local
transport input ssh
```

## What it means
- `enable secret` = password for privileged mode
- `service password-encryption` = hides weak passwords
- `line vty` = remote login lines
- `login local` = use local username database
- `transport input ssh` = allow SSH only

## Verification
```text
show running-config
show ip ssh
show users
```

## Expected result
- Console asks for password
- SSH works
- Telnet is blocked if you configured SSH only
- Passwords are not shown in plain text

## Common mistakes
- Forgetting the domain name before RSA key generation
- Forgetting username creation
- Using `login` instead of `login local`
- Enabling Telnet when the question asks for secure access

## Viva
- What is the management plane?
- Why use SSH instead of Telnet?
- What is the difference between `enable password` and `enable secret`?
- Why encrypt router passwords?
