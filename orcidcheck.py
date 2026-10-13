import os
import xml.etree.ElementTree as ET

folder = "."

total_orcids = 0
filled_orcids = 0
empty_orcids = 0
missing = []


def clean_tag(tag):
    """Remove XML namespace and normalize tag name."""
    if "}" in tag:
        tag = tag.split("}", 1)[1]
    return tag.lower()


def get_text(element):
    """Safely get stripped text."""
    if element is not None and element.text:
        return element.text.strip()
    return ""


def find_first_text(root, possible_tags):
    """Find the first matching tag under a specific element."""
    possible_tags = [x.lower() for x in possible_tags]

    for elem in root.iter():
        if clean_tag(elem.tag) in possible_tags:
            value = get_text(elem)
            if value:
                return value

    return ""


def get_author_name(author):
    """Get author name from first/middle/last name."""

    first = find_first_text(
        author,
        ["first_name", "firstname", "first", "given_name", "givenname"]
    )

    middle = find_first_text(
        author,
        ["middle_name", "middlename", "middle"]
    )

    last = find_first_text(
        author,
        ["last_name", "lastname", "last", "family_name",
         "familyname", "surname"]
    )

    parts = [x for x in [first, middle, last] if x]

    if parts:
        return " ".join(parts)

    return "(Author name not found)"


for filename in os.listdir(folder):

    if not filename.lower().endswith(".xml"):
        continue

    filepath = os.path.join(folder, filename)

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Build parent lookup so we can move upward
        parent_map = {
            child: parent
            for parent in root.iter()
            for child in parent
        }

        # Find every ORCID tag
        for elem in root.iter():

            if clean_tag(elem.tag) != "orcid":
                continue

            total_orcids += 1

            orcid_value = get_text(elem)

            if orcid_value:
                filled_orcids += 1
                continue

            empty_orcids += 1

            # --------------------------------------------------
            # Find the enclosing AUTHOR
            # --------------------------------------------------
            current = elem
            author_element = None

            while current in parent_map:
                current = parent_map[current]

                if clean_tag(current.tag) == "author":
                    author_element = current
                    break

            if author_element is not None:
                author_name = get_author_name(author_element)
            else:
                author_name = "(Author not found)"

            # --------------------------------------------------
            # Find the enclosing PAPER
            # --------------------------------------------------
            current = elem
            paper_element = None

            while current in parent_map:
                current = parent_map[current]

                if clean_tag(current.tag) == "paper":
                    paper_element = current
                    break

            # Get article number ONLY from this paper
            if paper_element is not None:
                article_number = find_first_text(
                    paper_element,
                    ["published_article_number"]
                )

                # Fallback to event_tracking_number if somehow missing
                if not article_number:
                    article_number = find_first_text(
                        paper_element,
                        ["event_tracking_number"]
                    )
            else:
                article_number = ""

            if not article_number:
                article_number = "(Article number not found)"

            missing.append({
                "article_number": article_number,
                "author": author_name,
                "file": filename
            })

    except ET.ParseError as e:
        print(f"Could not parse {filename}: {e}")


print("\n===================================")
print("ORCID SUMMARY")
print("===================================")
print(f"Total ORCID tags : {total_orcids}")
print(f"With ORCID       : {filled_orcids}")
print(f"Empty ORCID      : {empty_orcids}")

print("\n===================================")
print("AUTHORS WITH MISSING ORCID")
print("===================================")

if missing:
    for item in missing:
        print(
            f"Article: {item['article_number']} | "
            f"Author: {item['author']} | "
            f"File: {item['file']}"
        )
else:
    print("None! All authors have ORCIDs.")