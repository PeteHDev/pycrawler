import sys
from crawl import get_html

# Chapter 2, lesson 1:
# def main():
#     if len(sys.argv) < 2:
#         print("no website provided")
#         sys.exit(1)
#     elif len(sys.argv) > 2:
#         print("too many arguments provided")
#         sys.exit(1)
#     else:
#         print(f"Starting crawl of: {sys.argv[1]}")

def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"Starting crawl of: {sys.argv[1]}")
        try:
            print(get_html(sys.argv[1]))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
