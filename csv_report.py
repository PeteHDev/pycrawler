import csv

def write_csv_report(page_data, file_name="report.csv"):
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["page_url",
                                            "h1",
                                            "first_paragraph",
                                            "outgoing_links",
                                            "image_urls"])
        writer.writeheader()
        for page in page_data:
            outgoing_links = ";".join(page_data[page]["outgoing_links"])
            image_urls = ";".join(page_data[page]["image_urls"])
            writer.writerow({
                "page_url": page_data[page]["url"],
                "h1": page_data[page]["h1"],
                "first_paragraph": page_data[page]["first_paragraph"],
                "outgoing_links": outgoing_links,
                "image_urls": image_urls
            })

    print(f"Report written to {file_name}")
