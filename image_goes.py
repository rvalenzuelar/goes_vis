'''

www.ncdc.noaa.gov/gridsat/index.php?name=data
ftp://eclipse.ncdc.noaa.gov/cdr/gridsat

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import os

from mpl_toolkits.basemap import Basemap, cm
from mpl_toolkits.axes_grid1 import ImageGrid
from netCDF4 import Dataset
from glob import glob
from rv_utilities import add_colorbar
from datetime import datetime
import cartopy.crs as ccrs
from matplotlib.collections import LineCollection


def main():
    # fig,ax=plt.subplots(1,3,sharey=True)
    # cfsr_file='/home/rvalenzuela/GOES/NETCDF/GRIDSAT-B1.1998.01.18.21.v02r01.nc'
    # plot_sector(filein=cfsr_file,ax=ax[0])
    # cfsr_file='/home/rvalenzuela/GOES/NETCDF/GRIDSAT-B1.1998.01.19.00.v02r01.nc'
    # plot_sector(filein=cfsr_file,ax=ax[1])
    # cfsr_file='/home/rvalenzuela/GOES/NETCDF/GRIDSAT-B1.1998.01.19.00.v02r01.nc'
    # plot_sector(filein=cfsr_file,ax=ax[2])
    # plt.show(block=False)

    # fs=glob('/home/rvalenzuela/GOES/NETCDF/case02/*.nc')
    # fs.sort()
    # grid=create_figure(grid=(4,3))
    # for n, f in enumerate(fs[:-1]):
    # 	plot_sector(filein=f ,ax=grid[n])
    # plt.show(block=False)


    # fig=plt.figure()
    # grid = ImageGrid(fig,111,	nrows_ncols=(4,3),
    # 					axes_pad=0.1,cbar_mode='single',cbar_location='top')
    # fs=glob('/home/rvalenzuela/GOES/NETCDF/case02/*.nc')
    # fs.sort()
    # for n, f in enumerate(fs[:-1]):
    # 	plot_sector(filein=f ,ax=grid[n])
    # plt.show(block=False)


    # fs = glob('/home/rvalenzuela/GOES/GRIDSAT/netcdf/case14/*.nc')
    fs = glob('/Users/raulvalenzuela/Downloads/*.nc')
    fs.sort()

    # sector = dict(latn=30,latx=55,lonn=-150,
                  # lonx=-120) # US west coast

    sector = dict(latn=-55, latx=-25,
                  lonn=-106, lonx=-63)  # South America

    boundary = dict(lw=1,color='k')

    # for f in fs:
    #     grid = create_figure(figsize=(8, 6), grid=(1, 1))
    #     plot_sector(filein=f, ax=grid[0], colorbar=True,
    #                 labels=True, sector=sector)
    #     fout = f.replace('netcdf', 'jpg')
    #     fout = fout.replace('nc', 'jpg')
    #     plt.savefig(fout)
    #     plt.close('all')

    grid = create_figure(figsize=(8, 8), grid=(3, 2))

    plot_sector(filein=fs[0], ax=grid[0], colorbar=True,
                lonlabel=False, sector=sector, target='irwin_cdr',
                boundary=boundary, id='(a)')
    plot_sector(filein=fs[1], ax=grid[2], colorbar=False,
                lonlabel=False, sector=sector, target='irwin_cdr',
                boundary=boundary, id='(c)')
    plot_sector(filein=fs[2], ax=grid[4], colorbar=False,
                sector=sector, target='irwin_cdr',
                boundary=boundary, id='(e)')

    plot_sector(filein=fs[0], ax=grid[1], colorbar=True,
                labels=False, sector=sector, target='irwvp',
                boundary=boundary, id='(b)')
    plot_sector(filein=fs[1], ax=grid[3], colorbar=False,
                labels=False,sector=sector, target='irwvp',
                boundary=boundary, id='(d)')
    plot_sector(filein=fs[2], ax=grid[5], colorbar=False,
                latlabel=False, sector=sector, target='irwvp',
                boundary=boundary, id='(f)')


    for g in grid:
        g.scatter(-73, -37.8, s=50)

    grid[0].annotate('Nahuelbuta',
                     color='white',ha='right',
                     xy=(-73, -37.8), xycoords='data',
                     xytext=(-80, -30), textcoords='data',
                     arrowprops=dict(arrowstyle="-")
                     )


    # grid[0].annotate('lower',
    #                  color='k',ha='right',
    #                  xy=(0.12, 1.115), xycoords=grid[0].transAxes,
    #                  xytext=(0.35, 1.1), textcoords=grid[0].transAxes,
    #                  arrowprops=dict(arrowstyle="->")
    #                  )
    #
    # grid[0].annotate('higher',
    #                  color='k',ha='right',
    #                  xy=(0.8, 1.115), xycoords=grid[0].transAxes,
    #                  xytext=(0.7, 1.1), textcoords=grid[0].transAxes,
    #                  arrowprops=dict(arrowstyle="->")
    #                  )
    #
    # grid[1].annotate('drier',
    #                  color='k',ha='right',
    #                  xy=(0.12, 1.115), xycoords=grid[1].transAxes,
    #                  xytext=(0.35, 1.1), textcoords=grid[1].transAxes,
    #                  arrowprops=dict(arrowstyle="->")
    #                  )
    #
    # grid[1].annotate('wetter',
    #                  color='k',ha='right',
    #                  xy=(0.8, 1.115), xycoords=grid[1].transAxes,
    #                  xytext=(0.7, 1.1), textcoords=grid[1].transAxes,
    #                  arrowprops=dict(arrowstyle="->")
    #                  )


    fout = fs[0].replace('netcdf', 'jpg')
    fout = fout.replace('nc', 'jpg')
    plt.savefig(fout)
    plt.close('all')
    print('ready!')

def create_figure(figsize=None, grid=None):

    plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(grid[0], grid[1])
    gs.update(top=0.95, bottom=0.05,
              wspace=0.05, hspace=0)
    ax = []
    for g in gs:
        ax.append(plt.subplot(g))

    return ax


def plot_sector(filein=None, ax=None,
                latlabel=True, lonlabel=True,
                labels=True,
                colorbar=False, sector=None,
                target=None,
                boundary=None,
                id=None):

    latn = sector['latn']
    latx = sector['latx']
    lonn = sector['lonn']
    lonx = sector['lonx']

    lw = boundary['lw']
    color = boundary['color']

    data = Dataset(filein, 'r')
    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]
    idxlon = np.where((lons > lonn) & (lons < lonx))[0]
    idxlat = np.where((lats > latn) & (lats < latx))[0]
    array = np.squeeze(
        data.variables[target][:, idxlat, idxlon]) - 273.15
    data.close()

    lats2 = lats[idxlat]
    lons2 = lons[idxlon]

    if target == 'irwin_cdr':
        mycmap = goes_cmap(type='ir')
    elif target == 'irwvp':
        mycmap = goes_cmap(type='wvp')

    im = ax.pcolormesh(lons2, lats2, array,
                       cmap=mycmap,
                       vmax=20,
                       vmin=-60,
                       )

    add_boundaries(ax,sector,lw=lw,color=color)

    latlabels = ['','50S','','40','','30','']
    ax.set_yticklabels(latlabels,rotation=90)

    lonlabels = ['123','100W','90','80','70']
    ax.set_xticklabels(lonlabels)

    ax.set_xlim([lonn, lonx])
    ax.set_ylim([latn, latx])

    if labels is False:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    elif latlabel is False:
        ax.set_yticklabels([])
    elif lonlabel is False:
        ax.set_xticklabels([])

    if colorbar:
        cbar = add_colorbar(ax, im,loc='top',size='10%',label='',
                            ticks_inside=True,tick_color='w')
        cbar.ax.invert_xaxis()

    if id is not None:
        ax.text(0.05,0.9,id,fontsize=14,
                color='w',weight='bold',
                transform=ax.transAxes)

    filedate = filein[-23:-10]
    timest = datetime.strptime(filedate,'%Y.%M.%d.%H')
    ax.text(0.05, 0.05, timest.strftime('%Y-%M-%d %HUTC'),
            color='black',
            weight='bold',
            transform=ax.transAxes)

    plt.draw()


def goes_cmap(type=None):
    " stackoverflow hitzg answer "

    if type == 'ir':
        colors1 = plt.cm.gray_r(np.linspace(0.1, 0.8, 128))
        colors2 = plt.cm.nipy_spectral_r(np.linspace(0, 0.74, 214))
        colors = np.vstack((colors2, colors1))
        mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap',
        colors)
    elif type == 'wvp':
        colors1 = plt.cm.copper(np.linspace(0.1, 0.8, 150))
        colors2 = plt.cm.gray_r(np.linspace(0.1, 0.8, 100))
        colors3 = plt.cm.Blues_r(np.linspace(0, 0.74, 50))
        colors = np.vstack((colors3, colors2, colors1))
        mymap = mcolors.LinearSegmentedColormap.from_list(
            'my_colormap',
            colors)

    return mymap


def plot_global(cfsr_file):
    data = Dataset(cfsr_file, 'r')
    lats = data.variables['lat'][:]
    lons = data.variables['lon'][:]

    array = np.squeeze(data.variables['irwin_cdr'][:, :, :])

    latn = data.geospatial_lat_min
    latx = data.geospatial_lat_max
    lonn = data.geospatial_lon_min
    lonx = data.geospatial_lon_max
    data.close()

    lons2d, lats2d = np.meshgrid(lons, lats)

    m = Basemap(projection='merc',
                llcrnrlat=latn,
                urcrnrlat=latx,
                llcrnrlon=lonn,
                urcrnrlon=lonx,
                resolution='l')

    m.drawcoastlines()
    m.pcolormesh(lons2d, lats2d, array, latlon=True, cmap='gray')
    plt.show()


def add_boundaries(ax,sector,lw=1,color='k'):

    latn = sector['latn']
    latx = sector['latx']
    lonn = sector['lonn']
    lonx = sector['lonx']

    m = Basemap(projection='cyl', lat_0=35, lon_0=-130,
                resolution='c',
                area_thresh=0.1,
                llcrnrlon=lonn,
                llcrnrlat=latn,
                urcrnrlon=lonx,
                urcrnrlat=latx)

    coastline = m.coastpolygons
    for line in coastline:
        ax.plot(line[0], line[1],
                linewidth=lw,
                color=color)

    cnts,types = m._readboundarydata('countries')
    countries = LineCollection(cnts,
                               color=color,
                               linewidth=lw)
    ax.add_collection(countries)


main()
