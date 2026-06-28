# Practical 8: Configure BGP MED Attribute

## What this practical means
MED is a polite suggestion sent to another AS. It says, "If you have more than one way into my network, please use this one."

Lower MED is better.

## Topology idea from the paper
- One ISP router
- Two routers in another AS
- Parallel BGP links between them

## Build it
1. Place routers as shown in the paper.
2. Give each link a /30 network.
3. Configure eBGP neighbors.
4. Advertise loopbacks or internal networks.
5. Set MED on one route so the other side prefers one entry point.

## Example
```text
route-map SET-MED permit 10
set metric 10
route-map SET-MED permit 20
set metric 50
```

Apply it:
```text
router bgp 64512
neighbor 192.168.1.1 route-map SET-MED out
```

## What MED does
If one path has MED 10 and another has MED 50, the router usually prefers 10.

## Verification
```text
show ip bgp
show ip route
show ip bgp neighbors
```

## Common mistakes
- Using `set local-preference` when the practical asks for MED
- Applying the route-map on the wrong side
- Forgetting to advertise the network
- Expecting MED to beat every other BGP rule

## Viva
- What is MED?
- Which MED is better?
- Is MED used inside or outside an AS?
- Why would an ISP use MED?
