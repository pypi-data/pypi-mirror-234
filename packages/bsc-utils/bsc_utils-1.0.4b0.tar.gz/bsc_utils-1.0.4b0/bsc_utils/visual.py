import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from bsc_utils.helpers import row_ratio


def plotly(
    subplots: dict,
    shared_xaxis: bool = True,
    fill_gap: bool = True,
    **layout_kwargs
) -> go.Figure:

    no_subplots = len(subplots)

    fig = make_subplots(
        rows=no_subplots,
        cols=1,
        shared_xaxes=shared_xaxis,
        row_heights=row_ratio(no_subplots),
        vertical_spacing=0.25 / no_subplots,
        subplot_titles=list(subplots.keys()),
        specs=[[{
            'secondary_y': True
        }] for _ in subplots]
    )

    for row_id, subplot in enumerate(subplots.values()):
        for trace in subplot:
            fig.add_trace(
                {
                    k: v
                    for k, v in trace.items()
                    if k not in ['secondary_y', 'range', 'showticklabels']
                },
                secondary_y=trace.get('secondary_y', False),
                row=(row_id + 1),
                col=1,
            )

            if not trace.get('secondary_y'):
                fig['layout'][f'yaxis{row_id * 2 + 1}'].update(
                    range=trace.get('range'), side='right'
                )
            else:
                fig['layout'][f'yaxis{row_id * 2 + 2}'].update(
                    range=trace.get('range'),
                    showticklabels=trace.get('showticklabels'),
                    side='right'
                )

    fig.update_traces(
        xaxis=f'x{no_subplots}',
        xhoverformat='%a %d %b %Y',
    )
    fig.update_xaxes(
        showgrid=False,
        showline=True,
        automargin=True,
        showspikes=True,
        spikemode='across+toaxis',
        spikesnap='cursor',
        spikethickness=1,
        spikedash='solid',
    )
    fig.update_yaxes(
        showgrid=False,
        showline=False,
        automargin=True,
    )
    fig.update_layout(
        showlegend=True,
        autosize=True,
        font_family='Rockwell',
        hovermode='x unified',
        **layout_kwargs
    )
    if shared_xaxis and fill_gap:
        shared_x = trace.get('x')
        if shared_x.dtype.kind == 'M':  # datetime type
            avb_days = [d.to_pydatetime() for d in shared_x]
            all_days = [
                d.to_pydatetime() for d in pd.date_range(
                    start=avb_days[0], end=avb_days[-1], freq=shared_x.freq
                )
            ]
            non_avb_days = [d for d in all_days if d not in avb_days]
            fig.update_xaxes(rangebreaks=[dict(values=non_avb_days)])

    return fig