"""Print the World Series championship results table from Wikipedia."""

import requests
from bs4 import BeautifulSoup

# Source: https://en.wikipedia.org/wiki/List_of_World_Series_champions
URL = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"


def main():
    response = requests.get(
        URL,
        headers={"User-Agent": "IS211-Assignment9-Student/1.0 (educational project)"},
        timeout=20,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the results table using its column names.
    table = next(
        (
            table for table in soup.find_all("table")
            if "Winning team" in table.get_text(" ", strip=True)
            and "Losing team" in table.get_text(" ", strip=True)
            and "Year" in table.get_text(" ", strip=True)[:500]
        ),
        None,
    )
    if table is None:
        print("Could not find the World Series results table. The page layout may have changed.")
        return

    print("WORLD SERIES CHAMPIONSHIP RESULTS")
    print("Source:", URL)
    print("-" * 80)
    for row in table.find_all("tr"):
        for reference in row.select("sup.reference"):
            reference.decompose()
        cells = row.find_all(["th", "td"], recursive=False)
        values = [cell.get_text(" ", strip=True) for cell in cells]
        if values:
            print(" | ".join(values))


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as error:
        print("Unable to load Wikipedia:", error)
