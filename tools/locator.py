LOCATION_STRATEGIES = {
    "css": "css selector",
    "xpath": "xpath",
    "id": "id",
    "link": "link text",
    "part_link": "partial link text",
    "name": "name",
    "tag": "tag name",
    "class_": "class name",
}


class Locator:
    """
    Объект преобразования локатора
    """

    def __init__(self, **by):
        by, value = next(iter(by.items()))
        if by == "text":
            self.by = "xpath"
            self.value = f"//*[contains(text(), '{value}')]"
        else:
            self.by = LOCATION_STRATEGIES.get(by)
            if not self.by:
                raise Exception(
                    f"Неизвестная стратегия '{by}'. Используй одну из: {list(LOCATION_STRATEGIES.keys())}")
            self.value = value

    def __str__(self):
        return f"\"{self.by}={self.value}\""
