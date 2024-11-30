import os
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_URL = "https://adityainduraj.github.io/library"  # Replace with your GitHub Pages URL
OUTPUT_FILE = "feed.xml"

def generate_opds(directory):
    feed = ET.Element("feed", attrib={
        "xmlns": "http://www.w3.org/2005/Atom",
        "xmlns:opds": "http://opds-spec.org/2010/catalog"
    })
    ET.SubElement(feed, "title").text = "My eBooks Catalog"
    ET.SubElement(feed, "id").text = f"{BASE_URL}/{OUTPUT_FILE}"
    ET.SubElement(feed, "updated").text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    ET.SubElement(feed, "author").append(ET.Element("name", text="Your Name"))

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".epub"):
                file_path = os.path.relpath(os.path.join(root, file), directory)
                file_url = f"{BASE_URL}/{file_path.replace(os.sep, '/')}"
                entry = ET.SubElement(feed, "entry")
                ET.SubElement(entry, "title").text = os.path.splitext(file)[0]
                ET.SubElement(entry, "id").text = file_url
                ET.SubElement(entry, "updated").text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                ET.SubElement(entry, "link", attrib={"rel": "alternate", "href": file_url, "type": "application/epub+zip"})
                ET.SubElement(entry, "summary").text = "Description goes here."

    tree = ET.ElementTree(feed)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    generate_opds("ebooks")

