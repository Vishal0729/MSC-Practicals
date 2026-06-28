# Practical 4: Configure IP SLA Tracking and Path Control

## What this practical means
This is a router that has a tiny helper robot. The robot keeps checking whether the main path is alive. If the path dies, the router switches away.

## Important note
In many Packet Tracer builds, IP SLA may not be supported even if the command exists in real Cisco IOS. If the command fails in Packet Tracer, move to `Packet-Tracer-Limitations.md`.

## What to place
- 3 routers
- Optional PC

## Topology idea
```text
R1 branch router
  |\
  | \
 R2  R3
```

## Build it
1. Place three routers.
2. Connect R1 to R2 and R1 to R3.
3. Assign IP addresses.
4. Turn interfaces on.

## Example IPs
- R1 to R2: `209.165.201.0/30`
- R1 to R3: `209.165.202.128/30`
- Loopback on R2 for testing

## Normal default route
```text
ip route 0.0.0.0 0.0.0.0 209.165.201.1
```

## IP SLA idea
```text
ip sla 12
icmp-echo 209.165.201.30
frequency 11
ip sla schedule 12 life forever start-time now
```

## Tracking
```text
track 1 ip sla 12 reachability
delay down 10 up 1
```

## Link the route to the track
```text
no ip route 0.0.0.0 0.0.0.0 209.165.201.1
ip route 0.0.0.0 0.0.0.0 209.165.201.1 5 track 1
```

## What it means
- IP SLA = the robot that pings
- Track = the watcher that listens to the robot
- Tracked route = the route only stays if the watcher says "OK"

## Verification
```text
show ip sla statistics
show track 1
show ip route
```

## Expected result
If the probed path is alive, the track says up and the route stays. If the path fails, the route disappears or the router switches to backup routing.

## Common mistakes
- IP SLA not supported in Packet Tracer
- Wrong probe IP
- Forgot to schedule the SLA
- Wrong track number
- No backup route

## Viva
- What is IP SLA?
- What is object tracking?
- What happens when the tracked object goes down?
- Why use delay timers?
