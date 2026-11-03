"""Print the Super Bowl championship results table from Wikipedia."""

import requests
from bs4 import BeautifulSoup

# Source: https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions
URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"


def main():
    response = requests.get(
        URL,
        headers={"User-Agent": "IS211-Assignment9-Student/1.0 (educational project)"},
        timeout=20,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the results table, rather than assuming it is the first table.
    table = next(
        (
            table for table in soup.find_all("table")
            if "Winning team" in table.get_text(" ", strip=True)
            and "Losing team" in table.get_text(" ", strip=True)
            and "Game" in table.get_text(" ", strip=True)[:500]
        ),
        None,
    )
    if table is None:
        print("Could not find the Super Bowl results table. The page layout may have changed.")
        return

    print("SUPER BOWL CHAMPIONSHIP RESULTS")
    print("Source:", URL)
    print("-" * 80)
    for row in table.find_all("tr"):
        # Exclude citation markers like [1] from displayed text.
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
