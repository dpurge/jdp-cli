from pathlib import Path
from genanki import Deck, Package, Model, Note, guid_for
from jinja2 import Template
from markdown import Markdown

from .lib_anki_project import get_anki_project
from .lib_get_anki_data import get_anki_data

def cmd_build_project(config='jdp-apkg.toml', filename=None, directory=None):
    cfg = get_anki_project(config=config)
    md = Markdown()

    if filename:
        cfg.filename = Path(filename).absolute()

    if directory:
        cfg.filename = Path(directory).absolute() / cfg.filename.name

    model_templates = []
    for mtpl in cfg.model.templates:
        with mtpl.qfmt.open(mode='r', encoding='utf-8') as tpl:
            qfmt = tpl.read()

        with mtpl.afmt.open(mode='r', encoding='utf-8') as tpl:
            afmt = tpl.read()

        model_templates.append({
            'name': mtpl.name,
            'qfmt': qfmt,
            'afmt': afmt })
            
    with cfg.model.styles.open(mode='r', encoding='utf-8') as tpl:
        css = tpl.read()

    model = Model(
        model_id = cfg.model.id,
        name = cfg.model.name,
        fields = [{'name': fld.name} for fld in cfg.model.fields],
        templates = model_templates,
        css = css,
        model_type = Model.CLOZE if cfg.model.type == 'cloze' else Model.FRONT_BACK)

    deck = Deck(cfg.deck.id, cfg.deck.name)

    templates = {}
    for fld in cfg.model.fields:
        with fld.template.open(mode="r", encoding="utf-8") as tpl:
            templates[fld.name] = Template(tpl.read())

    for d in cfg.data:
        for data in get_anki_data(d.filename):
            guid = " ".join([data[i] for i in cfg.model.guid])
            fields = []
            for fld in cfg.model.fields:
                if fld.markdown:
                    data[fld.name] = md.convert(data[fld.name])
                    md.reset()
                fields.append(templates[fld.name].render(**data))
            
            note = Note(
                guid = guid_for(guid),
                model = model,
                fields = fields,
                tags = d.tags)

            deck.add_note(note)

    pkg = Package(deck)

    cfg.filename.parent.mkdir(parents=True, exist_ok=True)
    pkg.write_to_file(cfg.filename)
