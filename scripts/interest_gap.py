"""Want-to-use vs. used ratios and median pay by language.

Usage: python scripts/interest_gap.py survey-data.csv
"""
import csv, collections, statistics, sys
csv.field_size_limit(10**9)
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
def counts(col):
    c = collections.Counter()
    for r in rows:
        if r[col] and r[col] != "NA": c.update(x.strip() for x in r[col].split(";"))
    return c
for kind in ["Language", "Database"]:
    have, want = counts(kind + "HaveWorkedWith"), counts(kind + "WantToWorkWith")
    print(kind, "want/have ratio (min 3000 users):")
    rat = sorted(((want[k] / have[k], k, have[k], want[k]) for k in have if have[k] >= 3000), reverse=True)[:8]
    for r_, k, h, w in rat: print(f"   {k}: have {h}, want {w}, ratio {r_:.2f}")
# median comp by language among full-time employed with comp
by = collections.defaultdict(list)
for r in rows:
    if r["ConvertedCompYearly"] not in ("", "NA") and r["LanguageHaveWorkedWith"] not in ("", "NA"):
        for l in r["LanguageHaveWorkedWith"].split(";"): by[l].append(float(r["ConvertedCompYearly"]))
print("median comp by language (n>=2000):")
for k, v in sorted(((k, v) for k, v in by.items() if len(v) >= 2000), key=lambda kv: -statistics.median(kv[1]))[:12]:
    print(f"   {k}: {statistics.median(v):.0f} (n={len(v)})")
print("countries", len({r['Country'] for r in rows if r['Country'] not in ('', 'NA')}))
print("answered Country", sum(r['Country'] not in ('', 'NA') for r in rows))
