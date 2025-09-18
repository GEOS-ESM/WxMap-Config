import numpy as np


def float_format(num, precision=10, trim='-'):
    return np.format_float_positional(num, precision=precision, trim=trim)

# -----------------------------------------------------------------------------


def set_clevs(cmin, cmax, cint):
    """
    Sets contour levels based on the specified min/max/increment.

    This method expands the contour levels into a string of values
    based on the range [cmin, cmax]. The values are formatted floats
    using the assigned precision (see float_format method).

    Parameters
    ----------
    cmin : string|float
        Contour minimum value
    cmax: string|float
        Contour maximum value
    cint: string|float
        Contour interval (increment)

    Returns
    -------
    levels : None|string
        None: contour levels were unspecified
        string: list-string of formatted contour levels (space delimited)

    See Also
    --------
    float_format : method
        Reformats floating point numbers into string values

    """

    # Return if contour level specification is incomplete

    if None in (cmin, cmax, cint):
        return

    # Construct a list-string of values over the
    # contour interval [cmin,cmax]

    vmin = float(cmin)
    vmax = float(cmax)
    vint = float(cint)

    cout = []
    for v in np.arange(vmin, vmax+vint/2.0, vint):
        cout.append(float_format(v))
        v += vint

    return ' '.join(cout)

# -----------------------------------------------------------------------------


def refine_clevs(clevs, nsub, type):
    """
    Refines contour levels by sub-dividing each interval into smaller
    intervals.

    This method refines the contour levels into a string of values
    where each interval is sub-divided into equally spaced sub-intervals.

    Parameters
    ----------
    clevs : string|string[]|float[]
        String (blank delimited) or list of contour levels
    nsub : int
        Number of sub-divisions for each contour interval
        E.g. [0,1] with nsub=10 will yield [0, 0.1, 0.2, ..., 1]
    type : string
        linear : default
        log : logarithmic scaling

    Returns
    -------
    levels : string
        List-string of formatted contour levels (space delimited)

    See Also
    --------
    float_format : method
        Reformats floating point numbers into string values

    """
    clevs_f = []
    levels = []

    # Set up interpolation parameters

    if type.upper() == 'LOG':
        interpolate = np.logspace
        options = dict(base=np.e, dtype=float)
        clevs = [np.log(float(clev)) for clev in clevs.split() if clev != ' ']
    else:
        interpolate = np.linspace
        options = dict(dtype=float)
        clevs = [float(clev) for clev in clevs.split() if clev != ' ']

    # Interpolate to sub-divisions

    for index, clev in enumerate(clevs[0:-1]):
        levels = interpolate(clev, clevs[index+1], nsub+1, **options)
        clevs_f += [float_format(level) for level in levels[0:-1]]

    clevs_f.append(float_format(levels[-1]))

    return ' '.join(clevs_f)
