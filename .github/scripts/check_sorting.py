import re


def clean_item(item):
    return re.sub(r'\[|\]|\(|\)|`', '', item[0].split('\n')[0].lower())


def sort_items(items):
    return sorted(items, key=lambda x: clean_item(x))


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
            items = []
            current_item = None
            for line in sublines[1:]:
                if line.strip().startswith('- ['):
                    if current_item:
                        items.append(current_item)
                    current_item = [line.strip(), []]
                elif line.strip() and current_item:
                    current_item[0] += '\n  ' + line.strip()

            if current_item:
                items.append(current_item)

            sorted_items = sort_items(items)
            if items != sorted_items:
                all_sorted = False
                change = f"In section '{section_name}', subsection '{subsection_name}':\n"
                for item in sorted_items:
                    change += item[0] + '\n'
                    for subitem in item[1]:
                        change += subitem + '\n'
                changes.append(change.strip())

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
