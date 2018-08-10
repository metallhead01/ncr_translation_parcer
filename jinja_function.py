from jinja2 import Environment, PackageLoader, select_autoescape


def write_xml(data: dict):
    env = Environment(loader=PackageLoader('redis_method', 'Templates'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.xml')
    output_from_parsed_template = template.render(values=data)
    with open('output.xml', "wb+") as fh:
        fh.write(output_from_parsed_template.encode('utf-8'))
