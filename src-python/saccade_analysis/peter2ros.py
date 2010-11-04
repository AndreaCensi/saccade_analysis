
from optparse import OptionParser

description = """

This scripts takes the data in Peter Weir's logs and
put it according to Ros's convention.

"""

def main():
    parser = OptionParser()
    parser.add_option("--peters_pickle", 
                      help="Peter's pickle file")
    parser.add_option("--data", help="Main data directory", default='.')

    (options, args) = parser.parse_args()

