# Practical 1: Static Routing

## What this practical means
Think of routers like kids passing notes between houses. Static routing is when you tell each router exactly where to send the note. No guessing. No magic. Just fixed directions.

## What to place
- 5 routers
- 5 PCs or VPCS
- Serial cables between routers
- Straight-through cables between each PC and its router

## Simple topology idea
```text
PC5 --- R5
          \
           R2 --- R1 --- R3 --- R4 --- PC3
          /               \
PC1 --- R3                 PC4
```

Use the exact topology shown in your exam paper if the examiner gives one. If not, build the same shape with 5 routers and 5 PCs.

## Build it
1. Drag 5 routers.
2. Drag 5 PCs.
3. Connect router-to-router links with serial DCE cables.
4. Connect PC-to-router links with copper straight-through cables.
5. Turn on every serial interface with `no shutdown`.

## Where to type commands
Open each router, click **CLI**, then type.

## Basic IP plan
Use one /30 network for each router-to-router link and one /24 network for each LAN.

Example:
- R1 to R2: `10.0.12.0/30`
- R1 to R3: `10.0.13.0/30`
- R3 to R4: `10.0.34.0/30`

## Commands
### On each router
```text
enable
configure terminal
hostname R1
```

### On interfaces
```text
interface serial 0/0/0
ip address 10.0.12.1 255.255.255.252
no shutdown
```

If your router side is DCE:
```text
clock rate 64000
```

### Add static routes
Example on R1:
```text
ip route 192.168.2.0 255.255.255.0 10.0.12.2
ip route 192.168.3.0 255.255.255.0 10.0.13.2
```

## What the commands mean
- `ip route` = "Send packets this way."
- `no shutdown` = "Turn the interface on."
- `/30` link = small link between two routers only.
- `/24` LAN = normal local network for PCs.

## Verification
```text
show ip interface brief
show ip route
ping <destination>
```

## Expected result
- Router interfaces become `up/up`
- `show ip route` shows your static routes
- PCs can ping remote PCs

## Common mistakes
- Wrong interface number
- Forgetting `no shutdown`
- Wrong subnet mask
- Forgetting the return route on the other router
- Using the wrong cable type

## Viva
- What is static routing?
- Why is it called static?
- What happens if one link fails?
- Why do routers need return routes?
