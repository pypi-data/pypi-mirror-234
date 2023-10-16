import os
import copy
import subprocess
import numpy as np
import matplotlib.pylab as plt


# defaults for practical 2
displacement_map = 'E451_20000818_20020719.unw'
sample    = 1100
line      = 980
posting   = 40.0
half_wave = 28.3


def extents(vector_component):
    '''

    Returns the extent of an array for plotting

        vector_component: the input numpy array

    '''
    delta = vector_component[1] - vector_component[0]
    return [vector_component[0] - delta/2, vector_component[-1] + delta/2]



def load_data():
    '''

    Loads LOS InSAR surface displacement
    Returns the masked LOS map

    '''

    with open (displacement_map, 'rb') as f:
        coh = np.fromfile(f, dtype='>f', count=-1)

    observed_displacement_map = np.reshape(coh, (line, sample))

    # rescale insar phase into surface displacement in cm units and replace all nans with 0
    observed_displacement_map = observed_displacement_map*half_wave/2.0/np.pi
    where_are_NaNs = np.isnan(observed_displacement_map)
    observed_displacement_map[where_are_NaNs] = 0

    # create mask
    observed_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, observed_displacement_map)

    return observed_displacement_map_m


def plot_model(los):
    '''

    Plots the interferogram LOS and the corresponding surface displacement.

        - los : Line-of-sight 2D array (numpy)

    '''
    # Calculate the bounding box
    extent_xvec = extents((np.arange(1, sample*posting, posting)) / 1000)
    extent_yvec = extents((np.arange(1, line*posting, posting)) / 1000)
    extent_xy = extent_xvec + extent_yvec

    plt.rcParams.update({'font.size': 14})
    inwrapped = (los/10 + np.pi) % (2*np.pi) - np.pi
    cmap = copy.copy(plt.cm.get_cmap("jet"))
    cmap.set_bad('white', 1.)

    # Plot displacement
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_subplot(1, 2, 1)
    im = ax1.imshow(los, interpolation='nearest', cmap=cmap, extent=extent_xy, origin='upper')
    cbar = ax1.figure.colorbar(im, ax=ax1, orientation='horizontal')
    ax1.set_title("Displacement in look direction [mm]")
    ax1.set_xlabel("Easting [km]")
    ax1.set_ylabel("Northing [km]")
    plt.grid()

    # Plot interferogram
    im.set_clim(-30, 30)
    ax2 = fig.add_subplot(1, 2, 2)
    im = ax2.imshow(inwrapped, interpolation='nearest', cmap=cmap, extent=extent_xy, origin='upper')
    cbar = ax2.figure.colorbar(im, ax=ax2, orientation='horizontal')
    ax2.set_title("Interferogram phase [rad]")
    ax2.set_xlabel("Easting [km]")
    ax2.set_ylabel("Northing [km]")
    plt.grid()

    return


def calc_forward_model_mogi(n1, e1, depth, delta_volume, northing, easting, plook):
    '''
    Function to calculate a forward model for a Mogi source.

        - n1: the north coordinate component of the source location [m]
        - e1: the east coordinate component of the source location [m]
        - depth: the depth of the source [m]
        - delta_volume: the volume change [m^3]
        - northing: grid of surface observations (north compoent)
        - easting: grid of surface observations (east component)
        - plook: the look angle for the InSAR mission

    Returns the Mogi synthetic LOS.

    '''
    # This geophysical coefficient is needed to describe how pressure relates to volume change
    displacement_coefficient = (1e6*delta_volume*3)/(np.pi*4)

    # Calculating the horizontal distance from every point in the displacement map to the x/y source location
    d_mat = np.sqrt(np.square(northing-n1) + np.square(easting-e1))

    # denominator of displacement field for mogi source
    tmp_hyp = np.power(np.square(d_mat) + np.square(depth),1.5)

    # horizontal displacement
    horizontal_displacement = displacement_coefficient * d_mat / tmp_hyp

    # vertical displacement
    vertical_displacement = displacement_coefficient * depth / tmp_hyp

    # azimuthal angle
    azimuth = np.arctan2((easting-e1), (northing-n1))

    # compute north and east displacement from horizontal displacement and azimuth angle
    east_displacement = np.sin(azimuth) * horizontal_displacement
    north_displacement = np.cos(azimuth) * horizontal_displacement

    # project displacement field onto look vector
    temp = np.concatenate((east_displacement, north_displacement, vertical_displacement), axis=1)
    delta_range = temp.dot(np.transpose([plook]))
    delta_range = -1.0 * delta_range

    return delta_range


def displacement_data_from_mogi(x, y, z, volume, iplot, imask):
    '''

    Creates simulated displacement data based on Mogi Source Model parameters

    '''

    # Organizing model parameters
    bvc = [x, y, z, volume, 0, 0, 0, 0]
    bvc = np.asarray(bvc, dtype=object)
    bvc = np.transpose(bvc)

    # Setting acquisition parameters
    track =  -13.3*np.pi / 180.0
    look  = 23.0*np.pi / 180.0
    plook = [-np.sin(look)*np.cos(track), np.sin(look)*np.sin(track), np.cos(look)]

    # Defining easting and northing vectors
    northing = np.arange(0, (line)*posting, posting) / 1000
    easting = np.arange(0, (sample)*posting, posting) / 1000
    northing_mat = np.tile(northing, (sample, 1))
    easting_mat = np.transpose(np.tile(easting, (line, 1)))
    northing_vec = np.reshape(northing_mat, (line*sample, 1))
    easting_vec = np.reshape(easting_mat, (line*sample, 1))

    # Handing coordinates and model parameters over to the rngchg_mogi function
    calc_range = calc_forward_model_mogi(bvc[1], bvc[0], bvc[2], bvc[3], northing_vec, easting_vec, plook)

    # Reshaping surface displacement data derived via calc_forward_model_mogi()
    surface_displacement = np.reshape(calc_range, (sample,line))

    # return rotated surface displacement
    return np.transpose(np.fliplr(surface_displacement))

def plot_forward_model_mogi(zs,volume,observed_displacement_map):
    '''

    Plots a foward model with different values of source location x,y


        - zs: depth in km
        - volume: volume change in km^3
    '''
    plt.rcParams.update({'font.size': 14})
    extent_x = extents((np.arange(1, sample*posting, posting))/1000)
    extent_y = extents((np.arange(1, line*posting, posting))/1000)
    extent_xy = extent_x + extent_y

    xs = np.arange(18, 24.2, 0.4)
    ys = np.arange(20, 24.2, 0.4)

    xa = [0, 7, 15]
    ya = [0 ,5, 10]

    fig = plt.figure(figsize=(18, 18))
    cmap = copy.copy(plt.cm.get_cmap("jet"))
    subplot_index = 1

    for k in xa:
        for l in ya:
            ax = fig.add_subplot(3, 3, subplot_index)
            predicted_displacement_map = displacement_data_from_mogi(xs[k], ys[l], zs, volume, 0, 0)
            predicted_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, predicted_displacement_map)
            im = ax.imshow(predicted_displacement_map_m, cmap=cmap, extent=extent_xy)
            cbar = ax.figure.colorbar(im, ax=ax, orientation='horizontal')
            plt.grid()
            im.set_clim(-30, 30)
            ax.plot(xs[k],ys[l], 'k*', markersize=25, markerfacecolor='w')
            ax.set_title('Source: X=%4.2fkm; Y=%4.2fkm' % (xs[k], ys[l]))
            ax.set_xlabel("Easting [km]")
            ax.set_ylabel("Northing [km]")
            subplot_index += 1

    return


def search_mogi_location(xmin,xmax,xinc,ymin,ymax,yinc,zs,volume,observed_displacement_map):
    '''

    Grid search for x and y source location, while fixing the depth and the volume change.

        - xmin: start of x range
        - xmax: end of x range
        - xminc: increment of x
        - ymin: start of y range
        - ymax: end of y range
        - yminc: increment of y
        - zs: depth [km]
        - volume: volume change [km^3]
        - observed_displacement_map: observed LOS array
    '''

    # create mask
    observed_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, observed_displacement_map)

    # Setting up search parameters
    xs = np.arange(xmin, xmax, xinc)
    ys = np.arange(ymin, ymax, yinc)

    nx = xs.size
    ny = ys.size
    ng = nx * ny;

    print(f"fixed z = {zs}km, dV = {volume}, searching over (x,y)")

    misfit = np.zeros((nx, ny))
    subplot_index = 0

    # Commence grid-search for best model parameters
    for k, xv in enumerate(xs):
        for l, yv in enumerate(ys):
            subplot_index += 1
            predicted_displacement_map = displacement_data_from_mogi(xs[k], ys[l], zs, volume, 0, 0)
            predicted_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, predicted_displacement_map)
            misfit[k,l] = np.sum(np.square(observed_displacement_map_m - predicted_displacement_map_m))
        print(f"Source {subplot_index:3d}/{ng:3d} is x = {xs[k]:.2f} km, y = {ys[l]:.2f} km")

    # Searching for the minimum in the misfit matrix
    mmf = np.where(misfit == np.min(misfit))
    print(f"\n----------------------------------------------------------------")
    print('Best fitting Mogi Source located at: X = %5.2f km; Y = %5.2f km' % (xs[mmf[0]], ys[mmf[1]]))
    print(f"----------------------------------------------------------------")


    return xs[mmf[0]], ys[mmf[1]],misfit



