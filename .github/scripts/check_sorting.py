import re


def clean_item(item):
    return re.sub(r'\[|\]|\(|\)|`', '', item.split('\n')[0].lower())


def check_alphabetical_order(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    sections = re.split(r'^##\s', content, flags=re.MULTILINE)[1:]

    all_sorted = True
    changes = []

    for section in sections:
        lines = section.strip().split('\n')
        section_name = lines[0].strip()
        subsections = re.split(r'^###\s', section, flags=re.MULTILINE)[1:]

        for subsection in subsections:
            sublines = subsection.strip().split('\n')
            subsection_name = sublines[0].strip()
            items = [line.strip() for line in sublines[1:]
                     if line.strip().startswith('- [')]

            sorted_items = sorted(items, key=clean_item)
            if items != sorted_items:
                all_sorted = False
                change = f"In section '{section_name}', subsection '{subsection_name}':\n"
                change += "\n".join(sorted_items)
                changes.append(change)

    return all_sorted, changes


def main():
    all_sorted, changes = check_alphabetical_order('README.md')
    if not all_sorted:
        print("Suggested changes:")
        for change in changes:
            print(change)
            print()
        exit(1)
    else:
        print("All sections and subsections are in alphabetical order!")


if __name__ == "__main__":
    main()
