#  Copyright (C) 2020 SuperDARN Canada, University of Saskatchewan
#  Author: Cooper Ross Robertson, Summer Student 2020, Marina Schmidt
import copy
import matplotlib.pyplot as plt
import numpy as np

from typing import List

from pydarn import SuperDARNRadars, exceptions, RTP


class Power():
    """
    Power class to plot SuperDARN RAWACF data power related.


    Methods
    -------
    plot_pwr0_statistic()
    """
    def _str_(self):

        return "This class provides the following methods: \n"\
                " - plot_interference()"

    @classmethod
    def plot_pwr0_statistic(cls, records: List[dict], beam_num: int = 0,
                            compare: bool = True, min_frequency: float = None,
                            max_frequency: float = None,
                            split_frequency: float = None,
                            statistical_method: object = np.mean):

        """
        This function will calculate and plot a statistic of the lag-0
        power of each record as a function of time.

        This function applies the statistical function (ex. numpy.mean)
        to the pwr0 vector (lag-0 power for each range) for each record
        before plotting the results from all records chronologically.

        Notes
        -----
        This code can be used to study background interference in rawacf data
        when the radar has been operating in a receive-only mode such as
        "politescan" (cpid -3380), or during periods without any obvious
        coherent scatter returns from any range.

        If you wish to compare the background interference associated with two
        different frequencies then let compare=true. The frequencies will be
        organized by the 'frequency' input. For example, if politescan ran
        with 10.3 and 12.2 MHz then you could let 'frequency' equal 11000.
        All records with tfreq below 11000 will be separated from those records
        with tfreq above 11000. If compare = False then frequency is simply
        the frequency that politescan ran with i.e 12.2 MHz exclusively.

        Future Work
        -----------
        Allow for multi-beam comparison to get a directional
        sense of the interference


        Parameters
        ----------
        records: List[dict]
        beam_num: int
            The beam number with the desired data to plot
        compare: bool
            determines if a single frequency is use in plotting pwr0
            (compare=False) or two frequencies between a frequency
            (compare=True)
            default: False
        min_frequency: float
            set a minimum frequency boundary to plot
            default: None
        max_frequency: float
            set a maximum frequency boundary to plot
            default: None
        split_frequency: float
            frequency to specifically look for or split between depending
            on the setting of compare.
            default: None
        statistical_method: numpy object
            numpy statistical calculation or generic min or max functions
            e.g. numpy.std, numpy.median, numpy.min, numpy.max
            default: numpy.mean

        Raise
        -----
        NoDataFound
        """
        if split_frequency is None:
            if min_frequency is None and max_frequency is None:
                # Plot all frequencies
                records_of_interest = cls.__apply_stat2pwr0(records,
                                                            statistical_method,
                                                            beam_num)
                cls.__plot_pwr0(records_of_interest, beam_num,
                                statistical_method)
            else:
                # plot all frequencies lower than max_frequency
                if min_frequency is None:
                    records_of_interest = cls.\
                            __apply_stat2pwr0(records, statistical_method,
                                              beam_num, '<', max_frequency)
                    cls.__plot_pwr0(records_of_interest, beam_num,
                                    statistical_method)

                elif max_frequency is None:
                    # plot all frequencies higher than min_frequency
                    records_of_interest = cls.\
                            __apply_stat2pwr0(records, statistical_method,
                                              beam_num, '>', min_frequency)
                    cls.__plot_pwr0(records_of_interest, beam_num,
                                    statistical_method)

                else:
                    # plot all frequencies between min and max frequency
                    records_of_interest = cls.\
                        __apply_stat2pwr0(records, statistical_method,
                                          beam_num, '>', min_frequency)
                    records_of_interest = cls.\
                        __apply_stat2pwr0(records_of_interest,
                                          statistical_method,
                                          beam_num, '<', max_frequency)

                    cls.__plot_pwr0(records_of_interest, beam_num,
                                    statistical_method)
        else:
            if compare:
                if min_frequency is None and max_frequency is None:
                    # Plot high and low frequencies
                    low_frequency_records = cls.\
                        __apply_stat2pwr0(records, statistical_method,
                                          beam_num, '<', split_frequency)
                    high_frequency_records = cls.\
                        __apply_stat2pwr0(records, statistical_method,
                                          beam_num, '>', split_frequency)
                    plt.subplot(2, 1, 1)
                    cls.__plot_pwr0(low_frequency_records, beam_num,
                                    statistical_method)
                    plt.xticks([])
                    plt.subplot(2, 1, 2)
                    cls.__plot_pwr0(high_frequency_records, beam_num,
                                    statistical_method, False)

                else:
                    # plot all frequencies lower than
                    # split_frequency and plot all frequencies between
                    # split_frequency and max_frequency
                    if min_frequency is None:
                        records_of_interest = cls.\
                            __apply_stat2pwr0(records, statistical_method,
                                              beam_num, '<', max_frequency)
                        low_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '<', split_frequency)
                        high_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '>', split_frequency)
                        plt.subplot(2, 1, 1)
                        cls.__plot_pwr0(low_frequency_records, beam_num,
                                        statistical_method)
                        plt.xticks([])
                        plt.subplot(2, 1, 2)
                        cls.__plot_pwr0(high_frequency_records, beam_num,
                                        statistical_method, False)

                    elif max_frequency is None:
                        # plot all frequencies between min_frequency and
                        # split_frequency and plot all frequencies higher than
                        # split_frequency
                        records_of_interest = cls.\
                            __apply_stat2pwr0(records, statistical_method,
                                              beam_num, '>', min_frequency)
                        low_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '<', split_frequency)
                        high_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '>', split_frequency)
                        plt.subplot(2, 1, 1)
                        cls.__plot_pwr0(low_frequency_records, beam_num,
                                        statistical_method)
                        plt.xticks([])
                        plt.subplot(2, 1, 2)
                        cls.__plot_pwr0(high_frequency_records, beam_num,
                                        statistical_method, False)

                    else:
                        # plot all low and high frequencies between
                        # min and max frequency
                        records_of_interest = cls.\
                            __apply_stat2pwr0(records, statistical_method,
                                              beam_num, '>', min_frequency)
                        records_of_interest = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '<', max_frequency)

                        low_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '<', split_frequency)
                        high_frequency_records = cls.\
                            __apply_stat2pwr0(records_of_interest,
                                              statistical_method,
                                              beam_num, '>', split_frequency)
                        plt.subplot(2, 1, 1)
                        cls.__plot_pwr0(low_frequency_records, beam_num,
                                        statistical_method)
                        plt.xticks([])
                        plt.subplot(2, 1, 2)
                        cls.__plot_pwr0(high_frequency_records, beam_num,
                                        statistical_method, False)

            else:
                # plot the single frequency
                records_of_interest = cls.\
                        __apply_stat2pwr0(records, statistical_method,
                                          beam_num, '==', split_frequency)
                cls.__plot_pwr0(records_of_interest, beam_num,
                                statistical_method)

    @staticmethod
    def __plot_pwr0(records: list, beam_num: int, statistical_calc: object,
                    title: bool = True):
            stid = records[0]['stid']
            radar_abbrev = SuperDARNRadars.radars[stid].hardware_info.abbrev
            RTP.plot_time_series(records, parameter='pwr0', beam_num=beam_num)
            plt.ylabel("{} Power\n [raw units]"
                       "".format(statistical_calc.__name__.capitalize()))
            plt.legend(["{} kHz".format(records[0]['tfreq'])])
            if title:
                plt.title(' Lag 0 Power for {} Beam: {} '.format(radar_abbrev,
                                                                 beam_num))

    @staticmethod
    def __apply_stat2pwr0(records: list, stat_method: object, beam_num: int,
                          operand: str = '', frequency: float = None):

        records_of_interest = copy.deepcopy(records)

        if operand is '>':
            records_of_interest = [record for record in records
                                   if record['tfreq'] > frequency]
        elif operand is '<':
            records_of_interest = [record for record in records
                                   if record['tfreq'] < frequency]
        elif operand is '==':
            records_of_interest = [record for record in records
                                   if record['tfreq'] == frequency]

        if len(records_of_interest) == 0:
            raise exceptions.plot_exceptions.\
                  NoDataFoundError('tfreq', beam_num,
                                   opt_beam_num=records[0]['bmnum'],
                                   opt_parameter_value=records[0]['tfreq'])

        for record in records_of_interest:
            stat_pwr = stat_method(record['pwr0'])
            record.update({'pwr0': stat_pwr})

        return records_of_interest
