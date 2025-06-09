import os
import re
import argparse
from urllib.parse import urlparse


README_HEADER = (
    "| Title | Paper | Code | Publisher | Year | Topics |\n"
    "|-------|-------|------|-----------|------|--------|\n"
)

def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')

def get_source_name(url):
    if not url:
        return "-"
    hostname = urlparse(url).hostname or ""
    if "arxiv" in hostname:
        return "arXiv"
    elif "github" in hostname:
        return "GitHub"
    elif "paperswithcode" in hostname:
        return "PapersWithCode"
    else:
        return hostname.replace("www.", "").split('.')[0].capitalize()
    
def create_paper_md(paper, folder="papers"):
    os.makedirs(folder, exist_ok=True)
    slug = sanitize_filename(paper['title'])
    filepath = os.path.join(folder, f"{slug}.md")

    # Check if file already exists and grab existing summary
    existing_summary = ""
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        match = re.search(r"## 🧠 Summary\s*\n(.+?)(?:\n## |\Z)", content, re.DOTALL)
        if match:
            existing_summary = match.group(1).strip()

    # Check if a matching image exists in assets/figures/
    image_formats = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
    image_path = next(
        (f"../assets/figures/{slug}{ext}" for ext in image_formats if os.path.exists(f"assets/figures/{slug}{ext}")),
        None
    )

    with open(filepath, "w") as f:
        f.write(f"# {paper['title']}\n\n")
        if paper.get('year'):
            f.write(f"**Year:** {paper['year']}\n\n")
        if paper['publisher']:
            f.write(f"**Published by:** {paper['publisher']}\n\n")
        if paper['source']:
            f.write(f"**Paper:** [{get_source_name(paper['source'])}]({paper['source']})\n\n")
        if paper['code']:
            f.write(f"**Code:** [{get_source_name(paper['code'])}]({paper['code']})\n\n")

        # Summary section
        f.write("## 🧠 Summary\n")
        if existing_summary and "Add a brief summary here" not in existing_summary:
            f.write(existing_summary + "\n\n")
        else:
            f.write("(Add a brief summary here)\n\n")

        # If image exists, include it
        if image_path:
            f.write(f"![Figure]({image_path})\n\n")

        f.write("## 🏷️ Topics\n")
        f.write(", ".join(f"`{t}`" for t in paper['topics']))
        f.write("\n")

    return slug


def ensure_readme_structure(readme_path="README.md"):
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write("# 🧠 ML is All You Need\n\n")
            f.write("## 📚 Paper Index\n\n")
            f.write(README_HEADER)
    else:
        with open(readme_path, "r") as f:
            content = f.read()
        if "| Title |" not in content:
            with open(readme_path, "a") as f:
                f.write("\n## 📚 Paper Index\n\n")
                f.write(README_HEADER)

def add_to_readme(paper, slug, readme_path="README.md"):
    row = "| [{0}](papers/{1}.md) | {2} | {3} | {4} | {5} | {6}\n".format(
        paper['title'],
        slug,
        f"[{get_source_name(paper['source'])}]({paper['source']})" if paper.get('source') else "-",
        f"[{get_source_name(paper['code'])}]({paper['code']})" if paper.get('code') else "-",
        paper.get('publisher', "-") or "-",
        paper.get('year', "-") or "-",
        ", ".join(f"`{t}`" for t in paper.get('topics', [])) if paper.get('topics') else "-"
    )

    with open(readme_path, "r") as f:
        lines = f.readlines()

    was_updated = False
    pattern = f"| [{paper['title']}]("
    for i, line in enumerate(lines):
        if line.startswith(pattern):
            lines[i] = row
            was_updated = True
            break

    if not was_updated:
        # Find table start and insert
        for i, line in enumerate(lines):
            if line.strip().startswith("|") and "---" in lines[i + 1]:
                lines.insert(i + 2, row)
                break
        else:
            # fallback append
            lines.append(row)

    with open(readme_path, "w") as f:
        f.writelines(lines)

    return "updated" if was_updated else "added"


def delete_paper(title, papers_folder="papers", readme_path="README.md"):
    slug = sanitize_filename(title)
    paper_path = os.path.join(papers_folder, f"{slug}.md")

    if os.path.exists(paper_path):
        os.remove(paper_path)
        print(f"🗑️ Deleted file: {paper_path}")
    else:
        print(f"⚠️ File not found: {paper_path}")

    with open(readme_path, "r") as f:
        lines = f.readlines()

    updated_lines = []
    removed = False
    pattern = f"| [{title}](papers/{slug}.md) |"
    for line in lines:
        if line.startswith(pattern):
            removed = True
            continue
        updated_lines.append(line)

    if removed:
        with open(readme_path, "w") as f:
            f.writelines(updated_lines)
        print(f"✅ Removed entry from {readme_path}")
    else:
        print(f"⚠️ Entry not found in {readme_path}")


def main():
    parser = argparse.ArgumentParser(description="Add or delete an ML paper summary entry.")
    parser.add_argument("--title", required=True, help="Title of the paper")
    parser.add_argument("--year", type=int, help="Year of publication")

    parser.add_argument("--source", help="URL to the paper")
    parser.add_argument("--code", default="", help="URL to the code repo")
    parser.add_argument("--publisher", default="", help="Company or university that published the paper")
    parser.add_argument("--topics", nargs='*', help="List of topics")

    parser.add_argument("--delete", action="store_true", help="Delete the paper by title and year")

    args = parser.parse_args()

    if args.delete:
        delete_paper(args.title.strip())
        return

    paper = {
        "title": args.title.strip(),
        "source": args.source.strip() if args.source else "",
        "code": args.code.strip(),
        "publisher": args.publisher.strip(),
        "year": args.year,
        "topics": args.topics if args.topics else []
    }

    ensure_readme_structure()
    slug = create_paper_md(paper)
    status = add_to_readme(paper, slug)
    print(f"✅ {status.capitalize()}: {paper['title']}\n→ papers/{slug}.md")


if __name__ == "__main__":
    main()
