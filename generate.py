"""CLI entry point for POM Generator."""
import sys
import argparse
from pathlib import Path
from pom_generator.parser import parse_html
from pom_generator.locator import select_locator
from pom_generator.validator import validate_and_normalize_names
from pom_generator.codegen import generate_pom_class
from collections import namedtuple
from pom_generator import NoElementsFoundError

OUTPUT_DIR = Path(__file__).parent / "output"
LocatedElement = namedtuple('LocatedElement', ['name', 'element', 'locator'])


def main(args=None):
    """
    Main CLI entry point.

    Args:
        args: Command-line arguments (default: sys.argv[1:])
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Generate Playwright POM classes from HTML snippets'
    )
    parser.add_argument('html_file', help='Path to HTML file')
    parser.add_argument(
        '--class-name',
        default='PageObject',
        help='Name for generated class (default: PageObject)'
    )

    parsed_args = parser.parse_args(args)

    try:
        elements = parse_html(parsed_args.html_file)

        names = [elem.attributes.get('id') or
                 elem.attributes.get('name') or
                 elem.attributes.get('text') or
                 f"{elem.type}_{i}"
                 for i, elem in enumerate(elements)]

        normalized_names = validate_and_normalize_names(names)

        located_elements = []
        for elem, name in zip(elements, normalized_names):
            locator = select_locator(elem)
            located_elements.append(LocatedElement(name, elem, locator))

        code = generate_pom_class(located_elements, class_name=parsed_args.class_name)

        OUTPUT_DIR.mkdir(exist_ok=True)
        output_file = OUTPUT_DIR / f"{parsed_args.class_name}.py"
        output_file.write_text(code)

        print(f"Generated {output_file}")

    except NoElementsFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
