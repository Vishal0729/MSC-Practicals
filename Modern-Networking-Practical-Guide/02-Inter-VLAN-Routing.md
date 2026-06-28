# Practical 2: Inter-VLAN Routing

## What this practical means
Imagine one switch is a big school with different classrooms. VLANs are like separate classrooms. Inter-VLAN routing is the teacher who helps one classroom talk to another.

## What to place
- 1 router
- 1 switch
- 2 or more PCs

## Two common methods
- Router-on-a-stick
- Multilayer switch routing

This file uses the beginner-friendly router-on-a-stick method.

## Topology
```text
PC1 --- SW1 --- Router1
PC2 ---/
PC3 ---/
```

## Build it
1. Drag 1 router and 1 switch.
2. Drag 2 or more PCs.
3. Connect PCs to the switch with copper straight-through.
4. Connect switch to router with one trunk link.
5. Create VLANs on the switch.
6. Put each PC port into the correct VLAN.

## VLAN idea
- VLAN 10 for PC1
- VLAN 20 for PC2
- VLAN 30 for PC3

## Switch commands
```text
enable
configure terminal
vlan 10
name SALES
vlan 20
name HR
vlan 30
name IT
```

Assign ports:
```text
interface fastethernet 0/1
switchport mode access
switchport access vlan 10
```

## Router commands
On the router interface connected to the switch:
```text
interface gigabitethernet 0/0
no shutdown
interface gigabitethernet 0/0.10
encapsulation dot1Q 10
ip address 192.168.10.1 255.255.255.0
interface gigabitethernet 0/0.20
encapsulation dot1Q 20
ip address 192.168.20.1 255.255.255.0
interface gigabitethernet 0/0.30
encapsulation dot1Q 30
ip address 192.168.30.1 255.255.255.0
```

## What it means
- `dot1Q` = tag that tells the router which VLAN the packet came from.
- Subinterface `.10` is like a small doorway inside one big router door.

## Verification
```text
show vlan brief
show ip interface brief
ping
```

## Expected result
A PC in VLAN 10 can talk to a PC in VLAN 20 through the router.

## Common mistakes
- Trunk not enabled
- Wrong VLAN number
- Wrong default gateway on PCs
- Forgot `no shutdown`
- Put a PC in the wrong access port

## Viva
- What is a VLAN?
- Why do we need inter-VLAN routing?
- Difference between access and trunk port?
- What is router-on-a-stick?
