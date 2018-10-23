# -*- mode: python; coding: utf-8 -*-
"""``get_pie()`` returns SVG for a single-parameter pie chart with slice
``color`` for a given ``percent`` (hardcoded size, color).
"""

def get_pie(percent, color):
    """returns SVG for a single-parameter pie chart with slice ``color`` for a
    given ``percent`` (hardcoded size, color).
    """
    # from
    # https://www.smashingmagazine.com/2015/07/designing-simple-pie-charts-with-css/
    pie = """
    <style>
    svg {
      width: 100px; height: 100px;
      transform: rotate(-90deg);
      background: green;
      border-radius: 50%%;
    }
    circle {
      fill: green;
      stroke: %(color)s;
      stroke-width: 32;
      stroke-dasharray: %(percent)s 100; /* for 38%% */
    }
    </style>
    <svg viewBox="0 0 32 32">
      <circle r="16" cx="16" cy="16" />
    </svg>
    """
    return pie % {
        'percent': str(percent),
        'color': color,
    }


if __name__ == '__main__':

    # Simple testing

    # INPROD: I would use ``tempfile`` for this kind of thing in practice.
    path = '/tmp/.pie.html'

    print('Writing to file %s !!' % path)
    open(path, 'w').write(get_pie(33, 'blue'))

    import webbrowser
    webbrowser.open(path, new=0, autoraise=True)
