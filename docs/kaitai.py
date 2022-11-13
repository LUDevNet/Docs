import os
import yaml
from docutils.parsers.rst import Directive, directives
from docutils import nodes


class Kaitai(Directive):
    required_arguments = 1
    final_argument_whitespace = True
    has_content = False

    def data(self, data):
        if isinstance(data, list):
            node = nodes.enumerated_list()
            for v in data:
                list_item = nodes.list_item()
                list_item += self.data(v)
                node += list_item
            return node
        if isinstance(data, dict):
            node = nodes.field_list(classes=["kaitai"])
            for id, val in data.items():
                field = nodes.field()
                field += nodes.field_name(text=str(id))
                var_body = nodes.field_body()
                var_body += self.data(val)
                field += var_body
                node += field
            return node
        if isinstance(data, str) or isinstance(data, int) or isinstance(data, float):
            return nodes.literal(text=str(data))
        else:
            return nodes.literal(text=f"{type(data)} {data}")
    
    def field(self, data: dict):
        _if = data.pop("if", None)
        repeat = data.pop("repeat", None)
        repeat_expr = data.pop("repeat-expr", None)
        if data.keys() == set(["id", "type"]) and isinstance(data["type"], str):
            id = data["id"]
            ty = data["type"]
            block = nodes.paragraph()
            block += nodes.strong(text = f"[{ty}] ")
            block += nodes.emphasis(text = id)
        elif data.keys() == set(["id", "type", "enum"]):
            id = data["id"]
            ty = data["type"]
            enum = data["enum"]
            block = nodes.paragraph()
            block += nodes.strong(text = f"[{ty}:{enum}] ")
            block += nodes.emphasis(text = id)
        elif data.keys() == set(["id", "contents"]):
            id = data["id"]
            contents = data["contents"]
            block = nodes.paragraph()
            if isinstance(contents, str):
                block += nodes.literal(text = f"\"{contents}\"")
            else:
                block += nodes.literal(text = contents)
            block += nodes.emphasis(text = f" {id}")
        else:
            block = self.data(data)
        if _if != None or repeat_expr != None or repeat != None:
            lines = nodes.line_block()
            if _if != None:
                if_line = nodes.line()
                if_line += nodes.strong(text = "if: ")
                if_line += nodes.literal(text = str(_if))
                lines += if_line
            line2 = nodes.line()
            line2 += block
            lines += line2
            if repeat == 'expr':
                rep_line = nodes.line()
                rep_line += nodes.strong(text = "repeat-expr: ")
                rep_line += nodes.literal(text = str(repeat_expr))
                lines += rep_line
            elif repeat != None:
                rep_line = nodes.line()
                rep_line += nodes.strong(text = "repeat: ")
                rep_line += nodes.literal(text = str(repeat))
                lines += rep_line
            return lines
        return block

    def seq(self, data, id):
        section = nodes.section(ids=f"{id}-seq")
        section += nodes.title(text="Sequence")
        node = nodes.enumerated_list()
        for v in data:
            list_item = nodes.list_item()
            list_item += self.field(v)
            node += list_item
        section += node
        return [section]
    
    def instances(self, data, id):
        instances_id = f"{id}-instances"
        section = nodes.section(ids=[instances_id])
        section += nodes.title(text="Instances")
        for key, value in data.items():
            instance_id = f"{instances_id}-{key}"
            subsec = nodes.section(ids=[instance_id])
            title_node = nodes.title()
            title_node += nodes.generated(text="Instance ")
            title_node += nodes.literal(text=key)
            subsec += title_node
            subsec += self.data(value)
            section += subsec
        return [section]

    def enums(self, data, id):
        enums_id = f"{id}-enums"
        enums_section = nodes.section(ids=[enums_id])
        enums_section += nodes.title(text = "Enums")
        for key, value in data.items():
            enum_section = nodes.section(ids=[f"{enums_id}-{key}"])
            enum_title = nodes.title()
            enum_title += nodes.generated(text="Enum ")
            enum_title += nodes.literal(text=key)
            enum_section += enum_title
            list = nodes.field_list()
            for id, val in value.items():
                field = nodes.field()
                field += nodes.field_name(text=str(id))
                var_body = nodes.field_body()
                var_body += nodes.literal(text=str(val))
                field += var_body
                list += field
            enum_section += list
            enums_section += enum_section
        return enums_section
    
    def types(self, data, id):
        id = f"{id}-types"
        section = nodes.section(ids=[id])
        section += nodes.title(text = "Types")
        for key, value in data.items():
            type_id = f"{id}-{key}"
            type_section = nodes.section(ids=[type_id])
            type_title = nodes.title()
            type_title += nodes.generated(text="Type ")
            type_title += nodes.literal(text=key)
            type_section += type_title
            for id, val in value.items():
                if id == 'seq':
                    type_section.extend(self.seq(val, type_id))
                elif id == 'instances':
                    type_section.extend(self.instances(val, type_id))
                else:
                    sec = nodes.section(ids = [f"{type_id}-{id}"])
                    sec += nodes.title(text = id)
                    sec += self.data(val)
                    type_section += sec
            section += type_section
        return section

    def run(self):
        try:
            file = directives.path(self.arguments[0])
            doc = self.state_machine.document
            src = doc.current_source
            dir = os.path.dirname(src)
            path = os.path.normpath(os.path.join(dir, file))
            
            with open(path, 'r') as ksy_file:
                data = yaml.safe_load(ksy_file)
                id = data['meta']['id']
                section = nodes.section(ids=[id])
                section += nodes.title(text=f"Binary Format")
                for key, value in data.items():
                    if key == 'enums':
                        section += self.enums(value, id)
                    elif key == 'types':
                        section += self.types(value, id)
                    elif key == 'seq':
                        section += self.seq(value, id)
                    else:
                        sec = nodes.section(ids = [f"{id}-{key}"])
                        sec += nodes.title(text = key)
                        sec += self.data(value)
                        section += sec
                return [section]
        except Exception as e:
            return [nodes.paragraph(text=str(e))]