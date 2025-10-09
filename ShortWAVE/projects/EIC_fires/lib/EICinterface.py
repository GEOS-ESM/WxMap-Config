import re
import argparse
import datetime as dt

class Interface(object):

    def __init__(self, description):

        self.parser = argparse.ArgumentParser(description=description)

        self.parser.add_argument('datetime', metavar='datetime', type=str,
                    help='ISO datetime as ccyy-mm-ddThh:mm:ss')
        self.parser.add_argument('config', metavar='config', type=str,
                    help='configuration file (.yml)')
        self.parser.add_argument('--theme', metavar='theme', type=str,
                    default='default', help='Name of configuration theme')
        self.parser.add_argument('--create', action='store_true',
                    help='Create fire event(s)')
        self.parser.add_argument('--init', action='store_true',
                    help='Initialize basemaps')
        self.parser.add_argument('--stats', action='store_true',
                    help='Generate statistics')
        self.parser.add_argument('--base', action='store_true',
                    help='Generate base images')
        self.parser.add_argument('--final', action='store_true',
                    help='Generate final images')
        self.parser.add_argument('--movie', action='store_true',
                    help='Generate movie files')
        self.parser.add_argument('--monitor', action='store_true',
                    help='Generate fire monitor images')
        self.parser.add_argument('--plot', action='store_true',
                    help='Generate all EIC fire images and movies')
        self.parser.add_argument('--publish', action='store_true',
                    help='Publish visuals')
        self.parser.add_argument('--purge', action='store_true',
                    help='Purge events')

    def get_args(self):

        args = self.parser.parse_args()

        dattim = re.sub('[^0-9]', '', args.datetime+'000000')[0:14]
        idate = int(dattim[0:8])
        itime = int(dattim[8:14])
        time_dt = dt.datetime.strptime(dattim,'%Y%m%d%H%M%S')

        args_dict = vars(args)
        args_dict.update({'date': idate, 'time': itime, 'time_dt': time_dt})

        return args_dict
