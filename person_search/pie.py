# -*- mode: python; coding: utf-8 -*-
"""``get_pie()`` returns SVG for a single-parameter pie chart for a given ``percent``  (hardcoced size, color).
"""

def get_pie(percent):
    """returns SVG for a single-parameter pie chart for a given ``percent``  (hardcoced size, color).
    """
    # from https://www.smashingmagazine.com/2015/07/designing-simple-pie-charts-with-css/
    pie = """
    <style>
    svg {
      width: 100px; height: 100px;
      transform: rotate(-90deg);
      background: yellowgreen;
      border-radius: 50%%;
    }
    circle {
      fill: yellowgreen;
      stroke: #655;
      stroke-width: 32;
      stroke-dasharray: %(percent)s 100; /* for 38%% */
    }
    </style>
    <svg viewBox="0 0 32 32">
      <circle r="16" cx="16" cy="16" />
    </svg>
    """
    return pie % {'percent': str(percent)}


if __name__ == '__main__':

    # Simple testing

    # INPROD: I would use ``tempfile`` for this kind of thing in practice.
    path = '/tmp/.pie.html'

    print('Writing to file %s !!' % path)
    open(path, 'w').write(get_pie(33))

    import webbrowser
    webbrowser.open(path, new=0, autoraise=True)
