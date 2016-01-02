'''
	Script for dowloading GOES gridsat products 
	from http://www.ncdc.noaa.gov/gridsat/index.php?name=data

	Raul Valenzuela
	December, 2105
	raul.valenzuela@colorado.edu
'''

import pandas as pd
import os
import urllib
import sys

from glob import glob

def main(*arg):

	cwd=os.getcwd()

	cnum=arg[0][1]
	file_list = get_case_file_list(int(cnum))
	folder='/netcdf/case'+cnum.zfill(2)
	ok = check_path(cwd+folder)

	if ok:
		print 'Saving ...'
		for f in file_list:
			fname = os.path.basename(f)
			fout=cwd+folder+'/'+fname
			urllib.urlretrieve(f,fout)
		print 'done\n'


def check_path(path):

	isdir = os.path.isdir(path)
	if isdir:
		fs=glob(path+'/*.nc')
		if not fs:
			print 'Downloading to '+path
			return 1
		else:
			print 'Directory: \n'+path
			print 'contains netCDF files'
			return 0
	else:
			print 'Directory: \n'+path
			usr_input = raw_input('does not exist. Do you want to create it? [y/n]: ')
			if usr_input == 'n':
				print 'No files dowloaded'
				return 0
			elif usr_input == 'y':
				os.makedirs(path)
				return 1

def get_case_file_list(case):

	base_dir='ftp://eclipse.ncdc.noaa.gov/cdr/gridsat/files/'
	set_prefix='GRIDSAT-B1'
	set_suffix='v02r01.nc'
	dates=[]
	dates.append(pd.date_range('1998-01-18 00:00', '1998-01-19 00:00', freq='3H')) # 1
	dates.append(pd.date_range('1998-01-26 00:00', '1998-01-27 12:00', freq='3H')) # 2
	dates.append(pd.date_range('2001-01-23 00:00', '2001-01-24 12:00', freq='3H')) # 3
	dates.append(pd.date_range('2001-01-25 00:00', '2001-01-27 00:00', freq='3H')) # 4
	dates.append(pd.date_range('2001-02-09 00:00', '2001-02-10 15:00', freq='3H')) # 5
	dates.append(pd.date_range('2001-02-11 00:00', '2001-02-12 00:00', freq='3H')) # 6
	dates.append(pd.date_range('2001-02-17 00:00', '2001-02-18 00:00', freq='3H')) # 7
	dates.append(pd.date_range('2003-01-12 12:00', '2003-01-14 15:00', freq='3H')) # 8
	dates.append(pd.date_range('2003-01-21 03:00', '2003-01-23 09:00', freq='3H')) # 9
	dates.append(pd.date_range('2003-02-15 18:00', '2003-02-16 12:00', freq='3H')) # 10
	dates.append(pd.date_range('2004-01-09 12:00', '2004-01-10 00:00', freq='3H')) # 11
	dates.append(pd.date_range('2004-02-02 00:00', '2004-02-03 00:00', freq='3H')) # 12
	dates.append(pd.date_range('2004-02-16 00:00', '2004-02-18 09:00', freq='3H')) # 13
	dates.append(pd.date_range('2004-02-25 06:00', '2004-02-26 00:00', freq='3H')) # 14

	dates_case=dates[case-1]
	file_list=[]
	for d in dates_case:
		dt=d.to_datetime()
		item=base_dir+str(d.year)+'/'+set_prefix+dt.strftime('.%Y.%m.%d.%H.')+set_suffix
		file_list.append(item)

	return file_list

main(sys.argv)