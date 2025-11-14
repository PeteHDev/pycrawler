import sys
import asyncio
from crawl import print_list, AsyncCrawler
from csv_report import write_csv_report

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

async def crawl_site_async(base_url, max_pages = 100, max_concurrency=3):
    async with AsyncCrawler(base_url, max_pages, max_concurrency) as crawler:
        return await crawler.crawl()

async def main():
    page_data = None
    crawler_parameters = []
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    crawler_parameters.append(sys.argv[1])
    if len(sys.argv) > 2:
        try:
            max_pages = int(sys.argv[2])
            crawler_parameters.append(max_pages)
        except ValueError:
            print("Invalid <max pages> value")
            sys.exit(1)
    if len(sys.argv) > 3:
        try:
            max_concurrency = int(sys.argv[3])
            crawler_parameters.append(max_concurrency)
        except ValueError:
            print("Invalid <max concurrency> value")
            sys.exit(1)
            
    print(crawler_parameters)
    page_data = await crawl_site_async(*crawler_parameters)

    write_csv_report(page_data)


if __name__ == "__main__":
    asyncio.run(main())
