"""Count job postings per technology with exact skill-name matching.

Usage: python scripts/count_job_postings.py jobs.json
Data: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/module%201/Accessing%20Data%20Using%20APIs/jobs.json
"""
import json, collections, sys
jobs = json.load(open(sys.argv[1], encoding="utf-8"))
techs = ["C", "C#", "C++", "Java", "JavaScript", "Python", "Scala", "Oracle", "SQL Server", "MySQL", "PostgreSQL", "MongoDB"]
def skills(j): return [s.strip().lower() for s in j.get("Key Skills", "").split("|") if s.strip()]
print("total postings", len(jobs))
print(f"{'tech':12}{'substring (original)':>22}{'exact skill match':>20}")
for t in techs:
    sub = sum(t.lower() in j.get("Key Skills", "").lower() for j in jobs)
    exact = sum(t.lower() in skills(j) for j in jobs)
    print(f"{t:12}{sub:>22}{exact:>20}")
locs = collections.Counter(j.get("Location", "") for j in jobs)
print("top locations", locs.most_common(8))
