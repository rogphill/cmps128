# A single-site Key-value store with forwarding

# Motivation
To explore Primary / Backup Replication in distributed systems
 
# Installation
Make sure you have Docker installed

# How to run
If subnet has not been created yet, run 
```sudo docker network create --subnet=10.0.0.0/16 mynet``` 

then run (on Mac)

``` ./runtest.sh ```

run (on Windows)

```.\wintest.bat```

The second command will kill all existing containers, build Docker container, then run the provided Test Script to test `get`, `put`, and `delete` on our Key-value Store, then rm all existing instances. 

# Contributors
- Akobir - akhamido@ucsc.edu
- Vien Van - vhvan@ucsc.edu
- Rob Phillips - rogphill@ucsc.edu
- Tarun Salh - tsalh@ucsc.edu

# Purpose
HW2 for CMPS128 - Distributed Systems Fall 2018 @ UCSC



