import xml.etree.ElementTree as Et

def is_xml(file_content: str):
    try:
        Et.fromstring(file_content)
        return True
    except Et.ParseError:
        return False
