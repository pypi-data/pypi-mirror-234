import os


def to_readable_case(string):
    new_string = string.replace('_', ' ')
    new_string = new_string.replace('-', ' ')
    new_string = new_string.title()

    return new_string


def to_folder_case(string):
    new_string = to_readable_case(string)
    new_string = new_string.replace(' ', '_')

    return new_string


def to_pascal_case(string):
    new_string = to_readable_case(string)
    new_string = new_string.replace(' ', '')

    return new_string


def sort_font_styles(old_list, start_index):
    new_list = [old_list[start_index]]
    i = 1

    while start_index - i >= 0 or start_index + i < len(old_list):
        if start_index - i >= 0:
            new_list.append(old_list[start_index - i])

        if start_index + i < len(old_list):
            new_list.append(old_list[start_index + i])

        i += 1

    return new_list


def find_style(folder, font_name, style, italic):
    font_name = to_pascal_case(font_name)
    style = to_pascal_case(style)
    regular_styles = [
        'ExtraLight', 'Light', 'Thin', 'Regular', 'Medium',
        'SemiBold', 'Bold', 'ExtraBold', 'Black'
    ]
    italic_styles = [f'{style}Italic' for style in regular_styles]
    style_index = regular_styles.index(style)
    ordered_styles = []

    if italic:
        ordered_styles = sort_font_styles(italic_styles, style_index)

    ordered_styles = [
        *ordered_styles, *sort_font_styles(regular_styles, style_index)
    ]

    for style in ordered_styles:
        name = f'{font_name}-{style}.ttf'
        font_path = os.path.join(folder, name)

        if os.path.exists(font_path):
            return font_path

    return None


def find_font(name, style='Regular', italic=False, root='assets/fonts'):
    name = str(name)
    font_folder = os.path.join(root, to_folder_case(name))

    if os.path.exists(font_folder):
        static_folder = os.path.join(font_folder, 'static')

        if os.path.exists(static_folder):
            return find_style(static_folder, name, style, italic)
        else:
            return find_style(font_folder, name, style, italic)
    else:
        return None