def search_mogi_source(zmin,zmax,zinc,vmin,vmax,vinc,xs,ys,observed_displacement_map):
    '''
     Grid search for zs and volume source parameters, while fixing the depth and the volume change.

        - zmin: start of depth range
        - zmax: end of depth range
        - zminc: increment of depth
        - vmin: start of volume range
        - vmax: end of volume range
        - vminc: increment of volume
        - xs: x source location [km]
        - ys: y source location [km]
        - observed_displacement_map: observed LOS array
    '''
    # create mask
    observed_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, observed_displacement_map)


    zs = np.arange(zmin,zmax,zinc);
    volume = np.arange(vmin,vmax,vinc)

    nz = zs.size
    nv = volume.size
    ng = nz * nv;

    print(f"fixed x = {xs}km, y = {ys}, searching over (zs,volume)")

    misfit = np.zeros((nz, nv))
    subplot_index = 0

    # Commence grid-search for best model parameters
    for k, zv in enumerate(zs):
        for l, vv in enumerate(volume):
            subplot_index += 1
            predicted_displacement_map = displacement_data_from_mogi(xs, ys, zs[k], vv, 0, 0)
            predicted_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, predicted_displacement_map)
            misfit[k,l] = np.sum(np.square(observed_displacement_map_m - predicted_displacement_map_m))
        print(f"Source {subplot_index:3d}/{ng:3d} is z = {zs[k]:.2f} km, v = {volume[l]:.5f} km^3")

    # Searching for the minimum in the misfit matrix
    mmf = np.where(misfit == np.min(misfit))
    print(f"\n----------------------------------------------------------------")
    print('Best fitting Mogi Source located at: Z = %5.2f km; V = %5.5f km' % (zs[mmf[0]], volume[mmf[1]]))
    print(f"----------------------------------------------------------------")


    return zs[mmf[0]], volume[mmf[1]],misfit

def plot_fit_mogi(xsfit,ysfit,zs,volume,observed_displacement_map):
    '''

    Plot the calculate forward Mogi source LOS map, given source parameters

    '''

    # create mask
    observed_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, observed_displacement_map)

    # Calculate predicted displacement map for best-fitting Mogi parameters:
    predicted_displacement_map = displacement_data_from_mogi(xsfit, ysfit, zs, volume, 0, 0)

    # Mask the predicted displacement map to remove pixels incoherent in the observations:
    predicted_displacement_map_m = np.ma.masked_where(observed_displacement_map==0, predicted_displacement_map)

    # Plot observed displacement map
    plot_model(observed_displacement_map_m)

    # Plot simulated displacement map
    plot_model(predicted_displacement_map_m)

    # Plot simulated displacement map without mask applied
    plot_model(predicted_displacement_map)

    return


def plot_misfit_mogi(xmin,xmax,xinc,ymin,ymax,yinc,xsfit,ysfit,misfit):
    '''

    Plots the misfit function and the best-fit parameters.

    '''

    # Setting up search parameters
    xs = np.arange(xmin, xmax, xinc)
    ys = np.arange(ymin, ymax, yinc)

    plt.rcParams.update({'font.size': 18})
    extent_xy = extents(xs) + extents(ys)
    fig = plt.figure(figsize=(10, 10))
    cmap = copy.copy(plt.cm.get_cmap("jet"))
    ax1 = fig.add_subplot(1, 1 ,1)
    im = ax1.imshow(np.transpose(misfit), origin='lower', cmap=cmap, extent=extent_xy)
    ax1.set_aspect('auto')
    cbar = ax1.figure.colorbar(im, ax=ax1, orientation='horizontal')
    ax1.plot(xsfit, ysfit, 'k*', markersize=25, markerfacecolor='w')
    ax1.set_title("Misfit Function for Mogi-Source Approximation")
    ax1.set_xlabel("Parameter 1")
    ax1.set_ylabel("Parameter 2")

    return
