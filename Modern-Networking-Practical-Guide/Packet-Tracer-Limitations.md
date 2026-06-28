# Packet Tracer Limitations

This file is important because some practicals from the paper may not work fully in Packet Tracer even if they are real Cisco topics.

## Commonly problematic or unsupported features
- IP SLA on some Packet Tracer IOS images
- MPLS
- Some VRF features
- Advanced BGP behavior
- Some security features depending on router image

## What to do in an exam
1. Try the command only once or twice.
2. If the CLI says `Invalid input`, do not keep guessing forever.
3. Move to the next supported part if the practical can still be partially done.
4. If the examiner asks, say the simulator does not support that feature in the given IOS image.

## How to tell if a command is unsupported
- `Invalid input detected`
- Command is missing from `?` help
- The device model does not support the feature

## Good exam habit
Always verify the simulator before the exam:
- `show version`
- `show ip interface brief`
- `ip ?`
- `router bgp ?`

## From your uploaded paper
The repeated paper includes practicals such as IP SLA, MPLS, VRF, BGP attributes, secure management plane, PBR, inter-VLAN routing, and static routing. Some of these are fully fine in Packet Tracer, while some may need a stronger simulator. The paper pages are visibly repeated across the upload.
