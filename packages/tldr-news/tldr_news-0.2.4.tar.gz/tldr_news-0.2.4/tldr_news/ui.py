from typing import Container
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Footer


class Sidebar(Static):

    def compose(self) -> ComposeResult:
        yield Button("Primary!", variant="primary", classes="sidebar-btn")


class MainContent(Static):

    def compose(self) -> ComposeResult:
        yield Container("dadsadssdsd")


class HorizontalLayoutExample(App):
    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar(classes="box", id="sidebar")
        yield Static(classes="box")
        yield Footer()


if __name__ == "__main__":
    app = HorizontalLayoutExample()
    app.run()
