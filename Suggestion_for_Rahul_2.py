from astropy import units as u
from astropy.table import Table
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import pickle
import requests
import time

# get the data from the pkl file
with open('coord_list.pkl', 'rb') as f:
    data = pickle.load(f)

ra = []
dec = []
for coord in data:
    ra.append(coord.ra.value)
    dec.append(coord.dec.value)
tab = Table([ra, dec], names=('RA', 'Dec'))

orig_coord = SkyCoord(ra=tab['RA']*u.degree, dec=tab['Dec']*u.degree)

search_radius = [20. * u.arcsec] * len(orig_coord)

try:
    result_table = Simbad.query_region(orig_coord,
                                       radius=search_radius)
except requests.exceptions.ReadTimeout:
    time.sleep(3)
    print('I had to raise an error.')
    result_table = Simbad.query_region(orig_coord,
                                       radius=search_radius)

ra_no_match = []
dec_no_match = []

for entry in result_table.errors:
    ra_no_match.append(entry.msg.split(' ')[0][1:])
    dec_no_match.append(entry.msg.split(' ')[1][:-2])
    print(ra_no_match[-1], dec_no_match[-1])

coords_no_match = SkyCoord(ra=ra_no_match, dec=dec_no_match, unit=u.deg)
print(len(coords_no_match))
