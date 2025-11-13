import sys
from crawl import get_html, crawl_page, print_list

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

#Chapter 2, lesson 2
# def main():
#     if len(sys.argv) < 2:
#         print("no website provided")
#         sys.exit(1)
#     elif len(sys.argv) > 2:
#         print("too many arguments provided")
#         sys.exit(1)
#     else:
#         print(f"Starting crawl of: {sys.argv[1]}")
#         try:
#             print(get_html(sys.argv[1]))
#         except Exception as e:
#             print(e)

def report(page_data):
    for key in page_data:
        print("========== " + key + " ==========")
        if isinstance(page_data[key], str):
            print(page_data[key])
        else:
            print("Title:")
            print(page_data[key]["h1"])
            print()
            print("Excerpt:")
            print(page_data[key]["first_paragraph"])
            print()
            print("Outgoing links:")
            for link in page_data[key]["outgoing_links"]:
                print(" --- " + link)
            print()
            print("Image urls:")
            for url in page_data[key]["image_urls"]:
                print(" --- " + url)
        print()

def main():
    page_data = None
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        page_data = crawl_page(sys.argv[1])

    print()
    print("==============================")
    print("============REPORT============")
    print("==============================")
    print()

    report(page_data)


if __name__ == "__main__":
    main()
