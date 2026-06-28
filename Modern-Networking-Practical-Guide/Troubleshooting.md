# Troubleshooting Guide

## 1. Red link between routers
Possible reasons:
- Wrong cable
- `no shutdown` missing
- `clock rate` missing on DCE side
- Wrong interface number

## 2. Interface is down/down
Check:
- Cable seated properly
- Correct interface selected
- The other router interface is also configured

## 3. Interface is administratively down
That usually means:
```text
no shutdown
```
is missing.

## 4. Ping fails
Check:
- IP address
- Subnet mask
- Default gateway
- Routing
- Return path

## 5. BGP neighbor not established
Check:
- AS number
- Neighbor IP
- Reachability
- Interface status
- Network statement

## 6. Command gives invalid input
Possible causes:
- Wrong mode
- Wrong IOS feature set
- Packet Tracer limitation
- Typo

## 7. Route does not show up
Check:
- Next hop reachable
- Correct subnet
- Metric / administrative distance
- Track status
- Route-map application

## 8. Quick checks
```text
show ip interface brief
show ip route
show running-config
show cdp neighbors
show ip bgp summary
```

## 9. Practical exam rescue plan
If something stops working:
- Stop and check the interface status first
- Then check the IP address
- Then check the routing
- Then check simulator support
