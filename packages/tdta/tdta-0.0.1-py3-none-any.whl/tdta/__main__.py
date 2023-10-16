import argparse
import pathlib
from tdta.purl_publish import publish_to_purl


def main():
    parser = argparse.ArgumentParser(prog="tdta", description='TDT actions cli interface.')
    subparsers = parser.add_subparsers(help='Available TDT actions', dest='action')

    parser_purl = subparsers.add_parser("purl-publish",
                                            description="The PURL publication parser",
                                            help="Published the given taxonomy to the PURL system.")
    parser_purl.add_argument('-i', '--input', action='store', type=pathlib.Path, required=True)
    parser_purl.add_argument('-t', '--taxonomy', required=True)
    parser_purl.add_argument('-u', '--user', required=True)

    args = parser.parse_args()

    if args.action == "purl-publish":
        publish_to_purl(str(args.input), str(args.taxonomy), str(args.user))


if __name__ == "__main__":
    main()
