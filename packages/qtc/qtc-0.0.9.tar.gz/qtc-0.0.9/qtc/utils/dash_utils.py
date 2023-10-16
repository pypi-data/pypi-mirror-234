import qtc.utils.misc_utils as mu
import plotly.graph_objs as go

####################################################################
# !!! It would be better that all "styles" be specified in style.css
#     instead of in this python module
####################################################################

DEFAULT_DASH_TABLE_STYLES = None
def get_dash_table_styles(apply_defaults=True,
                          bold_cols=None):
    """
    >>> import qtc.utils.dash_utils as dashu
    """
    global DEFAULT_DASH_TABLE_STYLES
    if apply_defaults:
        if DEFAULT_DASH_TABLE_STYLES is None:
            style_data_conditional = [{
                'if': {'row_index': 'odd'},
                # 'backgroundColor': 'rgb(220, 220, 220)',
                'backgroundColor': '#D9E1F2',
            }]

            DEFAULT_DASH_TABLE_STYLES = dict(
                css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                style_header={
                    'textAlign': 'center',
                    'fontWeight': 'bold',
                    # 'backgroundColor': '#0047AB',
                    'backgroundColor': '#305496',
                    'color': 'white'
                },
                style_data_conditional=style_data_conditional,
                style_cell={'padding': '8px', 'font-family': 'sans-serif', 'font-size': '12px', 'whiteSpace': 'pre-line'}, # 'Monaco'
                fill_width=False
            )

        dash_table_styles = DEFAULT_DASH_TABLE_STYLES
    else:
        dash_table_styles = dict()

    if bold_cols is not None:
        bold_cols = set(mu.iterable_to_tuple(bold_cols, raw_type='str'))
        style_data_conditional = dash_table_styles.get('style_data_conditional', list())
        style_data_conditional += [{'if': {'column_id': bold_col}, 'fontWeight': 'bold'} for bold_col in bold_cols]
        dash_table_styles['style_data_conditional'] = style_data_conditional

    return dash_table_styles


def set_dash_table_new_line(col_fmts, cols_with_new_line):
    new_fmt_items = list()
    for col in cols_with_new_line:
        col_name = col.replace(' ', '\n')
        found = False
        for col_fmt in col_fmts:
            id_value = col_fmt.get('id', None)
            if id_value is not None and id_value == col:
                col_fmt['name'] = col_name
                found = True

        if not found:
            new_fmt_items.append([{'id': col, 'name': col_name}])

    col_fmts.extend(new_fmt_items)

    return col_fmts



DEFAULT_TAB_STYLES = None
def get_default_tab_style():
    global DEFAULT_TAB_STYLES
    if DEFAULT_TAB_STYLES is None:
        DEFAULT_TAB_STYLES = {
            # 'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            # 'fontWeight': 'bold',
            'backgroundColor': '#305496',
            'color': 'white',
        }
    return DEFAULT_TAB_STYLES


DEFAULT_TAB_SELECTED_STYLES = None
def get_default_tab_selected_style():
    global DEFAULT_TAB_SELECTED_STYLES
    if DEFAULT_TAB_SELECTED_STYLES is None:
        DEFAULT_TAB_SELECTED_STYLES = {
            # 'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            # 'fontWeight': 'bold',
            'backgroundColor': 'white',
            'color': 'black',
        }
    return DEFAULT_TAB_SELECTED_STYLES


DEFAULT_LEGEND_STYLES = None
def get_default_legend_styles():
    global DEFAULT_LEGEND_STYLES
    if DEFAULT_LEGEND_STYLES is None:
        DEFAULT_LEGEND_STYLES = {
            'orientation': 'h',
            'title': None,
            'x': 1, 'xanchor': 'right',
            'y': 1, 'yanchor': 'bottom'}
    return DEFAULT_LEGEND_STYLES


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig
