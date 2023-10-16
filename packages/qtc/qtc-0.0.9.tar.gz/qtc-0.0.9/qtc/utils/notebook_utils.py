"""
This module contains some tools to create cleaner report-like output in python notebooks
"""

import base64, io
import matplotlib.pyplot as plt
import nbformat
from IPython.core.display import HTML, Markdown, display, Javascript
from bs4 import BeautifulSoup
from jinja2 import Template
from matplotlib.axes._subplots import SubplotBase
from nbconvert import HTMLExporter, PDFExporter
from nbconvert.preprocessors import ExecutePreprocessor, TagRemovePreprocessor
from qtc.utils.misc_utils import get_zero_centered_min_max
import pandas as pd
import seaborn as sns
sns.set()


def fig_to_base64(fig: SubplotBase):
    """
    Encodes figures for placing directly into html
    :param fig: figure to be encoded
    :return: base64 encoded plot
    """
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue())


def output_grid(*functions, nrows=1, ncols=1, byrow=True):
    """
    Input any number of functions (() ->  obj) that resolve to an object
    which either has _repr_html_ or are a matplotlib SubPlotBase and generate
    a grid display of the results in html.
    :param functions: Any number of () -> obj functions
    :param nrows: number of rows in the grid
    :param ncols: number of columns in the grid
    :param byrow: functions should be taken in row major order (fill row1, then row2, etc).
                  False is column majore order.  Rows are filled left to right fro the top,
                  Columns are filled top to bottom from the left
    :return: html
    """
    # Get the html outputs
    html_outputs = []
    for function in functions:
        obj = function() if callable(function) else function
        if isinstance(obj, SubplotBase):
            fig = obj.get_figure()
            encoded = fig_to_base64(fig)
            plt.close(fig)
            html_outputs.append('<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8')))
        elif hasattr(obj, '_repr_html_') and callable(obj._repr_html_):
            html_outputs.append(obj._repr_html_())
        elif isinstance(obj, Markdown):
            html_outputs.append(obj)
        else:
            html_outputs.append('')

    # Add the grid to the flexbox template
    template = Template('''
    <div style="display:inline-grid;grid-gap:10px 10px;grid-auto-flow: {{ 'row' if byrow else 'column' }};grid-template-rows: repeat({{nrows}}, min-content);grid-template-columns: repeat({{ncols}}, max-content);">
        {% for item in html_outputs %}
            <div style="flex: 1 1 auto;">
                {{ item }}
            </div>
        {% endfor %}
    </div>
    ''')

    # Return the html output
    return HTML(template.render(html_outputs=html_outputs, nrows=nrows, ncols=ncols, byrow=byrow))


def clean_html(notebook_as_html):
    soup = BeautifulSoup(notebook_as_html, 'html.parser')

    # removes code input blocks
    for inp in soup.find_all('div', {'class': 'input'}):
        inp.decompose()

    # removes line number container
    for inp in soup.find_all('div', {'class': 'prompt'}):
        inp.decompose()

    # removes line number output
    for inp in soup.find_all('div', {'class': 'prompt output_prompt'}):
        inp.decompose()

    # removes show/hide code toggle
    for inp in soup.find_all('input', {'type': 'submit'}):
        inp.decompose()

    # removes box shadow for better printing
    for inp in soup.find_all('div', {'id': 'notebook-container'}):
        inp['style'] = 'box shadow: none; -webkit-box-shadow: none;'

    # prevents scroll bars
    for inp in soup.find_all('div', {'class': 'output_html rendered_html output_subarea'}):
        inp['style'] = 'overflow-x: visible;'

    for inp in soup.find_all('div', {'class': 'output_html rendered_html output_subarea output_execute_result'}):
        inp['style'] = 'overflow-x: visible;'

    return str(soup)


def export_notebook_to_html(nb, notebook_filename_out, clean_notebook=True, template=None):
    if isinstance(nb, str):
        nb = _read_in_notebook(notebook_fp=nb)
    html_exporter = HTMLExporter(template_file=template) if template else HTMLExporter()
    body, resources = html_exporter.from_notebook_node(nb)
    out_fp = notebook_filename_out.replace(".ipynb", ".html")
    html_final = clean_html(body) if clean_notebook else body
    with open(out_fp, "w", encoding="utf8") as f:
        f.write(html_final)


def export_notebook_to_pdf(nb, notebook_filename_out):
    pdf_exporter = PDFExporter()
    pdf_data, resources = pdf_exporter.from_notebook_node(nb)
    out_fp = notebook_filename_out.replace(".ipynb", ".pdf")
    with open(out_fp, "wb") as f:
        f.write(pdf_data)


def _read_in_notebook(notebook_fp):
    with open(notebook_fp) as f:
        nb = nbformat.read(f, as_version=4)
    return nb


# def _add_notebook_title(nb):
#     parameters = nbparameterise.extract_parameters(nb)
#     for p in parameters:
#         if p.name == 'notebook_title':
#             nb.metadata.title = p.value
#             return
#     # default
#     nb.metadata.title = 'NoteBook'
# #


