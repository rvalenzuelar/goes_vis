

'''

www.ncdc.noaa.gov/gridsat/index.php?name=data
ftp://eclipse.ncdc.noaa.gov/cdr/gridsat

'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.gridspec as gridspec
import os 

from mpl_toolkits.basemap import Basemap,cm
from mpl_toolkits.axes_grid1 import ImageGrid
from netCDF4 import Dataset
from glob import glob

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


	fs=glob('/home/rvalenzuela/GOES/GRIDSAT/netcdf/case14/*.nc')
	fs.sort()
	for f in fs:
		grid=create_figure(figsize=(8,8), grid=(1,1))
		plot_sector(filein=f ,ax=grid[0],colorbar=True,labels=True)
		fname= os.path.basename(f)
		fout=f.replace('netcdf','jpg')
		fout=fout.replace('nc','jpg')
		plt.savefig(fout)
		plt.close('all')
	# plt.show(block=False)	

def create_figure(figsize=None, grid=None):

	fig=plt.figure(figsize=figsize)
	gs = gridspec.GridSpec(grid[0],grid[1])
	gs.update(top=0.95,bottom=0.05,wspace=0.05,hspace=0.05)
	ax=[]
	for g in gs:
		ax.append(plt.subplot(g))

	return ax


def plot_sector(filein=None,ax=None,labels=False,colorbar=False):

	latn=30.
	latx=55.
	lonn=-150
	lonx=-120

	data = Dataset(filein,'r')
	lats=data.variables['lat'][:]
	lons=data.variables['lon'][:]
	idxlon=np.where( (lons>lonn)&(lons<lonx))[0]
	idxlat=np.where( (lats>latn)&(lats<latx) )[0]
	array = np.squeeze(data.variables['irwin_cdr'][:, idxlat, idxlon])-273.15
	data.close()

	lons2d, lats2d=np.meshgrid(lons[idxlon],lats[idxlat])

	m=Basemap(projection='merc',
					llcrnrlat=latn,
					urcrnrlat=latx,
					llcrnrlon=lonn,
					urcrnrlon=lonx,
					resolution='l',
					ax=ax)

	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()

	parallels=np.arange(-90,90,5)
	meridians=np.arange(-180,180,5)
	if labels:
		sw=1,
	else:
		sw=0
	m.drawparallels(parallels,labels=[sw,0,0,0],fontsize=10)
	m.drawmeridians(meridians,labels=[0,0,0,sw],fontsize=10)
	mycmap=goes_cmap()
	im=m.imshow(array, cmap=mycmap,vmax=20,vmin=-60, aspect='auto')
	if colorbar:
		cb=m.colorbar(im)
		cb.ax.invert_yaxis()
	filedate=filein[-23:-10]
	ax.text(0.05,0.05,filedate,color='black',weight='bold',transform=ax.transAxes)
	plt.draw()

def goes_cmap():

	' stackoverflow hitzg answer'

	colors1 = plt.cm.gray_r(np.linspace(0.1, 0.8, 128))
	# colors2 = plt.cm.rainbow_r(np.linspace(0, 0.9, 128))
	colors2 = plt.cm.nipy_spectral_r(np.linspace(0, 0.74, 214))
	colors = np.vstack((colors2, colors1))
	mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

	return mymap

def plot_global(cfsr_file):

	data = Dataset(cfsr_file,'r')
	lats=data.variables['lat'][:]
	lons=data.variables['lon'][:]

	array = np.squeeze(data.variables['irwin_cdr'][:,:,:])

	latn=data.geospatial_lat_min
	latx=data.geospatial_lat_max
	lonn=data.geospatial_lon_min
	lonx=data.geospatial_lon_max
	data.close()

	lons2d, lats2d=np.meshgrid(lons,lats)

	m=Basemap(projection='merc',
					llcrnrlat=latn,
					urcrnrlat=latx,
					llcrnrlon=lonn,
					urcrnrlon=lonx,
					resolution='l')

	m.drawcoastlines()
	m.pcolormesh(lons2d, lats2d, array, latlon=True, cmap='gray')
	plt.show()


main()
