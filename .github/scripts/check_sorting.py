import re


def check_alphabetical_order(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    sections = re.split(r'^##\s', content, flags=re.MULTILINE)[1:]

    all_sorted = True
    changes = []

    for section in sections:
        lines = section.strip().split('\n')
        section_name = lines[0].strip()
        items = []
        current_subsection = None
        for line in lines[1:]:
            if line.strip().startswith('### '):
                if items:
                    sorted_items = sorted(items, key=lambda x: re.sub(
                        r'\[|\]|\(|\)|`', '', x.lower()))
                    if items != sorted_items:
                        all_sorted = False
                        change = f"In section '{section_name}'"
                        if current_subsection:
                            change += f", subsection '{current_subsection}'"
                        change += ":\n" + "\n".join(sorted_items)
                        changes.append(change)
                current_subsection = line.strip()[4:]
                items = []
            elif line.strip().startswith('- ['):
                items.append(line.strip())

        if items:
            sorted_items = sorted(items, key=lambda x: re.sub(
                r'\[|\]|\(|\)|`', '', x.lower()))
            if items != sorted_items:
                all_sorted = False
                change = f"In section '{section_name}'"
                if current_subsection:
                    change += f", subsection '{current_subsection}'"
                change += ":\n" + "\n".join(sorted_items)
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
