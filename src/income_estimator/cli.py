"""
Command-line interface for the Income Estimator ML project.
"""

import json
from pathlib import Path
from typing import List, Optional

import click
import uvicorn
from rich.console import Console
from rich.table import Table

from .config import get_config, load_config
from .logger import get_logger, setup_logging

console = Console()
logger = get_logger(__name__)


@click.group()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    help="Set logging level",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def main(config: Optional[str], log_level: Optional[str], verbose: bool) -> None:
    """Income Estimator ML - Production-ready ML pipeline for income estimation."""
    if config:
        load_config(config)
    
    if log_level:
        setup_logging(log_level=log_level)
    
    if verbose:
        setup_logging(log_level="DEBUG")


@main.command()
@click.option(
    "--data-path",
    type=click.Path(exists=True),
    help="Path to training data CSV file",
)
@click.option(
    "--algorithms",
    multiple=True,
    type=click.Choice([
        "random_forest",
        "gradient_boosting", 
        "logistic_regression",
        "svm",
        "neural_network"
    ]),
    help="Algorithms to train (can be specified multiple times)",
)
@click.option(
    "--no-tune",
    is_flag=True,
    help="Skip hyperparameter tuning",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    help="Directory to save trained models",
)
def train(
    data_path: Optional[str],
    algorithms: List[str],
    no_tune: bool,
    output_dir: Optional[str],
) -> None:
    """Train machine learning models."""
    config = get_config()
    
    console.print("[bold blue]Starting model training...[/bold blue]")
    
    # Import here to avoid circular imports
    from .models.trainer import ModelTrainer
    
    trainer = ModelTrainer(config)
    
    # Set algorithms if specified
    if algorithms:
        config.model.algorithms = list(algorithms)
    
    # Set hyperparameter tuning
    if no_tune:
        config.model.hyperparameter_tuning = False
    
    try:
        results = trainer.train(
            data_path=data_path,
            output_dir=output_dir,
        )
        
        console.print("[bold green]Training completed successfully![/bold green]")
        
        # Display results
        table = Table(title="Training Results")
        table.add_column("Algorithm", style="cyan")
        table.add_column("Accuracy", style="magenta")
        table.add_column("F1 Score", style="green")
        
        for result in results:
            table.add_row(
                result["algorithm"],
                f"{result['accuracy']:.4f}",
                f"{result['f1_score']:.4f}",
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Training failed: {e}[/bold red]")
        logger.error(f"Training failed: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host to bind the server to",
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind the server to",
)
@click.option(
    "--reload",
    is_flag=True,
    help="Enable auto-reload for development",
)
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of worker processes",
)
def serve(host: str, port: int, reload: bool, workers: int) -> None:
    """Start the API server."""
    config = get_config()
    
    console.print(f"[bold blue]Starting API server on {host}:{port}[/bold blue]")
    
    try:
        uvicorn.run(
            "income_estimator.api.app:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else 1,
            log_level=config.api.log_level,
        )
    except Exception as e:
        console.print(f"[bold red]Server failed to start: {e}[/bold red]")
        logger.error(f"Server failed to start: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    help="JSON file with prediction input",
)
@click.option(
    "--model-id",
    help="Specific model ID to use for prediction",
)
@click.option(
    "--output-file",
    type=click.Path(),
    help="File to save prediction results",
)
def predict(
    input_file: Optional[str],
    model_id: Optional[str],
    output_file: Optional[str],
) -> None:
    """Make predictions using trained models."""
    from .models.predictor import ModelPredictor
    
    config = get_config()
    predictor = ModelPredictor(config)
    
    try:
        if input_file:
            # Load input from file
            with open(input_file, "r") as f:
                input_data = json.load(f)
        else:
            # Interactive input
            console.print("[bold blue]Enter prediction data:[/bold blue]")
            input_data = {}
            
            # Collect input interactively
            input_data["age"] = click.prompt("Age", type=int)
            input_data["education_num"] = click.prompt("Education years", type=int)
            input_data["hours_per_week"] = click.prompt("Hours per week", type=int)
            input_data["capital_gain"] = click.prompt("Capital gain", type=int, default=0)
            input_data["capital_loss"] = click.prompt("Capital loss", type=int, default=0)
            input_data["education"] = click.prompt("Education level")
            input_data["occupation"] = click.prompt("Occupation")
            input_data["marital_status"] = click.prompt("Marital status")
            input_data["relationship"] = click.prompt("Relationship")
            input_data["race"] = click.prompt("Race")
            input_data["sex"] = click.prompt("Sex")
            input_data["native_country"] = click.prompt("Native country")
        
        # Make prediction
        result = predictor.predict(input_data, model_id=model_id)
        
        # Display result
        console.print(f"[bold green]Prediction: {result['prediction']}[/bold green]")
        console.print(f"Confidence: {result['confidence']:.4f}")
        
        # Save to file if specified
        if output_file:
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            console.print(f"Results saved to {output_file}")
        
    except Exception as e:
        console.print(f"[bold red]Prediction failed: {e}[/bold red]")
        logger.error(f"Prediction failed: {e}")
        raise click.ClickException(str(e))


@main.command()
@click.option(
    "--model-name",
    help="Filter by model name",
)
@click.option(
    "--limit",
    default=10,
    type=int,
    help="Maximum number of models to show",
)
def list_models(model_name: Optional[str], limit: int) -> None:
    """List available trained models."""
    from .models.registry import ModelRegistry
    
    config = get_config()
    registry = ModelRegistry(config)
    
    try:
        models = registry.list_models(
            model_name=model_name,
            limit=limit,
        )
        
        if not models:
            console.print("[yellow]No models found.[/yellow]")
            return
        
        # Display models in a table
        table = Table(title="Available Models")
        table.add_column("Model ID", style="cyan")
        table.add_column("Algorithm", style="magenta")
        table.add_column("Accuracy", style="green")
        table.add_column("Created", style="blue")
        
        for model in models:
            table.add_row(
                model["model_id"],
                model["algorithm"],
                f"{model['accuracy']:.4f}",
                model["created_at"],
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[bold red]Failed to list models: {e}[/bold red]")
        logger.error(f"Failed to list models: {e}")
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()
