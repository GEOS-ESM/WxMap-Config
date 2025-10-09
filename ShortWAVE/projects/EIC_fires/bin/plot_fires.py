#! /usr/bin/env python

import os
import sys

import EICinterface
from handlers import *
from myutils import read_yaml
from fire_events import FireResponder

# Retrieve command-line arguments.

ui = EICinterface.Interface('EIC Fire Visualizer')
args = ui.get_args()
arg_dt = args['time_dt']
arg_plot = args['plot']

# Get configuration.
# ==================

# Get main workflow config
# ------------------------

config = read_yaml(args['config'])
theme = config[args['theme']]
cfg_base = theme['base_images']
cfg_final = theme['final_images']
cfg_movies = theme['movies']
cfg_publish = theme['publish']
cfg_latest = theme['publish_latest']
cfg_stats = theme['stats']
cfg_monitor = theme['monitor']
cfg_clean = theme['clean']
max_events = config.get('max_events', 2)

responder = FireResponder()

# Create event(s)
# ---------------

if args['create']:
    responder.execute(make_event, cfg_base, time_dt=arg_dt,
                      event_file=cfg_base['config'],
                      stat_file=cfg_stats['config'],
                      plot_domain_size=config['plot_domain_size'],
                      stat_domain_size=config['stat_domain_size'],
                      fire_source=config['EIC_fire_source'])


# Retrieve events
# ----------------

events = responder.execute(get_events, cfg_base, time_dt=arg_dt,
                           event_file=cfg_base['config'],
                           max_events=max_events)

# Pre-generate basemaps
# ---------------------

if args['init']:
    responder.execute(make_base, cfg_base, events=events,
                      ntasks=1, time_dt=arg_dt, tloop=False)
    sys.exit(0)

# Generate base images for all events.
# ------------------------------------

if arg_plot or args['base']:
    responder.execute(make_base, cfg_base, events=events, time_dt=arg_dt)

# Generate fire statistics for each event.
# ----------------------------------------

if arg_plot or args['stats']:
    responder.execute(make_stats, cfg_stats, events=events,
                      time_dt=arg_dt, tloop=False)

# Create fire monitor images
# --------------------------

if arg_plot or args['monitor']:
    responder.execute(make_monitor, cfg_monitor, events=events,
                      time_dt=arg_dt, iname=cfg_stats['oname'])

# Create final images with annotation
# -----------------------------------

if arg_plot or args['final']:
    places = responder.execute(get_places, cfg_final)
    responder.execute(make_final, cfg_final, events=events, time_dt=arg_dt,
                      iname=cfg_base['oname'], places=places)

# Generate movie files
# --------------------

if arg_plot or args['movie']:
    responder.execute(make_movie, cfg_movies, events=events,
                      time_dt=arg_dt, tloop=False, iname=cfg_final['oname'],
                      playlist=cfg_final['playlist'])

    responder.execute(make_movie, cfg_movies, events=events,
                      time_dt=arg_dt, tloop=False, iname=cfg_monitor['oname'],
                      playlist=cfg_monitor['playlist'])

# Publish EIC movies
# ------------------

if args['publish']:
    playlist = cfg_final['playlist'] | cfg_monitor['playlist']

    responder.execute(publish, cfg_publish, events=events, ntasks=1,
                      time_dt=arg_dt, tloop=False, iname=cfg_movies['oname'],
                      playlist=playlist)

    responder.execute(purge, cfg_latest, events=events, time_dt=arg_dt,
                      playlist={'dummy': {}}, ntasks=1)

    responder.execute(publish, cfg_latest, events=events, ntasks=1,
                      time_dt=arg_dt, tloop=False, iname=cfg_movies['oname'],
                      playlist=playlist)

# Purge expired files
# -------------------

if args['purge']:
    responder.execute(purge, cfg_clean, events=events, time_dt=arg_dt,
                      playlist={'dummy': {}})

sys.exit(0)
