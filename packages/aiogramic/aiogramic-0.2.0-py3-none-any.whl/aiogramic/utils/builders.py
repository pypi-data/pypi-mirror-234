from os.path import join
from os.path import dirname

from jinja2 import FileSystemLoader
from jinja2 import Environment
from jinja2 import Template


class TemplateBuilder:

    __root_folder__ = join(dirname(__file__), "../templates")

    templates_loader: FileSystemLoader
    template_environment: Environment

    def __init__(self):

        self.templates_loader = FileSystemLoader(self.__root_folder__)
        self.template_environment = Environment(loader=self.templates_loader)

    def __get_template(self, template_location: str) -> Template:
        return self.template_environment.get_template(template_location)

    def build(
            self,
            template_location: str,
            *args,
            **kwargs
    ) -> str:
        template = self.__get_template(template_location)
        result = template.render(*args, **kwargs)
        return result
