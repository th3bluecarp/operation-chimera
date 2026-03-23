# Incident Case: Operation Chimera (NIGHTMARE DIFFICULTY)

**Background:** You are responding to a suspected major breach at a defense contractor. The alarm was tripped by a billing alert: an unexpected spike in AWS EBS Snapshot storage costs. The primary application server (`10.0.1.20`) seems to be the epicenter, but standard `ps` and `netstat` commands on the box show nothing malicious. 

**Your Objective:**
Reconstruct the entire kill chain across Web, Linux System, Network, and AWS Cloud environments. Answer the following:
1. **Initial Access:** How did the attacker get in, and what specific AWS credentials did they steal?
2. **Evasion:** The attacker has an active C2 process running, but it's hidden from system tools. How are they hiding it, and what is the hidden process ID (PID)?
3. **Lateral Movement:** How did the attacker communicate with the isolated internal database (`10.0.5.50`), and what tool did they use?
4. **Data Exfiltration:** Explain exactly how the attacker stole the database data using AWS APIs without downloading the database files over the internet. What external AWS account did they send it to?

**Rules of Engagement:**
Use your own timeline analysis to correlate the timestamps across the artifacts.
