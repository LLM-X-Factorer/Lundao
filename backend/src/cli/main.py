"""
CLI tool for paper processing.
"""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from src.core.config import get_settings
from src.core.state import create_initial_state
from src.core.workflow import run_workflow
from src.utils.file_handler import load_paper_materials, save_output
from src.utils.logger import setup_logger, get_logger

# Initialize Typer app
app = typer.Typer(
    name="lundao",
    help="Academic paper presentation automation system",
    add_completion=False,
)

console = Console()


@app.command()
def process(
    paper_dir: Path = typer.Argument(..., help="Directory containing paper materials"),
    output_dir: Path = typer.Option(
        None, "--output-dir", "-o", help="Output directory (default: from config)"
    ),
    skip_gamma: bool = typer.Option(False, "--skip-gamma", help="Skip Gamma API call"),
):
    """Process a paper and generate PPT blueprint and documents."""
    # Setup logger
    setup_logger()
    logger = get_logger(__name__)

    console.print("[bold blue]Lundao Paper Processor[/bold blue]")
    console.print(f"Processing paper from: {paper_dir}\n")

    try:
        # Load paper materials
        with console.status("[bold green]Loading paper materials..."):
            paper_md, paper_meta, image_paths, paper_id = load_paper_materials(paper_dir)

        console.print(f"[green]✓[/green] Loaded paper: {paper_id}")
        console.print(f"  - Markdown: {len(paper_md)} chars")
        console.print(f"  - Images: {len(image_paths)} files")
        console.print(f"  - Metadata: {len(paper_meta)} fields\n")

        # Create initial state
        initial_state = create_initial_state(
            paper_md=paper_md,
            paper_meta=paper_meta,
            image_paths=image_paths,
            paper_id=paper_id,
        )

        # Run workflow
        console.print("[bold yellow]Running workflow...[/bold yellow]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing...", total=None)

            # Run async workflow
            final_state = asyncio.run(run_workflow(initial_state))

            progress.update(task, completed=True)

        # Display results
        console.print("\n[bold green]Workflow completed![/bold green]\n")

        # Create results table
        table = Table(title="Results")
        table.add_column("Task", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Time (s)", style="yellow", justify="right")

        for node, exec_time in final_state["execution_time"].items():
            table.add_row(node, "✓", f"{exec_time:.2f}")

        console.print(table)

        # Display errors if any
        if final_state["errors"]:
            console.print("\n[bold red]Errors:[/bold red]")
            for error in final_state["errors"]:
                console.print(f"  [red]✗[/red] {error}")

        # Save outputs
        settings = get_settings()
        output_dir_final = output_dir or settings.output_dir

        console.print(f"\n[bold blue]Saving outputs to: {output_dir_final}[/bold blue]")

        save_output(
            output_dir=output_dir_final,
            paper_id=paper_id,
            p1_markdown=final_state.get("p1_markdown"),
            p2_document=final_state.get("p2_document"),
            p3_article=final_state.get("p3_article"),
            p4_script=final_state.get("p4_script"),
            gamma_ppt_url=final_state.get("gamma_ppt_url"),
            metadata={
                "execution_time": final_state["execution_time"],
                "errors": final_state["errors"],
            },
        )

        console.print("[green]✓[/green] Outputs saved successfully")

        if final_state.get("gamma_ppt_url"):
            console.print(f"\n[bold]Gamma PPT URL:[/bold] {final_state['gamma_ppt_url']}")

        if final_state.get("gamma_export_path"):
            console.print(f"[bold]Gamma Export:[/bold] {final_state['gamma_export_path']}")

        console.print("\n[bold green]Done![/bold green]")

    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {e}")
        logger.exception("CLI execution failed")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show version information."""
    console.print("Lundao Backend P2P3 v0.1.0")


if __name__ == "__main__":
    app()
