# Practical 6: Using the AS_PATH Attribute

## What this practical means
AS_PATH is like a travel diary. It writes down every AS the packet has passed through. BGP uses that diary to choose the shorter or cleaner route.

## What to place
- 3 routers
- Two different paths from one side to another

## Idea from the paper
One side has AS 100, the middle has AS 300, and the other side has AS 65000.

## Why it matters
BGP prefers the path with the shorter AS_PATH, unless another rule is stronger.

## Example topology idea
```text
Andheri --- Bandra --- Churchgate
   AS100      AS300      AS65000
```

## Basic commands
```text
router bgp 100
network 10.1.1.0 mask 255.255.255.0
neighbor 192.168.1.6 remote-as 300
```

## AS_PATH idea
If one route went through:
```text
100 -> 300 -> 65000
```
and another route went through:
```text
100 -> 200 -> 65000
```
BGP can prefer the path with fewer AS hops.

## Verification
```text
show ip bgp
show ip bgp neighbors
show ip route
```

## What to look for
In the BGP table, the AS path column shows the route history.

## Common mistakes
- Missing network statement
- Wrong AS number
- Neighbor not established
- Expecting AS_PATH to work without BGP routes

## Viva
- What is AS_PATH?
- Why does BGP keep the AS path?
- How does BGP use AS_PATH?
- Can AS_PATH be changed?
