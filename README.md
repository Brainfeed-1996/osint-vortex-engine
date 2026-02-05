# OSINT Vortex Engine

Advanced correlation engine for Open Source Intelligence.

## 🗺️ Architecture
```mermaid
graph LR
    T[Target] --> S[Vortex Core]
    S --> D1[(Shodan)]
    S --> D2[(Whois)]
    S --> D3[(Social)]
    D1 & D2 & D3 --> R[Report]
```