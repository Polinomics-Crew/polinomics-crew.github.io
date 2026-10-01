"""Rebuild the public site's data files from an export of the Polinomics app's database.

Usage: python3 build.py <dump_dir>
<dump_dir> holds stories/*.json, crew/*.json and meta/edition.json, as saved by
ArtifactData "list" with out_dir.
"""
import json, os, sys, glob

dump = sys.argv[1]
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "data")
os.makedirs(out, exist_ok=True)

def load(coll):
    docs = []
    for f in glob.glob(os.path.join(dump, coll, "*.json")):
        d = json.load(open(f))
        d["id"] = os.path.basename(f)[:-5]
        docs.append(d)
    return docs

stories = sorted(load("stories"), key=lambda d: d.get("order", 99))
crew = sorted(load("crew"), key=lambda d: -(d.get("createdAt") or 0))
for c in crew:
    c.pop("authorId", None)  # account ids stay private
edition = json.load(open(os.path.join(dump, "meta", "edition.json")))

json.dump(stories, open(os.path.join(out, "stories.json"), "w"), ensure_ascii=False)
json.dump(crew, open(os.path.join(out, "crew.json"), "w"), ensure_ascii=False)
json.dump(edition, open(os.path.join(out, "edition.json"), "w"), ensure_ascii=False)
print(f"{len(stories)} stories, {len(crew)} crew articles, edition {edition.get('date')}")
