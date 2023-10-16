import json
import os
import pathlib
import uuid

import docker
import jinja2
from loguru import logger

import komodo_cli.printing as printing
from komodo_cli.types import OverlayImageBuildException, OverlayImagePushException

TEMPLATES_DIR = f"{pathlib.Path(__file__).parent.resolve()}/templates/"
TEMPLATE_FILE = "Dockerfile.jinja"

KOMODO_DOCKERFILE_NAME = "komodo.Dockerfile"


class OverlayImages:
    def __init__(self, base_image, source_dir, dest_dir, overlay_images_repository):
        self.base_image = base_image
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.overlay_images_repository = overlay_images_repository
        self.client = docker.from_env()

    def generate_dockerfile(self) -> str:
        templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(TEMPLATE_FILE)
        output = template.render(
            base_image=self.base_image,
            dest_dir=self.dest_dir,
        )
        return output

    def build_overlay_image(self):
        dockerfile = self.generate_dockerfile()
        dockerfile_path = os.path.join(self.source_dir, KOMODO_DOCKERFILE_NAME)
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile)

        try:
            image, build_logs = self.client.images.build(
                path=os.path.dirname(dockerfile_path),
                tag=f"{self.overlay_images_repository}:{str(uuid.uuid4())}",
                quiet=False,
                rm=True,
                pull=True,
                forcerm=True,
                dockerfile=dockerfile_path,
                platform="linux/amd64",  # TODO
            )
            return image
        except (
            docker.errors.BuildError,
            docker.errors.APIError,
            TypeError,
        ) as e:
            raise OverlayImageBuildException(str(e))
        except Exception as e:
            raise e

    def push_overlay_image(self, image):
        try:
            resp = self.client.images.push(
                self.overlay_images_repository,
                image.tags[0].split(":")[-1],
                stream=True,
                decode=True,
            )

            for line in resp:
                if "error" in line:
                    raise OverlayImagePushException(line["error"])
        except Exception as e:
            raise OverlayImagePushException(str(e))
