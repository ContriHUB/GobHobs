import json
import os
import sys
from collections import Counter


def order_json_by_keywords(json_file, keywords, output_file):
    #give the logic here
    ans="Not implemented"
    return ans


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ordering.py <json_file> <keyword1> <keyword2> ... <output_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    keywords = sys.argv[2:-1]
    output_file = sys.argv[-1]
    order_json_by_keywords(json_file, keywords, output_file)
