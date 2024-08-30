import re


def check_alphabetical_order(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    sections = re.split(r'^##\s', content, flags=re.MULTILINE)[1:]

    for section in sections:
        lines = section.strip().split('\n')
        section_name = lines[0].strip()
        items = [line.strip()
                 for line in lines[1:] if line.strip().startswith('- [')]

        sorted_items = sorted(items, key=lambda x: re.sub(
            r'\[|\]|\(|\)|`', '', x.lower()))

        if items != sorted_items:
            print(
                f"Error: Items in section '{section_name}' are not in alphabetical order")
            return False

    return True


def main():
    if not check_alphabetical_order('README.md'):
        exit(1)
    print("All sections are in alphabetical order!")


if __name__ == "__main__":
    main()
