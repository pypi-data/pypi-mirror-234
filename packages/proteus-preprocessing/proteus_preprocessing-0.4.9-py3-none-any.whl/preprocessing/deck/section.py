import os
import re


def get_includes(input_data_file_loc, download_func, allow_missing_files=tuple()):
    assert input_data_file_loc.upper().endswith(".DATA")
    return find_includes(
        input_data_file_loc, download_func, input_data_file_loc, allow_missing_files=allow_missing_files
    )


def find_section(input_data_file_loc, section_header, download_func, allow_missing_files=tuple()):
    file_list = [input_data_file_loc] + get_includes(
        input_data_file_loc, download_func, allow_missing_files=allow_missing_files
    )

    for file_loc in file_list:
        with open(file_loc, "r") as f:
            section = scan_file(f.read(), section_header)
            if section is not None:
                return section.group("content")


def parse_dependency_path(file_absolute_path, dependency):
    return os.path.abspath(os.path.join(os.path.dirname(file_absolute_path), dependency))


def find_includes(input_file_loc, download_func, base_data_file_path=None, allow_missing_files=tuple()):
    with open(input_file_loc, "r") as data_file:
        content = data_file.read()

    include_expression_re = re.compile(r"\s*INCLUDE[^\'\/]+'(?P<path>[^']+)'")
    inc_found = include_expression_re.finditer(content)
    includes_list = [inc.groupdict().get("path") for inc in inc_found]

    fixed_includes_list = []
    for include_file_loc in includes_list:

        try:
            download_base_path = (
                os.path.dirname(base_data_file_path)
                if base_data_file_path and not include_file_loc.startswith(".")
                else os.path.dirname(input_file_loc)
            )
            downloaded_path = download_func(include_file_loc, download_base_path)

            if downloaded_path is None:
                raise FileNotFoundError(f'Include file "{include_file_loc}" not found')

            fixed_includes_list.append(downloaded_path)

            fixed_includes_list += find_includes(
                downloaded_path, download_func, base_data_file_path, allow_missing_files=allow_missing_files
            )
        except FileNotFoundError as e:
            not_found_file = include_file_loc

            error_message = (
                f'File "{input_file_loc}" includes subfile '
                f"{include_file_loc}, but the file was not found. Reason: {str(e)}"
            )

            skip = False
            for skipable_file_rel in allow_missing_files:
                skipable_file = os.path.realpath(skipable_file_rel)

                if (
                    skipable_file == not_found_file
                    or not skipable_file_rel.startswith(os.path.sep)
                    and not_found_file.endswith(skipable_file_rel)
                ):
                    skip = True
                    break

            if skip:
                print(f"\n{error_message}. skipping because it was explicitly whitelisted.")
                continue
            else:
                raise FileNotFoundError(error_message)

    return fixed_includes_list


def scan_file(content, section_header):
    section_expression_re = re.compile(
        section_header + r"\s+=*(?P<content>[\S\s]*?)(RUNSPEC|GRID|PROPS|REGIONS|SOLUTIONS|SUMMARY|SCHEDULE)\s"
    )
    section_found = section_expression_re.finditer(content)

    section_content = next(section_found)
    if section_content is not None:
        return section_content
