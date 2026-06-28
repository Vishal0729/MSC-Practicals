# Practical 11: Simulating MPLS Environment

## What this practical means
MPLS is like putting a special label on packets so routers can move them fast without checking every detail again and again.

## Simple picture
- Ordinary routing looks at the whole address every time
- MPLS looks at a label

## Important note
MPLS support is limited in Packet Tracer. Many MPLS labs are better done on real equipment, GNS3, or EVE-NG.

## What MPLS needs
- Provider edge routers
- Provider core routers
- Labels enabled
- Often OSPF or LDP underneath

## Basic idea
1. Build the provider network.
2. Enable the IGP.
3. Enable MPLS on core-facing interfaces.
4. Verify labels.

## Typical commands
```text
mpls ip
mpls label protocol ldp
```

On interfaces:
```text
interface serial 0/0/0
mpls ip
```

## Verification
```text
show mpls interfaces
show mpls ldp neighbor
show mpls forwarding-table
```

## Common mistakes
- Trying MPLS in an unsupported Packet Tracer image
- Forgetting to enable MPLS on both sides
- Missing the IGP
- Not understanding that MPLS is usually a provider-core topic

## Viva
- What is MPLS?
- Why are labels used?
- What is LDP?
- Is MPLS a routing protocol?
