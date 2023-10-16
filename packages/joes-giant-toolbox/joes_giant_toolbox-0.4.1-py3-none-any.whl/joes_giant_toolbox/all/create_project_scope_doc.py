import os
from typing import List


def create_project_scope_doc() -> None:
    """Creates a basic project scope document (markdown) by prompting the user for input

    Example Usage
    -------------
    >>> create_project_scope_doc()
    """

    SECTION_DESC = {
        "Project Name": "Provide a name for your project.",
        "State the Problem": "A simple statement of the problem that you are trying to solve (the PROBLEM, not the solution).",
        "Wny Bother?": "A summary of why the problem is important, and why we care about solving it.",
        "Current Solutions and Why They Fail": "",
        "What Would a Solution Look Like?": "This is not a description of an actual solution, but rather the list of attributes that we expect any successful solution to this problem to have.",
        "How Do I Know If I've Solved It?": "How will a completed solution be evaluated/measured? What specific objective measure would convince all relevant stakeholders that the solution is successful?",
        "What are the Uncertainties?": "What must be true for the solution to work? What must not be true in order for the solution to work?",
        "Sketch of a Plan": 'A high level "roadmap" of the next steps',
        "Export Scope to Markdown": 'Provide an output filename for the markdown document e.g. "project_scope.md" (it is written to the directory in which this script is being run)',
    }

    build_md_text_entries = {k: "" for k in SECTION_DESC}

    def preview_string(raw_str: str | None, max_chars: int) -> str:
        """Truncate a string if it is more than a certain length and/or contains newlines"""
        if raw_str is None:
            return ""
        concat_dots = ""
        if "\n" in raw_str:
            raw_str = raw_str.split("\n")[0]
            concat_dots = "..."
        if len(raw_str) > max_chars:
            concat_dots = "..."
            return f"{raw_str[:max_chars]}{concat_dots}"
        else:
            return f"{raw_str}{concat_dots}"

    def get_multiline_input() -> List[str]:
        """Function for receiving (potentially) multi-line text input from the user"""
        lines = []
        while True:
            line = input(">>> ")
            if line:
                lines.append(line)
            else:
                break

        if len(lines) == 0:
            return None
        else:
            return "\n".join(lines)

    def print_current_stage(current_section_name) -> None:
        """Prints information to the screen about the current state of the process"""
        os.system("cls||clear")
        stage_text = """
    +---------------------------------+
    | Creating Project Scope Document |
    +---------------------------------+
    """
        stage_text += "Original methodology by Marco Tulio Ribiero\n\n"
        for print_section_name in SECTION_DESC:
            if current_section_name == print_section_name:
                stage_text += f"* {print_section_name:<50} {preview_string(build_md_text_entries[print_section_name],50)}\n"
            else:
                stage_text += f"  {print_section_name:<50} {preview_string(build_md_text_entries[print_section_name],50)}\n"
        stage_text += f"\n[{current_section_name}]\n"
        stage_text += f"{SECTION_DESC[current_section_name]}\n"
        print(stage_text)

    for section_name in SECTION_DESC:
        print_current_stage(section_name)
        build_md_text_entries[section_name] = get_multiline_input()

    build_md_string = ""
    for section_name in SECTION_DESC:
        if section_name == "Project Name":
            build_md_string += (
                f"# Project Scope: {build_md_text_entries[section_name]}\n\n"
            )
        elif section_name == "Export Scope to Markdown":
            pass
        else:
            build_md_string += f"## {section_name}\n\n"
            if build_md_text_entries[section_name] is None:
                build_md_text_entries[section_name] = "!! user input not provided !!"
            build_md_string += f"{build_md_text_entries[section_name]}\n\n"

    output_filepath = os.path.join(
        os.getcwd(), build_md_text_entries["Export Scope to Markdown"]
    )
    with open(output_filepath, "w") as f:
        f.write(build_md_string)
    print(f"!!! saved output to: {output_filepath} !!!")
