from __future__ import annotations

from rich.table import Table

from ..sdk.slingshot_sdk import SlingshotSDK
from ..sdk.utils import console
from .config.slingshot_cli import SlingshotCLIApp

app = SlingshotCLIApp()


@app.command(name="machines")
async def list_machines(sdk: SlingshotSDK) -> None:
    """Lists all machines available to the user in a table format."""
    all_machine_types = await sdk.list_machine_types()
    table = Table(title=f"Machine Types")
    table.add_column("Machine Type", style="cyan")
    table.add_column("Number of GPUs", style="cyan")
    table.add_column("GPU VRAM", style="cyan")
    table.add_column("CPU", style="cyan")
    table.add_column("RAM", style="cyan")
    table.add_column("Cost", style="cyan")

    for machine_type in all_machine_types:
        name = machine_type.name
        details = machine_type.details
        for gpu_count_machine_size in details.gpu_count_machine_sizes:
            machine_costs = gpu_count_machine_size.machine_costs
            gpu_vram = str(details.vram_gb) + "GB" if details.vram_gb else "-"
            gpu_count = str(gpu_count_machine_size.specs.gpu_limit)
            cpu = gpu_count_machine_size.specs.cpu_limit + " cores"
            ram = gpu_count_machine_size.specs.memory_limit.replace("Gi", "GB")
            credits_per_sec = (
                machine_costs.cpu_credits_per_sec
                + machine_costs.mem_credits_per_sec
                + machine_costs.gpu_credits_per_sec
            )
            cost_per_hour = credits_per_sec * 3600 / 1000
            table.add_row(name, gpu_count, gpu_vram, cpu, ram, f"~${cost_per_hour:.2f}/hour")
    console.print(table)
    console.print(
        "💡 To specify a machine type in your [yellow]slingshot.yaml[/yellow], "
        "set the [cyan]machine_type[/cyan] field to the value of the 'Machine Type' column, "
        "and the [cyan]num_gpu[/cyan] field to the number of GPUs you want to use (defaults to 0 for CPU "
        "machine types and 1 for GPU).\n"
    )
