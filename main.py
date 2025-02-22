import requests
from collections import deque
import time

def safe_input(msg: str, datatype = str):
    while True:
        try:
            text = input(msg)
            value = datatype(text)
            if value == "":
                print("Input cannot be empty")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please only {datatype.__name__} is allowed")

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

def get_wikipedia_links(title):
    links = set()
    plcontinue = None  # Token für Pagination

    while True:
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "links",
            "pllimit": "max"
        }
        if plcontinue:
            params["plcontinue"] = plcontinue

        try:
            response = requests.get(WIKI_API_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return set() # Error handling

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "links" in page:
                for link in page["links"]:
                    # Skip non-article pages (e.g., Help, Category, etc.)
                    if not any(link["title"].startswith(prefix) for prefix in ["Help:", "Category:", "File:", "Wikipedia:", "Template:", "Portal:", "Book:", "Draft:", "Module:"]):
                        links.add(link["title"])

        plcontinue = data.get("continue", {}).get("plcontinue")
        if not plcontinue:
            break  # No more pages

    return links

def bidirectional_bfs(start, goal):
    if start == goal:
        return [start]

    queue_start = deque([(start, [start])])
    queue_goal = deque([(goal, [goal])])
    visited_start = {start: [start]}
    visited_goal = {goal: [goal]}

    while queue_start and queue_goal:
        if len(queue_start) < len(queue_goal):
            result = expand_queue(queue_start, visited_start, visited_goal)
        else:
            result = expand_queue(queue_goal, visited_goal, visited_start)

        if result:
            return result

    return None  # No path found

def expand_queue(queue, visited_from, visited_other):
    current, path = queue.popleft()
    for link in get_wikipedia_links(current):
        if link in visited_other:  # path found
            return path + visited_other[link][::-1]

        if link not in visited_from:
            visited_from[link] = path + [link]
            queue.append((link, path + [link]))

    return None

def main():
    print("Welcome to Wikipedia Path Finder/Speedrunner")
    while True:
        start_article = safe_input("Enter the start article: ")
        goal_article = safe_input("Enter the goal article: ")
        print("Searching for path...")
        path = bidirectional_bfs(start_article, goal_article)
        print(" -> ".join(path) if path else "No path found.")
        time.sleep(1)
        response = safe_input("Do you want to make another Search? [y/n]: ", str)
        if response.lower() != "y":
            time.sleep(1)
            print("By Tamino1230...")
            time.sleep(1)
            print("Exiting..")
            time.sleep(1)
            break
        else:
            continue

if __name__ == "__main__":
    main()
