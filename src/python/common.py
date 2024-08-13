from typing import List

from pyscript import document

from src.python.model import DataSourceDetails

output_option_id_prefix = "output-"
input_option_id_prefix = "input-"


def set_options(
        options_list: List[DataSourceDetails],
        select_element,
        id_prefix,
        editor,
        examples: dict = None
):
    for opt in options_list:
        option_element = document.createElement("option")
        option_element.value = opt.name
        option_element.innerText = opt.display_name
        option_element.setAttribute("id", f'{id_prefix}{opt.name}')
        if opt.additional_opts:
            for key, value in opt.additional_opts.items():
                option_element.setAttribute(key, value)
        if opt.is_default:
            option_element.setAttribute("selected", "")
        if opt.example_file and id_prefix == input_option_id_prefix:
            f = open(opt.example_file, "r")
            examples[opt.name] = f.read()
            f.close()
            if opt.is_default:
                editor.session.setValue(examples[opt.name])
        select_element.append(option_element)


def set_editor_mode(id_prefix, editor_type, editor):
    option = document.getElementById(f"{id_prefix}{editor_type}")
    editor_mode = option.getAttribute("editor_mode")
    editor.session.setMode(f'ace/mode/{editor_mode}')
