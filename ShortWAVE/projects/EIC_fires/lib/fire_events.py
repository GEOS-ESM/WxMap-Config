from multiprocessing import Pool, cpu_count
from myutils import parse_duration

class FireResponder(object):

    def __init__(self):
        self.num_cores = cpu_count()

    def execute(self, handler, config, events=None, **kwargs):

        task = config.get('task', True)
        task = kwargs.get('task', task)
        if not task or task == 'off':
            return

        if events is None:
            return handler(config | kwargs)

        ntasks = config.get('ntasks', self.num_cores)
        ntasks = kwargs.get('ntasks', ntasks)
        ntasks = min(ntasks, self.num_cores)
        print(f'Using {ntasks} out of {self.num_cores} cores')

        iterator = Player(config, events=events, **kwargs)
        with Pool(ntasks) as pool:
            pool.map(handler, iterator)

class Player(object):

    def __init__(self, config, events=None, **kwargs):

        self.config = dict(config)
        self.config.update(kwargs)
        self.tloop = kwargs.get('tloop', True)
        self.events = {}
        if events:
            self.events = events

    def __iter__(self):

        playlist = self.config['playlist']
        fields = self.config.get('fields', playlist.keys()) 

        for field in fields:

            play = dict(self.config)
            play.update(playlist[field])

            levels = play.get('levels', [0])
            events = list(self.events.keys())
            events.sort()

            fcst_dt = play.get('fcst_dt', 'PT0H')
            start_dt = play.get('start_dt', 'PT0H')
            end_dt = play.get('end_dt', 'PT0H')
            t_deltat = play.get('t_deltat', 'PT1H')
            time_dt = play['time_dt']

            fcst_dt = time_dt + parse_duration(fcst_dt)
            start_dt = time_dt + parse_duration(start_dt)
            end_dt = time_dt + parse_duration(end_dt)
            t_deltat = parse_duration(t_deltat)

            t_start = start_dt
            if not self.tloop:
                t_start = end_dt

            for level in levels:

                for event in events:

                    play.update(self.events.get(event, {}))

                    t = t_start
                    while t <= end_dt:

                        play.update({'field': field,
                                     'event': event,
                                     'level': level,
                                     't_start': t,
                                     't_end': t,
                                     't_deltat': t_deltat,
                                     'fcst_dt': fcst_dt,
                                     'start_dt': start_dt,
                                     'end_dt': end_dt})

                        yield dict(play)

                        t += t_deltat
