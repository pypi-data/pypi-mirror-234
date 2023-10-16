#!/usr/bin/env python

import os

import click
import jinja2

from ..constants import SAGEMAKER_CONTAINER_PATH_MAIN
from ..log import get_logger, verbosity_option
from ..utils import render_template
from . import rudderlabs

logger = get_logger(__name__)

@click.command(
    epilog="""
Examples:

  1. Generates a new project for Bob:

     $ rlabs new -vv data-apps-leadscoring -t "Lead Scoring" -o ~/Projects

     $ rlabs new -vv <project> -t <title> -o <output_dir>
"""
)
@click.argument("project")
@click.option(
    "-t",
    "--title",
    show_default=True,
    default="New project",
    help="This entry defines the project title. "
    "The project title should be a few words only.  It will appear "
    "at the description of your project and as the title of your "
    "documentation",
)
@click.option(
    "-o",
    "--output-dir",
    help="Directory where to dump the new " "project - must not exist",
)
@verbosity_option()
@rudderlabs.raise_on_error
def new(project, title, output_dir):
    """Creates a folder structure for a new rudderlabs data apps project."""

    # the jinja context defines the substitutions to be performed
    context = dict(
        project=project,
        title=title,
        sagemaker_container_path=SAGEMAKER_CONTAINER_PATH_MAIN,
    )

    # copy the whole template structure and de-templatize the needed files
    if output_dir is None:
        output_dir = os.path.join(os.path.realpath(os.curdir), project)

    logger.info(
        "Creating structure for %s at directory %s", project, output_dir
    )

    project_dir = os.path.join(output_dir, project)
    if os.path.exists(project_dir):
        raise IOError(
            "The project directory %s already exists - cannot "
            "overwrite!" % project_dir
        )

    logger.info("mkdir %s", project_dir)
    os.makedirs(project_dir)

    # base jinja2 engine
    template_loader = jinja2.PackageLoader("rudderlabs.data.apps", os.path.join("templates","project"))
    env = jinja2.Environment(
        loader = template_loader,
        autoescape = jinja2.select_autoescape(["html", "xml"]),
    )

    #Render all files in the template directory
    for k in template_loader.list_templates():
        #ignore .pyc files
        if k.endswith(".pyc"):
            continue
        render_template(env, k, context, project_dir)

    logger.info(f"Creating base {project} structure in {output_dir}")
