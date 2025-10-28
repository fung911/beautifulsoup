import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from bs4 import BeautifulSoup,SoupStrainer



def find_hyperlinks(input_path):
    """
    Read an HTML/XML file, parse it, find all the <a> tags.
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
        only_a_tags = SoupStrainer("a")

        print(BeautifulSoup(content, parser, parse_only=only_a_tags).prettify())

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
find_hyperlinks(input_file_path)