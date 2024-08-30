import re

def check_alphabetical_order(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    sections = re.split(r'^##\s', content, flags=re.MULTILINE)[1:]

    all_sorted = True
    errors = []
    for section in sections:
        lines = section.strip().split('\n')
        section_name = lines[0].strip()
        items = [line.strip()
                 for line in lines[1:] if line.strip().startswith('- [')]

        sorted_items = sorted(items, key=lambda x: re.sub(
            r'\[|\]|\(|\)|`', '', x.lower()))

        if items != sorted_items:
            all_sorted = False
            error_message = f"Error: Items in section '{section_name}' are not in alphabetical order\n"
            error_message += "Suggested order:\n"
            error_message += "\n".join(f"  {item}" for item in sorted_items)
            error_message += "\n\nCurrent order:\n"
            error_message += "\n".join(f"  {item}" for item in items)
            error_message += "\n\n"
            errors.append(error_message)

    return all_sorted, errors

def main():
    all_sorted, errors = check_alphabetical_order('README.md')
    if not all_sorted:
        print("Alphabetical order check failed.")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("All sections are in alphabetical order!")

if __name__ == "__main__":
    main()
