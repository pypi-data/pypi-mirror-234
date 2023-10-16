from __future__ import annotations

import argparse
import json
import pathlib
import re

import bibtexparser  # type: ignore

from texcliques import color


def extract_references_from_bib(bib: str) -> list[dict[str, str]]:
    with open(bib, 'r', encoding='utf-8') as f:
        bib_database = bibtexparser.load(f)
    return bib_database.entries


def extract_references_from_tex(
    tex: str,
    section_title: str | None,
    id_pattern: re.Pattern
) -> set[str]:
    """Extract references from a LaTeX file."""
    with open(tex, 'r', encoding='utf-8') as f:
        content = f.read()

    if section_title is not None:
        # Assuming the section is clearly demarcated
        # \section{<Passed section>}
        # [...]
        # \section{Another section}
        section = re.search(
            fr'\\section{{{section_title}}}(.*?)\\section',
            content, flags=re.I | re.DOTALL | re.M
        )

        if section:
            section_content = section.group(1)
            refs = re.findall(id_pattern, section_content)
    else:
        refs = re.findall(id_pattern, content)

    if refs:
        refs_split = [ref.split(',') for ref in refs]
        refs_unique = set([ref for refs in refs_split for ref in refs])
        return refs_unique
    else:
        return set()


def clean_bibtex_fields(
    bib_ref: dict[str, str],
    fields: list[str]
) -> dict[str, str]:
    """Remove unnecessary characters from BibTeX fields."""
    cleaned_fields = {}
    for field in fields:
        if field in bib_ref:
            cleaned_field = bib_ref[field]
            cleaned_field = re.sub(r'\\.', '', cleaned_field)
            cleaned_field = re.sub(r'[{}]', '', cleaned_field)
            cleaned_field = re.sub(r'\s+', ' ', cleaned_field)
            cleaned_fields[field] = cleaned_field
    return cleaned_fields


def save_output(
    all_refs: list[dict[str, str]],
    output: str,
    formats: list[str],
    fields: list[str]
) -> None:
    for format in formats:
        if format == 'toml':
            with open(f'{output}.toml', 'a', encoding='utf-8') as toml:
                for bib_ref in all_refs:
                    cleaned_fields = clean_bibtex_fields(bib_ref, fields)
                    toml.write(f'[{bib_ref["ID"]}]\n')
                    for field in cleaned_fields:
                        toml.write(f'{field} = "{cleaned_fields[field]}"\n')
                    toml.write("\n")
        elif format in ('yaml', 'yml'):
            with open(f'{output}.{format}', 'a', encoding='utf-8') as yaml:
                for bib_ref in all_refs:
                    cleaned_fields = clean_bibtex_fields(bib_ref, fields)
                    yaml.write(f'{bib_ref["ID"]}:\n')
                    for field in cleaned_fields:
                        yaml.write(f'  {field}: "{cleaned_fields[field]}"\n')
                    yaml.write('\n')
        elif format == 'json':
            with open(f'{output}.json', 'w', encoding='utf-8') as json_file:
                cleaned_refs = []
                for bib_ref in all_refs:
                    cleaned_fields = clean_bibtex_fields(bib_ref, fields)
                    cleaned_refs.append(cleaned_fields)
                json.dump(cleaned_refs, json_file, indent=4, ensure_ascii=False)


def extract_refs(args: argparse.Namespace) -> int:

    file = args.file
    section_title = args.section
    pattern = re.compile(args.pattern)
    bib = args.bib
    sort = args.sort
    output = args.output
    fields = args.fields
    formats = args.formats

    for arg in (file, bib):
        if not pathlib.Path(arg).exists() or not pathlib.Path(arg).is_file():
            print(f"'{arg}' does not exist (or is not a file).")
            return 1

    if not pathlib.Path(file).suffix == '.tex':
        print(f"'{file}' is not a LaTeX file.")
        return 1

    if not pathlib.Path(bib).suffix == '.bib':
        print(f"'{bib}' is not a BibTeX file.")
        return 1

    refs = extract_references_from_tex(file, section_title, pattern)

    if refs:
        suffix = 's' if len(refs) > 1 else ''
        ending = f'in {section_title}' if section_title else f'in {file}'
        msg = f"Found {len(refs)} reference{suffix} {ending}"
        color.step("Done", start=msg, color='green')

        all_refs = []
        bib_refs = extract_references_from_bib(bib)

        # natural sort
        if sort:
            bib_refs = sorted(
                bib_refs, key=lambda x: [int(c) if c.isdigit() else c
                                         for c in re.split(r'(\d+)', x['ID'])]
            )

        for bib_ref in bib_refs:
            if bib_ref['ID'] in refs:
                all_refs.append(bib_ref)

        save_output(all_refs, output, formats, fields)

        return 0

    else:
        color.step('ERR', start="Could not find any references", color='red')
        return 1
