# Practical 5: Configure IBGP and EBGP

## What this practical means
Routers are like club members. BGP is the club rulebook. iBGP is when routers inside the same club talk to each other. eBGP is when routers from different clubs talk to each other.

## What to place
- 2 or more routers
- Optional loopbacks

## Basic idea
- Same AS number = iBGP
- Different AS number = eBGP

## Example
- R1 and R2 inside AS 65001
- R3 in AS 65002

## Build it
1. Place routers.
2. Connect them with serial or gigabit links.
3. Assign IP addresses.
4. Add loopbacks if needed.
5. Configure BGP neighbors.

## Example commands
### On R1
```text
router bgp 65001
neighbor 10.0.0.2 remote-as 65001
neighbor 192.168.100.2 remote-as 65002
```

### On R2
```text
router bgp 65001
neighbor 10.0.0.1 remote-as 65001
```

### On R3
```text
router bgp 65002
neighbor 192.168.100.1 remote-as 65001
```

## What it means
- `router bgp 65001` = start BGP and join AS 65001
- `neighbor` = tell the router who to talk to
- `remote-as` = the other router's club number

## Verification
```text
show ip bgp summary
show ip bgp
show ip route
```

## Expected result
Neighbors should become `Established`.

## Common mistakes
- Wrong AS number
- Wrong neighbor IP
- Interface down
- Not advertising networks
- iBGP split-horizon style confusion

## Viva
- What is BGP?
- Difference between iBGP and eBGP?
- What is an AS?
- What does `remote-as` do?
