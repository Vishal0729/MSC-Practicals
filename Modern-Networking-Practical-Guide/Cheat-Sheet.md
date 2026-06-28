# Cheat Sheet

## Very common commands
```text
enable
configure terminal
end
show running-config
show ip interface brief
show ip route
ping
traceroute
```

## Interface
```text
interface serial 0/0/0
ip address 10.0.0.1 255.255.255.252
no shutdown
clock rate 64000
```

## Static route
```text
ip route 192.168.2.0 255.255.255.0 10.0.0.2
```

## VLAN
```text
vlan 10
name SALES
switchport mode access
switchport access vlan 10
```

## Router-on-a-stick
```text
interface g0/0.10
encapsulation dot1Q 10
ip address 192.168.10.1 255.255.255.0
```

## BGP
```text
router bgp 65001
neighbor 10.0.0.2 remote-as 65002
network 10.1.1.0 mask 255.255.255.0
```

## PBR
```text
access-list 101 permit ip host 192.168.1.10 any
route-map PBR-TEST permit 10
match ip address 101
set ip next-hop 10.0.0.2
ip policy route-map PBR-TEST
```

## Security
```text
enable secret class123
username admin secret Admin@123
line vty 0 4
login local
transport input ssh
```

## Tracking
```text
track 1 ip sla 12 reachability
show track 1
```

## If you forget everything
1. Turn interfaces on
2. Give them IPs
3. Check routes
4. Test with ping
5. Read the viva questions again
