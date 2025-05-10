# reflex_app/backend/table_state.py
import csv
from pathlib import Path
from typing import List

import reflex as rx


class TaxForm(rx.Base):
    """The tax form class."""

    id: int
    form_number: str
    form_name: str
    entity_type: str
    locality_type: str
    locality: str


class TableState(rx.State):
    """The state class."""

    items: List[TaxForm] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[TaxForm]:
        items = self.items

        # Filter items based on selected item
        if self.sort_value:
            items = sorted(
                items,
                key=lambda item: str(getattr(item, self.sort_value)).lower(),
                reverse=self.sort_reverse,
            )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "form_number",
                        "form_name",
                        "entity_type",
                        "locality_type",
                        "locality",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 1
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[TaxForm]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        # Let's add some sample tax forms for now
        self.items = [
            TaxForm(
                id=1,
                form_number="1040",
                form_name="U.S. Individual Income Tax Return",
                entity_type="individual",
                locality_type="federal",
                locality="United States",
            ),
            TaxForm(
                id=2,
                form_number="1120",
                form_name="U.S. Corporation Income Tax Return",
                entity_type="corporation",
                locality_type="federal",
                locality="United States",
            ),
            TaxForm(
                id=3,
                form_number="1065",
                form_name="U.S. Return of Partnership Income",
                entity_type="partnership",
                locality_type="federal",
                locality="United States",
            ),
            TaxForm(
                id=4,
                form_number="1120S",
                form_name="U.S. Income Tax Return for an S Corporation",
                entity_type="scorp",
                locality_type="federal",
                locality="United States",
            ),
            TaxForm(
                id=5,
                form_number="540",
                form_name="California Resident Income Tax Return",
                entity_type="individual",
                locality_type="state",
                locality="California",
            ),
        ]
        self.total_items = len(self.items)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()