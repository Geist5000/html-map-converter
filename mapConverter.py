import json
import sys, getopt
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag


def main(argv):
    input_file = ''
    output_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    print('Input file is "', input_file)
    print('Output file is "', output_file)
    loaded_html = process_html(input_file)
    write_json(output_file, loaded_html)
    print("converted!")


def process_html(input_file: str) -> dict:
    soup = load_html(input_file)
    map_tags = find_map_tags(soup)
    map_tag: Tag
    if len(map_tags) > 1:
        i = int(input("index von map tag:"))
        map_tag = map_tags[i]
    else:
        map_tag = map_tags[0]

    result_dict = convert_map_to_dict(map_tag)
    area_tags = find_area_tags(map_tag)
    area_list = list()
    for area_tag in area_tags:
        area_list.append(convert_area_to_dict(area_tag))
    result_dict['areas'] = area_list

    return result_dict


def load_html(input_file: str):
    with open(input_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser", from_encoding="utf-8")
        soup.encode("utf-8")
    if soup:
        return soup
    else:
        raise Exception("couldn't load html")


def write_json(output_file: str, data: dict):
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))


def find_map_tags(soup: BeautifulSoup) -> ResultSet:
    return soup.find_all('map')


def find_area_tags(map_tag: Tag):
    return map_tag.find_all("area")


def convert_map_to_dict(map_tag: Tag) -> dict:
    wanted_keys = ['name']
    return extract_attributes(map_tag, wanted_keys)


def convert_area_to_dict(area_tag: Tag) -> dict:
    wanted_keys = ['alt', 'coords', 'href', 'shape', 'target', 'title']  # The keys you want
    return extract_attributes(area_tag, wanted_keys)


def extract_attributes(tag: Tag, wanted_keys) -> dict:
    return dict((k, tag.attrs[k]) for k in wanted_keys if k in tag.attrs)


if __name__ == "__main__":
    main(sys.argv[1:])