# def execute_notebook(notebook_path,
#                      notebook_path_out,
#                      params_dict,
#                      run_path='',
#                      timeout=600,
#                      export_html=True,
#                      remove_cell_tags=['remove_cell'],
#                      template=None):
#     nb = _read_in_notebook(notebook_path)
#     new_nb = _set_parameters(nb, params_dict)
#     ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
#     tr = TagRemovePreprocessor()
#     tr.remove_cell_tags = remove_cell_tags
#
#     ep.preprocess(new_nb, {'metadata': {'path': run_path}})
#     new_nb, r = tr.preprocess(new_nb, {})
#     with open(notebook_path_out, mode='wt') as f:
#         nbformat.write(new_nb, f)
#     if export_html:
#         export_notebook_to_html(new_nb,
#                                 notebook_path_out,
#                                 clean_notebook=True,
#                                 template=template)
#     return new_nb
# #


def hide_toggle(for_next=False):
    import random

    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'

    toggle_text = 'Toggle show/hide'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    js_hide_current = ''  # bit of JS to permanently hide code in current cell (only when toggling next cell)

    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'

    js_f_name = 'code_toggle_{}'.format(str(random.randint(1,2**64)))

    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            $( document ).ready(function(){{
                code_shown=false;
                $('div.input').hide()
            }});

            {js_hide_current}
        </script>

        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current,
        toggle_text=toggle_text
    )

    return HTML(html)


def set_width_global(width=100):
    display(HTML(f"<style>.container {{ width:{width}% !important; }}</style>"))


def disable_auto_scroll():
    display(Javascript('''
        IPython.OutputArea.prototype._should_scroll = function(lines) {
            return false;
        }'''))


def create_download_link(df, filename, title='Download CSV file', index=True):
    csv = df.to_csv(index=index)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = f'<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    return HTML(html)


GR_PAL = sns.diverging_palette(12, 150, s=80, l=60, n=256, as_cmap=False)
GR_CM = sns.diverging_palette(12, 150, s=80, l=60, as_cmap=True)


def create_heatmap(data, row_summary=None, col_summary=None,
                   title=None,
                   fontsize=10, float_format='.0f', figsize=(20, 10),
                   xlabel=None, ylabel=None):
    min_val, max_val = get_zero_centered_min_max(data)

    fig = plt.figure(figsize=figsize)

    ax1 = plt.subplot2grid(figsize, (0, 0), fig=fig, colspan=figsize[1]-1, rowspan=figsize[0]-1)
    ax1.xaxis.tick_top()
    sns.heatmap(data, ax=ax1,
                fmt=float_format, annot=True, annot_kws={'fontsize': fontsize},
                cmap=GR_CM, cbar=False, vmin=min_val, vmax=max_val)
    if not xlabel:
        ax1.set_xlabel('')
    if not ylabel:
        ax1.set_ylabel('')

    if title is not None:
        ax1.set_title(title)

    if col_summary is not None:
        ax2 = plt.subplot2grid(figsize, (figsize[0] - 1, 0), fig=fig, colspan=figsize[1] - 1, rowspan=1)
        if isinstance(col_summary, str):
            if col_summary.lower()=='sum':
                col_stats = pd.DataFrame(data.sum(axis=0)).T
            elif col_summary.lower()=='mean':
                col_stats = pd.DataFrame(data.mean(axis=0)).T
            else:
                raise Exception(f"col_summary={col_summary} is not supported in [sum|mean]")
        else:
            col_stats = pd.DataFrame(col_summary(data)).T

        min_val, max_val = get_zero_centered_min_max(col_stats)
        sns.heatmap(col_stats, ax=ax2,
                    fmt=float_format, annot=True, annot_kws={'fontsize': fontsize},
                    cmap=GR_CM, cbar=False, vmin=min_val, vmax=max_val, xticklabels=False, yticklabels=False)
        if not xlabel:
            ax2.set_xlabel('')
        if not ylabel:
            ax2.set_ylabel('')

    if row_summary is not None:
        ax3 = plt.subplot2grid(figsize, (0, figsize[1] - 1), fig=fig, colspan=1, rowspan=figsize[0] - 1)
        if isinstance(row_summary, str):
            if row_summary.lower()=='sum':
                row_stats = pd.DataFrame(data.sum(axis=1))
            elif row_summary.lower()=='mean':
                row_stats = pd.DataFrame(data.mean(axis=1))
            else:
                raise Exception(f"row_summary={row_summary} is not supported in [sum|mean]")
        else:
            row_stats = pd.DataFrame(row_summary(data))

        min_val, max_val = get_zero_centered_min_max(row_stats)
        sns.heatmap(row_stats.values, ax=ax3,
                    fmt=float_format, annot=True, annot_kws={'fontsize': fontsize},
                    cmap=GR_CM, cbar=False, vmin=min_val, vmax=max_val, xticklabels=False, yticklabels=False)
        if not xlabel:
            ax3.set_xlabel('')
        if not ylabel:
            ax3.set_ylabel('')

    return ax1
