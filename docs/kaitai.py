import os
from typing import Any
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
    
    def meta(self, data: dict):
        box = nodes.note()
        node = nodes.field_list(classes=["kaitai"])
        for id, val in data.items():
            field = nodes.field()
            field += nodes.field_name(text=str(id))
            var_body = nodes.field_body()
            var_body += self.data(val)
            field += var_body
            node += field
        box += node
        return [box]

    def field(self, data: dict):
        pos = data.pop("pos", None)
        _if = data.pop("if", None)
        repeat = data.pop("repeat", None)
        repeat_expr = data.pop("repeat-expr", None)
        size = data.pop("size", None)
        encoding = data.pop("encoding", None)
        ty_cases = None
        ty = data.pop("type", None)
        id = data.pop("id", None)
        enum = data.pop("enum", None)
        
        if isinstance(ty, str):
            block = nodes.paragraph()
            if enum != None:
                block += nodes.strong(text = f"[{ty}:{enum}] ")
            else:
                block += nodes.strong(text = f"[{ty}] ")
            if id != None:
                block += nodes.emphasis(text = id)
        elif isinstance(ty, dict):
            switch_on = ty["switch-on"]
            ty_cases = ty["cases"]
            block = nodes.paragraph()
            block += nodes.strong(text = f"[switch-on:{switch_on}] ")
            if id != None:
                block += nodes.emphasis(text = id)
        elif "contents" in data:
            contents = data["contents"]
            block = nodes.paragraph()
            if isinstance(contents, str):
                block += nodes.literal(text = f"'{contents}'")
            else:
                block += nodes.literal(text = contents)
            if id != None:
                block += nodes.emphasis(text = f" {id}")
        else:
            block = None
        lines = nodes.line_block(classes=["kaitai-field"])
        if _if != None:
            if_line = nodes.line()
            if_line += nodes.strong(text = "if: ")
            if_line += nodes.literal(text = str(_if))
            lines += if_line
        if block != None:
            line2 = nodes.line()
            line2 += block
            lines += line2
        if pos != None:
            line = nodes.line()
            line += nodes.strong(text = "Position: ")
            line += nodes.literal(text = str(pos))
            lines += line
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
        if ty_cases != None:
            table = nodes.table()
            tgroup = nodes.tgroup(cols = 2)
            tgroup += nodes.colspec(colwidth=4)
            tgroup += nodes.colspec(colwidth=4)
            tbody = nodes.tbody()
            for val, ty in ty_cases.items():
                row = nodes.row()
                valEntry = nodes.entry()
                valEntry += nodes.strong(text = str(val))
                tyEntry = nodes.entry()
                tyEntry += nodes.literal(text = str(ty))
                row += valEntry
                row += tyEntry
                tbody += row
            tgroup += tbody
            table += nodes.title(text = "Type Cases")
            table += tgroup
            lines += table
        if size != None:
            size_line = nodes.line()
            size_line += nodes.strong(text = "Size: ")
            size_line += nodes.literal(text = str(size))
            lines += size_line
        if encoding != None:
            line = nodes.line()
            line += nodes.strong(text = "Encoding: ")
            line += nodes.literal(text = str(encoding))
            lines += line
        return lines

    def seq(self, data, id):
        section = nodes.section(ids=[f"{id}-seq"])
        section += nodes.title(text="Sequence")
        node = nodes.enumerated_list()
        for v in data:
            list_item = nodes.list_item()
            list_item += self.field(v)
            node += list_item
        section += node
        return [section]
    
    def instance(self, parent_id, key, value):
        instance_id = '-'.join([parent_id, key])
        subsec = nodes.section(ids=[instance_id])
        title_node = nodes.title()
        title_node += nodes.generated(text="Instance ")
        title_node += nodes.literal(text=key)
        subsec += title_node
        subsec += self.field(value)
        return subsec

    def instances(self, data, id):
        instances_id = '-'.join([id, "instances"])
        return [self.instance(instances_id, key, value) for key, value in data.items()]

    def enum_variant(self, id, val):
        field = nodes.field()
        field += nodes.field_name(text=str(id))
        var_body = nodes.field_body()
        if isinstance(val, dict):
            lines = nodes.line_block()
            if "id" in val:
                id_line = nodes.line()
                id_line += nodes.literal(text = str(val["id"]))
                lines += id_line
            if "doc" in val:
                doc_line = nodes.line()
                doc_line += nodes.paragraph(text = val["doc"])
                lines += doc_line
            var_body += lines
        else:
            var_body += nodes.literal(text=str(val))
        field += var_body
        return field

    def enum(self, parent_id, key, value):
        section = nodes.section(ids=[f"{parent_id}-{key}"])
        title = nodes.title()
        title += nodes.generated(text="Enum ")
        title += nodes.literal(text=key)
        section += title
        list = nodes.field_list()
        for id, val in value.items():
            list += self.enum_variant(id, val)
        section += list
        return section
    
    def enums(self, data, id):
        return [self.enum(f"{id}-enums", key, value) for key, value in data.items()]
    
    def type(self, parent_id, key, value):
        type_id = f"{parent_id}-{key}"
        section = nodes.section(ids=[type_id])
        title = nodes.title()
        title += nodes.generated(text="Type ")
        title += nodes.literal(text=key)
        section += title
        for id, val in value.items():
            if id == 'seq':
                section.extend(self.seq(val, type_id))
            elif id == 'instances':
                section.extend(self.instances(val, type_id))
            else:
                sec = nodes.section(ids = [f"{type_id}-{id}"])
                sec += nodes.title(text = id)
                sec += self.data(val)
                section += sec
        return section
            

    def types(self, data: dict[str, Any], id: str):
        return [self.type(f"{id}-types", key, value) for key, value in data.items()]

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
                section = []
                for key, value in data.items():
                    if key == 'enums':
                        section.extend(self.enums(value, id))
                    elif key == 'types':
                        section.extend(self.types(value, id))
                    elif key == 'seq':
                        section += self.seq(value, id)
                    elif key == 'instances':
                        section.extend(self.instances(value, id))
                    elif key == 'meta':
                        section.extend(self.meta(value))
                    else:
                        sec = nodes.section(ids = [f"{id}-{key}"])
                        sec += nodes.title(text = key)
                        sec += self.data(value)
                        section += sec
                return section
        except Exception as e:
            return [nodes.paragraph(text=str(e))]