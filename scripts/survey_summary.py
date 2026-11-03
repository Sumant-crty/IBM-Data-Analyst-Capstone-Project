"""Top technologies, demographics and pay from the 2024 Stack Overflow survey (standard library only).

Usage: python scripts/survey_summary.py survey-data.csv
Data: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n01PQ9pSmiRX6520flujwQ/survey-data.csv
"""
import csv, collections, statistics, sys, json
csv.field_size_limit(10**9)
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
N = len(rows); out = {"N": N}
print("rows", N, "unique ResponseId", len({r["ResponseId"] for r in rows}))
def multi(col, k=10):
    c = collections.Counter(); answered = 0
    for r in rows:
        v = r[col]
        if v and v != "NA":
            answered += 1
            c.update(x.strip() for x in v.split(";") if x.strip())
    return answered, c.most_common(k)
for col in ["LanguageHaveWorkedWith","LanguageWantToWorkWith","DatabaseHaveWorkedWith","DatabaseWantToWorkWith",
            "PlatformHaveWorkedWith","PlatformWantToWorkWith","WebframeHaveWorkedWith","WebframeWantToWorkWith","OpSysProfessional use"]:
    a, top = multi(col); out[col] = {"answered": a, "top": top}
    print(f"\n{col} (answered {a})"); [print(f"   {k}: {v}") for k, v in top]
def single(col, k=12):
    c = collections.Counter(r[col] for r in rows if r[col] and r[col] != "NA"); return c.most_common(k)
for col in ["Age","EdLevel","Country","Employment","MainBranch","RemoteWork"]:
    top = single(col); out[col] = top; print(f"\n{col}:"); [print(f"   {k}: {v}") for k, v in top]
ed = [r["EdLevel"] for r in rows if r["EdLevel"] and r["EdLevel"] != "NA"]
bach = sum(any(w in e for w in ["Bachelor", "Master", "Professional degree", "doctoral"]) for e in ed)
print("\nBachelor's or higher:", bach, "/", len(ed), round(100*bach/len(ed),1))
age = [r["Age"] for r in rows if r["Age"] and r["Age"]!="Prefer not to say"]
young = sum(a in ("18-24 years old","25-34 years old") for a in age); print("18-34 share", round(100*young/len(age),1))
num = lambda col: [float(r[col]) for r in rows if r[col] not in ("", "NA")]
comp = num("ConvertedCompYearly"); js = num("JobSat")
print("comp n", len(comp), "median", statistics.median(comp)); print("JobSat n", len(js), "mean", round(statistics.mean(js),2), "median", statistics.median(js))
ycp = [r["YearsCodePro"] for r in rows if r["YearsCodePro"] not in ("","NA")]
conv = [0.5 if v=="Less than 1 year" else 51 if v=="More than 50 years" else float(v) for v in ycp]
print("YearsCodePro n", len(conv), "median", statistics.median(conv))
out.update(bach_share=round(100*bach/len(ed),1), young_share=round(100*young/len(age),1), comp_median=statistics.median(comp), comp_n=len(comp), jobsat_mean=round(statistics.mean(js),2), jobsat_n=len(js), ycp_median=statistics.median(conv))
json.dump(out, open("survey_summary.json", "w"), indent=1)
