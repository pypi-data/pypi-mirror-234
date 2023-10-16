import io
import base64


def fig_to_base64(fig=None):
    import matplotlib.pyplot as plt
    if fig is None:
        fig = plt.gcf()

    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())


def get_default_styles():
    th_col_heading_props = [
        ('text-align', 'center'),
        ('background-color', '#F5F5F5'),
        ('border-collapse', 'collapse'),
        ('border', '1px black solid'),
        ('padding', '5px')
    ]

    th_props = [
        ('text-align', 'center'),
        ('font-size', '12px'),
        ('font-family', 'Arial'),
        # ('background-color', 'white'),
        ('border-collapse', 'collapse'),
        ('border', '1px black solid'),
        ('padding', '5px')
    ]

    td_props = [
        ('text-align', 'right'),
        ('font-size', '12px'),
        ('font-family', 'Arial'),
        ('border-collapse', 'collapse'),
        ('border', '1px black solid'),
        ('padding-left', '5px'),
        ('padding-right', '5px'),
        ('padding-top', '2px'),
        ('padding-bottom', '2px'),
    ]

    styles = [
        dict(selector='th.col_heading', props=th_col_heading_props),
        dict(selector='th', props=th_props),
        dict(selector='td', props=td_props),
        dict(selector='tr:nth-child(even)', props=[('background-color', '#F5F5F5')]),
    ]

    return styles


def html_from_styler(styler, styles=None, title=''):
    if styles is None:
        styles = get_default_styles()

    table_html = styler.set_table_styles(styles)\
                       .set_table_attributes('style="border-collapse:collapse; border:1px black solid"')\
                       .render()

    html = f'<h5>{title}</h5>\n{table_html}' if len(title) else table_html

    return html


def html_from_array(tables, title='', footer=''):
    if len(title):
        title = f'''<h4>{title}</h4>\n'''

    if len(footer):
        footer = f'''<p><i>{footer}</i>'''

    tables = '\n'.join(tables)
    html = f'''
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="..\limitstyle.css">
            </head>
            <body>
                {title}
                {tables}
                {footer}
            </body>
        </html>
    '''

    return html


def create_td_style_border_text(row_borders, col_borders, border_width='1.0pt'):
    if (row_borders == 'None') & (col_borders == 'None'):
        border_text = ''
    else:
        border_text = f'border:solid windowtext {border_width};'
        if row_borders == 'None':
            border_text = border_text + 'border-top:none;border-bottom:none;'
        elif row_borders == 'Top':
            border_text = border_text + 'border-bottom:none;'
        elif row_borders == 'Bottom':
            border_text = border_text + 'border-top:none;'
        if col_borders == 'None':
            border_text = border_text + 'border-left:none;border-right:none;'
        elif col_borders == 'Left':
            border_text = border_text + 'border-rightnone;'
        elif col_borders == 'Right':
            border_text = border_text + 'border-left:none;'

    return border_text


def create_td_element(width, row_borders, col_borders, data_value=None, height=None, width_pt=None,
                      border_width='1.0pt',
                      align=None, valign=None, nowrap=False, bold_font=False, font_color=None, background=None,
                      colspan=None):
    td_str = f'''<td width={width}'''
    if nowrap:
        td_str = td_str + ' nowrap'
    if valign is not None:
        td_str = td_str + f''' valign={valign}'''
    if colspan is not None:
        td_str = td_str + f''' colspan={colspan}'''

    td_style_str = ''
    if width_pt is not None:
        td_style_str = f'width:{width_pt};'
    td_style_str = td_style_str + create_td_style_border_text(row_borders, col_borders, border_width)
    if background is not None:
        td_style_str = td_style_str + f'''background:{background};'''
    td_style_str = td_style_str + 'padding:0in 5.4pt 0in 5.4pt;'
    if height is not None:
        td_style_str = td_style_str + f'''height:{height};'''
    if len(td_style_str) > 0:
        td_style_str = f" style='{td_style_str}'"

    td_str = td_str + td_style_str + '>'
    if data_value is not None:
        td_str = td_str + '<p class=MsoNormal'
        if align == 'Center':
            td_str = td_str + " style='text-align:center'"
        td_str = td_str + ">"
        if bold_font:
            td_str = td_str + "<b>"
        close_span = False
        if font_color is not None:
            td_str = td_str + f"<span style='color:{font_color}'>"
            close_span = True
        td_str = td_str + str(data_value)
        if close_span:
            td_str = td_str + "</span>"
        # td_str = td_str + "<o:p></o:p>"
        if bold_font:
            td_str = td_str + "</b>"
        td_str = td_str + "</p>"

    td_str = td_str + "</td>"
    return td_str


def format_df_rows(df,
                   formatter,
                   slicer=None):
    df = df.copy()

    if not slicer:
        for col in df.columns:
            df[col] = df[col].apply(formatter.format, axis=0)
        return df
    else:
        dfs = df.loc[slicer].copy()
        for col in dfs.columns:
            dfs[col] = dfs[col].apply(formatter.format, axis=0)
        df.loc[slicer] = dfs
        return df


DEFAULT_UL_BULLET_POINT_CODES = ['&#9632;', '&#9633;', '&#9679;', '&#9900;']

class HTMLListNode:
    def __init__(self, html=''):
        self.html = html
        self.children = list()

    def add_item(self, html):
        node = HTMLListNode(html=html)
        self.children.append(node)
        return node


class HTMLListBuilder:
    def __init__(self,
                 indent_start=0.25, indent_step=0.25,
                 padding=1,
                 ul_bullet_point_codes=DEFAULT_UL_BULLET_POINT_CODES):
        self.root = HTMLListNode()
        self.indent_start = indent_start
        self.indent_step = indent_step
        self.padding = padding
        self.ul_bullet_point_codes = ul_bullet_point_codes

    def _build_html_from_node(self,
                              html_list_node,
                              level=0):
        children = html_list_node.children

        lines = list()
        indent = '\t' * level
        # line = f'{indent}<p class=MsoNormal style="margin-left:{self.indent_start+self.indent_step*level}in;">{html_list_node.html}'
        # lines.append(line)
        for i, child in enumerate(children):
            # indent1 = '\t' * (level+1)
            # line = f'{indent1}<li class="MsoNormal">{child.html}</li>'
            # lines.append(line)
            # number_str = f'({convert_number(number=i+1, level=level)})'
            bullet_point_str = self.ul_bullet_point_codes[level - 1] if level <= len(self.ul_bullet_point_codes) else ''
            p_class = 'MsoListParagraph' if level == 1 else 'MsoNormal'
            line = f'{indent}<p class={p_class} style="margin-left:{self.indent_start + self.indent_step * level}in;">{bullet_point_str}&emsp;{child.html}</p>'
            lines.append(line)

            nested_lines = self._build_html_from_node(html_list_node=child,
                                                      level=level + 1)
            lines.extend(nested_lines)

        return lines

    def build_html_list(self):
        lines = self._build_html_from_node(html_list_node=self.root,
                                           level=1)
        return '\n'.join(lines)
