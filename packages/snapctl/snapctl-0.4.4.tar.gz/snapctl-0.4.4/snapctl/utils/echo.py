from rich import print
# Run `python -m rich.emoji` to get a list of all emojis that are supported

def error(msg: str) -> None:
  print(f"[bold red]Error[/bold red] {msg}")

def info(msg: str) -> None:
  print(f"[bold blue]Info[/bold blue] {msg}")

def success(msg: str) -> None:
  print(f"[green]Success[/green] {msg}")