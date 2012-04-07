from datetime import date

from boundaryservice import utils

SHAPEFILES = {
    'Counties': {
        'file': 'COUNTY/county.shp',
        'singular': 'County',
        'kind_first': False,
        'ider': utils.simple_namer(['COUNTY']),
        'namer': utils.simple_namer(['NAME']),
        'authority': 'CSA',
        'domain': 'Oklahoma',
        'last_updated': date(2011, 5, 14),
        'href': '',
        'notes': '',
        'encoding': '',
        #'srid': ''
    },
    'Municipal Boundaries': {
        'file': 'MUNIBND/munibnd.shp',
        'singular': 'Municipal Boundary',
        'kind_first': False,
        'ider': utils.simple_namer(['FIPS']),
        'namer': utils.simple_namer(['CITYNAME']),
        'authority': 'CSA',
        'domain': 'Oklahoma',
        'last_updated': date(2012, 3, 15),
        'href': '',
        'notes': '',
        'encoding': '',
        #'srid': ''
    },
    'INCOG Corporate Limits': {
        'file': 'incog_coporate_limits/Tulsa_CL.shp',
        'singular': 'INCOG Corporate Limits',
        'kind_first': False,
        'ider': utils.simple_namer(['OBJECTID']),
        'namer': utils.simple_namer(['CITY_NAME']),
        'authority': 'INCOG',
        'domain': 'Tulsa',
        'last_updated': date(2011, 5, 14),
        'href': '',
        'notes': '',
        'encoding': '',
        #'srid': ''
    },
    #'2000 Census Blocks': {
    #    'file': '2000_census/blocks.shp',
    #    'singular': '2000 Census Block',
    #    'kind_first': False,
    #    'ider': utils.simple_namer(['ID']),
    #    'namer': utils.simple_namer(['ABNAME']),
    #    'authority': 'CSA',
    #    'domain': 'Oklahoma',
    #    'last_updated': date(2000, 12, 31),
    #    'href': '',
    #    'notes': '',
    #    'encoding': '',
    #    #'srid': ''
    #},
}
