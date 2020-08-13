from astroquery.xmatch import XMatch
from astropy import units as u
from astropy.table import Table
from astropy.coordinates import SkyCoord
import pickle

# get the data from the pkl file
with open('coord_list.pkl', 'rb') as f:
    data = pickle.load(f)

# create an astropy table with RA and Dec as column
ra = []
dec = []
for coord in data:
    ra.append(coord.ra.value)
    dec.append(coord.dec.value)
tab = Table([ra, dec], names=('RA', 'Dec'))

# define the maximim distance for the cross match
xmatch_distance = 20 * u.arcsec

# cross match local file with Simbad through the Xmatch service
tab.write('orig_coord.csv', overwrite=True)
xmatch_tab = XMatch.query(cat1=open('orig_coord.csv'),
                          cat2='SIMBAD', max_distance=xmatch_distance,
                          colRA1='RA', colDec1='Dec')

# xmatch_tab will only have entries for those sources that have a cross
# match in Simbad, so to get a lists of those coordinates that do not have
# a cross match in Simbad we use the cross matching fuctionalities of
# astropy (https://docs.astropy.org/en/stable/coordinates/matchsep.html#astropy-coordinates-matching)
orig_coord = SkyCoord(ra=tab['RA']*u.degree, dec=tab['Dec']*u.degree)
xmatch_coord = SkyCoord(ra=xmatch_tab['RA']*u.degree,
                        dec=xmatch_tab['Dec']*u.degree)
nearest_source_index, dist_2d, dist_3d = orig_coord.match_to_catalog_sky(xmatch_coord)

# this procedure provides the shortest distance (dist_2d) for all entries from
# the XMatch result table to entries in the original table of all coordinates
# if we now just select those entires with short shortest distances we get
# a table of all coordinates with a cross match in Simbad, if we select those
# entries with large shortest distances we get the coordinates with no cross
# match in Simbad
mask_crossmatch = dist_2d <= xmatch_distance
mask_no_match = dist_2d > xmatch_distance

coords_crossmatch = tab[mask_crossmatch]
coords_no_match = tab[mask_no_match]

print(len(coords_no_match))
