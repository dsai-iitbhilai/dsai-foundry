import re

import requests


class WikipediaEnv:
    """Minimal Wikipedia environment with Search and Lookup."""

    URL = "https://en.wikipedia.org/w/api.php"
    HEADERS = {"User-Agent": "react-learning-agent/1.0"}

    def __init__(self):
        self.page_text = ""
        self.lookup_keyword = ""
        self.lookup_pos = 0

    def reset(self):
        self.page_text = ""
        self.lookup_keyword = ""
        self.lookup_pos = 0

    def step(self, action: str, action_input: str) -> str:
        action = action.lower().strip()

        if action == "search":
            return self.search(action_input)
        if action == "lookup":
            return self.lookup(action_input)
        if action == "finish":
            return action_input

        return "Unknown action. Use Search, Lookup, or Finish."

    def search(self, entity: str) -> str:
        entity = entity.strip()

        params = {
            "action": "query",
            "titles": entity,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "format": "json",
        }

        try:
            res = requests.get(self.URL, params=params, headers=self.HEADERS, timeout=15)
            data = res.json()
            pages = data.get("query", {}).get("pages", {})
            page = next(iter(pages.values()))

            if "missing" in page:
                return self._search_similar(entity)

            text = page.get("extract", "").strip()
            if not text:
                return self._search_similar(entity)

            self.page_text = text
            self.lookup_keyword = ""
            self.lookup_pos = 0

            sentences = self._split_sentences(text)
            return " ".join(sentences[:5])
        except Exception as exc:
            return f"Search error: {exc}"

    def lookup(self, keyword: str) -> str:
        if not self.page_text:
            return "No page loaded. Run Search first."

        keyword = keyword.strip().lower()
        if keyword != self.lookup_keyword:
            self.lookup_keyword = keyword
            self.lookup_pos = 0

        sentences = self._split_sentences(self.page_text)
        matches = [s for s in sentences if keyword in s.lower()]

        if not matches:
            return f"Keyword '{keyword}' not found in current page."

        if self.lookup_pos >= len(matches):
            self.lookup_pos = 0

        out = matches[self.lookup_pos]
        self.lookup_pos += 1
        return out

    def _search_similar(self, query: str) -> str:
        params = {
            "action": "opensearch",
            "search": query,
            "limit": 5,
            "format": "json",
        }

        try:
            res = requests.get(self.URL, params=params, headers=self.HEADERS, timeout=15)
            data = res.json()
            suggestions = data[1] if len(data) > 1 else []
            if suggestions:
                return f"Not found. Similar entities: {suggestions}"
            return "Not found."
        except Exception as exc:
            return f"Search error: {exc}"

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        return [s.strip() for s in re.split(r"(?<=[.!?])\\s+", text) if s.strip()]
