    def add_ENSO_context(self, plot):
        """
        Adds contextual parameters for ENSO instances

        This method defines parameters needed for configuring
        ENSO specific instances; especially those parameters needed for
        ENSO Composite statistics.

        Parameters
        ----------
        plot : Plot
            Plot object
        plot.handle.ENSO_composite_index : string
            time delta in months from composite reference date
        plot.handle.ENSO_composite_label : string
            label describing months before/after reference date

        Notes
        -----
        (1) ENSO composite reference date taken from:
            config['defs/ENSO_composite/ref_date']
            Default: 1980-12-01

        Returns
        -------
        None
            No return value

        """

        handle  = plot.handle
        request = plot.request

        time = request['time_dt']

        # Retrieve central event date for composite

        path = ['defs','ENSO_composite','ref_date']
        refdate = self.config(path, '1980-12-01')
        refdate = dt.strptime(refdate, '%Y-%m-%d')

        # Determine time delta in months from reference date

        diff = relativedelta(time, refdate)
        months = diff.years * 12 + diff.months

        # Set contextual parameters

        if months <= 0:
            label = "{:02d} Months Before Event".format(abs(months))
        else:
            label = "{:02d} Months After Event".format(months)

        handle.ENSO_composite_index = str(months)
        handle.ENSO_composite_label = label
