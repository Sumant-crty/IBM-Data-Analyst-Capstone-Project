"""Build Cognos-ready tables from the 2024 Stack Overflow survey (standard library only).

The survey stores multi-select answers as one string ("PostgreSQL;Redis;SQLite").
Cognos treats each string as a single category, so charts built on the raw file
count combinations instead of technologies. This script splits the answers into
one row per technology.

Usage: python scripts/make_cognos_tables.py survey-data.csv dashboard/data

Writes:
  tech_counts.csv   Category, Status, Technology, Respondents   (small; enough for every tech chart)
  tech_long.csv     ResponseId, Category, Status, Technology    (one row per answer; joins to demographics)
  demographics.csv  ResponseId, Age, EdLevel, Country, ...      (one row per respondent)
"""
import collections
import csv
import os
import sys

csv.field_size_limit(10**9)

COLUMNS = {
    ("Language", "Worked with"): "LanguageHaveWorkedWith",
    ("Language", "Want to work with"): "LanguageWantToWorkWith",
    ("Database", "Worked with"): "DatabaseHaveWorkedWith",
    ("Database", "Want to work with"): "DatabaseWantToWorkWith",
    ("Platform", "Worked with"): "PlatformHaveWorkedWith",
    ("Platform", "Want to work with"): "PlatformWantToWorkWith",
    ("Web framework", "Worked with"): "WebframeHaveWorkedWith",
    ("Web framework", "Want to work with"): "WebframeWantToWorkWith",
}
DEMOGRAPHICS = ["ResponseId", "Age", "EdLevel", "Country", "Employment", "RemoteWork", "YearsCodePro", "ConvertedCompYearly", "JobSat"]


def clean(value):
    return "" if value in ("", "NA") else value.replace("’", "'")


def main(survey_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    counts = collections.Counter()
    with open(survey_path, encoding="utf-8") as f, \
         open(os.path.join(out_dir, "tech_long.csv"), "w", newline="", encoding="utf-8") as long_f, \
         open(os.path.join(out_dir, "demographics.csv"), "w", newline="", encoding="utf-8") as demo_f:
        long_w = csv.writer(long_f)
        long_w.writerow(["ResponseId", "Category", "Status", "Technology"])
        demo_w = csv.writer(demo_f)
        demo_w.writerow(DEMOGRAPHICS)
        for row in csv.DictReader(f):
            demo_w.writerow([clean(row[c]) for c in DEMOGRAPHICS])
            for (category, status), column in COLUMNS.items():
                for tech in {t.strip() for t in clean(row[column]).split(";") if t.strip()}:
                    long_w.writerow([row["ResponseId"], category, status, tech])
                    counts[(category, status, tech)] += 1

    with open(os.path.join(out_dir, "tech_counts.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Category", "Status", "Technology", "Respondents"])
        for (category, status, tech), n in sorted(counts.items(), key=lambda kv: (kv[0][0], kv[0][1], -kv[1])):
            w.writerow([category, status, tech, n])

    for (category, status), _ in COLUMNS.items():
        top = sorted(((n, t) for (c, s, t), n in counts.items() if (c, s) == (category, status)), reverse=True)[:3]
        print(f"{category:14} {status:18} top 3: " + ", ".join(f"{t} {n:,}" for n, t in top))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
