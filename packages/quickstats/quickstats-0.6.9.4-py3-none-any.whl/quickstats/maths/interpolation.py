import numpy as np

def get_intervals(x:np.ndarray, y:np.ndarray, level:float, delta:float=0.0001):
    from scipy.interpolate import interp1d
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    y = y[sort_idx]
    func_interp = interp1d(x, y, fill_value="extrapolate")
    x_interp = np.arange(min(x), max(x), delta)
    y_interp = func_interp(x_interp)
    # remove points that are nan
    mask = np.argwhere(~np.isnan(y_interp))
    x_interp = x_interp[mask]
    y_interp = y_interp[mask]
    asign = np.sign(y_interp - level)
    sign_change   = (np.roll(asign, 1) - asign) != 0
    # first point can not have a sign change
    sign_change[0][0] = False
    intersections = x_interp[sign_change]
    sign_slope    = asign[sign_change]
    # no intersections
    if len(intersections) == 0:
        return []
    if len(intersections) == 1:
        if sign_slope[0] == -1:
            return np.array([[intersections[0], np.inf]])
        else:
            return np.array([[-np.inf, intersections[0]]])
    else:
        if sign_slope[0] == 1:
            intersections = np.insert(intersections, 0, -np.inf)
        if sign_slope[-1] == -1:
            intersections = np.insert(intersections, intersections.shape[0], np.inf)
        if len(intersections) & 1:
            raise RuntimeError("number of intersections can not be odd")
        n_pairs = len(intersections) // 2
        return intersections.reshape((n_pairs, 2))
    
def get_regular_meshgrid(*xi, n):
    reg_xi = [np.linspace(np.min(x), np.max(x), n) for x in xi]
    return np.meshgrid(*reg_xi)
    
def get_x_intersections(x1, y1, x2, y2):
    """Get x intersections of two curves
    """
    interp_y1 = np.interp(x2, x1, y1) 

    diff = interp_y1 - y2 
    # determines what index intersection points are at 
    idx = np.argwhere(np.diff(np.sign(diff))).flatten()

    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = [x2[i] - (x2[i + 1] - x2[i])/(diff[i + 1] - diff[i]) * diff[i] for i in idx]
    return intersections

def get_intervals_between_curves(x1, y1, x2, y2):
    """Get x intervals of intersection between two curves
    """
    interp_y1 = np.interp(x2, x1, y1) 

    diff = interp_y1 - y2 
    sign_change = np.diff(np.sign(diff))
    # determines what index intersection points are at 
    idx = np.argwhere(sign_change).flatten()
    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = np.array([x2[i] - (x2[i + 1] - x2[i])/(diff[i + 1] - diff[i]) * diff[i] for i in idx])
    # no intersection
    if len(intersections) == 0:
        return intersections
    # one-sided interval
    elif len(intersections) == 1:
        sign = sign_change[idx[0]]
        if sign < 0:
            return np.array([-np.inf, intersections[0]])
        return np.array([intersections[0], np.inf])
    elif len(intersections == 2):
        if (sign_change[idx[0]] + sign_change[idx[1]]) != 0:
            raise RuntimeError('found discontinuous curves')
        return intersections
    raise RuntimeError('found multiple intervals')
    
def interpolate_2d(x:np.ndarray, y:np.ndarray, z:np.ndarray, method:str='cubic', n:int=500):
    from scipy import interpolate
    mask = ~np.isnan(z)
    x, y, z = x[mask], y[mask], z[mask]
    X, Y = get_regular_meshgrid(x, y, n=n)
    Z = interpolate.griddata(np.stack((x, y), axis=1), z, (X, Y), method)
    return X, Y, Z