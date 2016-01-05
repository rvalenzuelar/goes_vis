'''
	Script for dowloading GOES jpg 
	images from www.ncdc.noaa.gov/gibbs

	Raul Valenzuela
	December, 2105
	raul.valenzuela@colorado.edu
'''


import sys 
import urllib
import os 

from urlparse import urlparse

def main(*arg):

	txtfile=arg[0][1]
	txt = open(txtfile)
	cwd = os.getcwd()
	directory = txtfile[:6]
	for n,t in enumerate(txt):
		clean = t.replace('\n','')
		o = urlparse(clean)
		fname = os.path.basename(o.path.replace('\r',''))
		fout = cwd+'/'+directory+'/'+fname+'.jpg'
		print 'saving '+fout
		urllib.urlretrieve(clean,fout)
	print ''

main(sys.argv)