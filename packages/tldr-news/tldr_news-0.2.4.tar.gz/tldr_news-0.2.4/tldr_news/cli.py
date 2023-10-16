import click
from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Header, Footer
from tldr_news.utils import get_content_by_day, get_days


class Sidebar(Static):
    def __init__(self, days, **kwargs):
        super().__init__(**kwargs)
        self.days = days

    def compose(self) -> ComposeResult:
        for day in self.days:
            yield Button(day, variant="primary", classes="sidebar-btn", id='id' + day)


class TLDRNewsApp(App):
    CSS_PATH = "main.css"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days = get_days()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        content = get_content_by_day(event.button.id[2:])
        self.query_one("#main-content", Static).update(content)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar(id="sidebar", days=self.days)
        yield Static(id="main-content")
        yield Footer()


@click.command()
def cli():
    app = TLDRNewsApp()
    app.run()


if __name__ == "__main__":
    cli()
