from pathlib import Path
from typing import List, Dict

from bson import ObjectId
from jinja2 import Environment, FileSystemLoader

template_path = Path(__file__).parent / "templates"


def load_template_files(project: Dict) -> List[tuple[str, str]]:
    """
    Load template files from the templates folder and render them.
    Args:
        project: project data
    Returns:
        List[tuple[str, str]]: List of tuples with file name and file content.
    """
    loader = FileSystemLoader(template_path)
    env = Environment(loader=loader)
    files: List[tuple[str, str]] = []

    pipeline_template = env.get_template("hello_world.py.jinja")
    rendered_pipeline_template = pipeline_template.render()
    files.append(("first_pipeline.py", rendered_pipeline_template))

    config_template = env.get_template("config.yml.jinja")
    rendered_config_template = config_template.render(
        project_id=project.get("_id"),
        project_name=project.get("name"),
        pipeline_id=ObjectId(),
    )
    files.append(("config.yml", rendered_config_template))

    return files
