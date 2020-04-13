# Nmap



## Faster Scans: --min-rate

`nmap scanme.nmap.com --top-ports 500 --min-rate 10`



`sudo nmap -n -Pn -p- --min-rate 20000 scanme.nmap.com`

Since a SYN packet is about 60 bytes, you have *roughly* the following scan rates in Mbps:

* 10'000 p/s → 5 Mbps
* 20'000 p/s → 10 Mbps
* 100'000 p/s → 50 Mbps
* 200'000 p/s 100 Mbps

A good tuning option is also --defeat-rst-ratelimit if you only care about open ports!