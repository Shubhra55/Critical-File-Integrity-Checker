# Critical-File-Integrity-Checker

🛡️ Local Critical File Integrity Checker
A Python-based tool for monitoring and verifying the integrity of essential local files by generating hash values and detecting unauthorized modifications. Data is persistently stored in both MySQL and Excel for reliability and accessibility.

📌 Features
Tracks selected critical files and their hash signatures

Detects file changes using hash comparisons

Stores file metadata and history in:

✅ MySQL for structured querying and backend access

✅ Excel for offline review and human-readable summaries

CLI-based interface (optionally extendable to a GUI)

🧰 Tech Stack
Python 3.x

hashlib, os

mysql.connector (or SQLAlchemy for DB interactions)

Excel (.xlsx) for report logging

MySQL for persistent storage


🚀 How It Works
Add critical files (by path) to monitor

The script computes each file’s SHA-256 hash and stores it in MySQL and Excel

On subsequent runs, it re-hashes and compares current values against stored ones

Any mismatch is flagged and logged as a potential integrity breach

📂 Sample Excel Output
File Path	Last Checked	Current Hash	Status
C:\system\config.sys	2025-06-20 19:45	...	✅ Unchanged
C:\auth\token.key	2025-06-20 19:45	...	❌ Modified
🔐 Use Cases
Monitoring local system configuration files

Ensuring source code files remain unaltered

Providing audit-ready logs for compliance checks
