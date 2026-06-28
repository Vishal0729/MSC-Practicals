# Practical 3: Configure and Verify Path Control Using PBR

## What this practical means
Normally routers choose paths by routing table rules. PBR, or Policy Based Routing, is like telling the router: "For this special traffic, ignore the usual road and take this one instead."

## Simple idea
- Normal traffic uses the normal route
- Special traffic is forced to another path

## What to place
- 3 routers
- 1 PC if needed

## Topology idea
```text
R1 --- R2
 \     /
  \   /
    R3
```

The paper often uses two paths from a branch router to two ISP routers.

## Build it
1. Place routers in a triangle or branch-to-ISP shape.
2. Connect with serial cables.
3. Assign IP addresses.
4. Make sure interfaces are up.

## Example IP plan
- R1 to R2: `172.16.12.0/29`
- R1 to R3: `172.16.13.0/29`
- Loopbacks on routers for testing

## Basic router setup
```text
enable
configure terminal
hostname R1
interface serial 0/0/0
ip address 172.16.12.1 255.255.255.248
no shutdown
```

## PBR logic
1. Match the traffic you care about.
2. Decide the next hop.
3. Apply the policy to the interface.

## Example
```text
access-list 101 permit ip host 192.168.1.10 any
route-map PBR-TEST permit 10
match ip address 101
set ip next-hop 172.16.12.2
interface gigabitethernet 0/0
ip policy route-map PBR-TEST
```

## What this means
- ACL = a filter to catch the packet
- Route-map = the rule book
- `set ip next-hop` = "send this packet there"

## Verification
```text
show route-map
show ip policy
show ip route
traceroute
```

## Expected result
Traffic that matches the rule goes through the chosen next hop, even if the normal route says something else.

## Common mistakes
- Forgot to apply the route-map on the interface
- Matched the wrong ACL
- Wrong next-hop IP
- Testing with the wrong source host

## Viva
- What is PBR?
- How is PBR different from normal routing?
- Why use route-maps?
- When would PBR be useful?
