import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from bs4 import BeautifulSoup,SoupReplacer

def change_tags(input_path):
    """
    Read an HTML/XML file, parse it, find all the <b> tags, change them into <blockquote> and save the changed file.
    """
    try:
        # Determine file type based on extension to use appropriate parser
        if input_path.endswith(('.html', '.htm')):
            parser = 'html.parser'
        elif input_path.endswith('.xml'):
            parser = 'lxml-xml'
        else:
            print("Error: Unsupported file type. Please provide HTML or XML file.")
            return

        # Read the input file
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the content into a tree structure
        b_to_blockquote = SoupReplacer("b","blockquote")
        soup = BeautifulSoup(content, parser,replacer=b_to_blockquote)

        name_parts = input_path.rsplit('.', 1)
        output_path = f"{name_parts[0]}_bTags.{name_parts[1]}"

        # Write the pretty-printed version to disk
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        print(f"Successfully change all the <b> tags: {output_path}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")



# Check if a file path was provided as command line argument
if len(sys.argv) != 2:
    print("Usage: python task1.py <path_to_html_or_xml_file>")
    sys.exit(1)

# Get the file path from command line argument
input_file_path = sys.argv[1]
change_tags(input_file_path)