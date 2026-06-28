# Practical 7: Configuring IBGP and EBGP Sessions, Local Preference, and MED

## What this practical means
This practical combines the BGP family tricks:
- iBGP and eBGP sessions
- Local Preference
- MED

Think of it like choosing the best bus line to school.

## Local Preference
Local Preference tells routers inside the same AS which exit road they should prefer.

Higher local preference = more preferred.

## MED
MED tells an outside AS which entry point is better.

Lower MED = more preferred.

## Basic idea
- Local Preference works inside one AS
- MED works between ASes, often to influence incoming traffic

## Example commands
### Set local preference
```text
route-map LP-200 permit 10
set local-preference 200
```

Apply to BGP neighbor:
```text
router bgp 65001
neighbor 10.0.0.2 route-map LP-200 in
```

### Set MED
```text
route-map MED-50 permit 10
set metric 50
```

Apply outbound:
```text
router bgp 65001
neighbor 192.168.100.2 route-map MED-50 out
```

## What they mean
- Local preference = "use this exit"
- MED = "please enter here"
- Bigger local preference wins
- Smaller MED wins

## Verification
```text
show ip bgp
show ip bgp neighbors
show ip route
```

## Common mistakes
- Applying the route-map in the wrong direction
- Confusing local preference and MED
- Forgetting iBGP neighbors
- Expecting MED to work across unrelated ASes the same way every time

## Viva
- What is local preference?
- What is MED?
- Which one is more preferred: higher or lower?
- Where does each attribute work?
