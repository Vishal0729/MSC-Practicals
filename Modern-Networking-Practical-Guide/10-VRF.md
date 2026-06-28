# Practical 10: Simulating VRF

## What this practical means
VRF is like giving one router multiple separate brains. The same router can keep different networks isolated from each other, even if they use similar IP ranges.

## What VRF does
It splits one router into separate routing tables.

## Think of it like this
One router can act like two separate routers:
- one for one customer
- one for another customer

## Topology idea from the paper
The paper shows one central router connected to two edge routers, with separate loopbacks and networks.

## Basic commands
```text
ip vrf RED
rd 1:1
ip vrf BLUE
rd 2:2
```

Apply VRF to interfaces:
```text
interface gigabitethernet 0/0
ip vrf forwarding RED
ip address 10.0.0.1 255.255.255.0
```

## What it means
- `ip vrf forwarding` = put this interface into a separate routing box
- `rd` = route distinguisher, a label that keeps routes separate

## Verification
```text
show ip vrf
show ip route vrf RED
show ip route vrf BLUE
```

## Common mistakes
- Applying VRF after the IP address and losing the address
- Forgetting to assign routes inside the VRF
- Mixing interfaces between VRFs
- Expecting normal routing to see VRF routes without special commands

## Viva
- What is VRF?
- Why is VRF used?
- What is an RD?
- How is VRF different from normal routing?
