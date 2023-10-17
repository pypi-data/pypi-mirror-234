#!/usr/bin/env python
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2019 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Plot availability of some representative data used by detchar tasks"""
import configparser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from matplotlib import use
import time
start_time = time.time()

import os
import sys

# if launched from a terminal with no display
# Must be done before modules like pyplot are imported
if len(os.getenv('DISPLAY', '')) == 0:
    use('Agg')  # nopep8


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'omicron-plot-gaps'

import argparse
import logging
from gwpy.time import to_gps, tconvert  # noqa: E402
from ._version import __version__

from gwpy.segments import DataQualityFlag, Segment, SegmentList  # noqa: E402
from gwpy.plot.segments import SegmentAxes
from .gap_utils import gps2utc, find_frame_availability, find_trig_seg, \
    get_default_ifo, get_gps_day, gps2dirname  # noqa: E402
import matplotlib   # noqa: E402
from gwpy.plot import Plot

ifo, host = get_default_ifo()
home = os.getenv('HOME')

std_segments = \
    [
        '{ifo}:DMT-GRD_ISC_LOCK_NOMINAL:1',
        '{ifo}:DMT-DC_READOUT_LOCKED:1',
        '{ifo}:DMT-CALIBRATED:1',
        '{ifo}:DMT-ANALYSIS_READY:1'
    ]
master_seg = '{ifo}:DMT-ANALYSIS_READY:1'

# std_trig_channels = \
#     [
#         ('{ifo}:GDS-CALIB_STRAIN', 'GW'),
#
#         ('{ifo}:ASC-INP2_Y_OUT_DQ', 'LOW1'),
#         ('{ifo}:ISI-BS_ST1_BLND_RY_T240_CUR_IN1_DQ', 'LOW2'),
#         ('{ifo}:SQZ-ASC_ANG_Y_OUT_DQ', 'LOW3'),
#
#         ('{ifo}:CAL-DELTAL_EXTERNAL_DQ', 'STD1'),
#         ('{ifo}:LSC-POP_A_RF45_I_ERR_DQ', 'STD2'),
#         ('{ifo}:HPI-HAM1_BLND_L4C_RX_IN1_DQ', 'STD3'),
#         ('{ifo}:ISI-BS_ST2_BLND_RY_GS13_CUR_IN1_DQ', 'STD4'),
#
#         ('{ifo}:ISI-GND_STS_HAM5_Y_DQ', 'PEM1'),
#         ('{ifo}:PEM-CS_ACC_BEAMTUBE_YMAN_X_DQ', 'PEM2'),
#         ('{ifo}:PEM-CS_VMON_ITMY_ESDPOWER18_DQ', 'PEM4'),
#         ('{ifo}:PEM-CS_MIC_LVEA_BS_DQ', 'PEM5'),
#     ]

std_frames = \
    {
        '{ifo}_HOFT_C00',
        '{ifo}_DMT_C00',
        '{ifo}_R',
        '{ifo}_M',
        '{ifo}_T',
        'SenseMonitor_Nolines_{ifo}_M',
        'SenseMonitor_CAL_{ifo}_M'
    }

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
matplotlib.use('agg')
datafind_servers = {'L1': 'LIGO_DATAFIND_SERVER=ldrslave.ligo-la.caltech.edu:443',
                    'H1': 'LIGO_DATAFIND_SERVER=ldrslave.ligo-wa.caltech.edu:443'}
if ifo is not None:
    default_datafind_server = datafind_servers[ifo]
else:
    default_datafind_server = os.environ.setdefault('GWDATAFIND_SERVER', 'ldrslave.ligo.caltech.edu:443')

global plot
plot: matplotlib.figure = None
axes = None
nribbons = 0


def plot_seg(seg_data, axnum):
    """
    Add a ribbon for a DataQualityFlag
    :param DataQualityFlag seg_data:
    :return:
    """
    global plot, ax, nribbons, ifo

    if plot is None:
        plot = Plot()
        if ifo is None:
            nsubplots = 4
            hratios = [1, 1, 1, 1]
        else:
            nsubplots = 3
            hratios = [1, 1, 3]

        ax = plot.subplots(nsubplots, 1, sharex='col', subplot_kw={"axes_class": SegmentAxes},
                           gridspec_kw={'height_ratios': hratios[0:nsubplots]})

    ax[axnum].plot(seg_data)

    nribbons += 1


def seg_dump(txt, segs, label):
    """
    Write segments to text file
    :param txt: file pointer to file open for writing
    :param dict segs: containing segment lists
    :param str label:
    :return:
    """
    print(f'{label} segments\n=================', file=txt)
    for seg_name, seg_data in segs.items():
        print(f'    {seg_name}:', file=txt)
        active_total = 0
        for seg in seg_data.active:
            seg_dur = seg.end - seg.start
            active_total = active_total + int(seg_dur)
            seg_dur_hr = int(seg_dur) / 3600.
            print(f'  {int(seg.start)} {int(seg.end)}    # ({int(seg_dur)} sec, {seg_dur_hr:.1f} hrs) '
                  f'{gps2utc(seg.start)} {gps2utc(seg.end)}', file=txt)
        print(f'---Total active time for {seg_name} {active_total} seconds, {active_total / 3600.:.1f} hrs\n',
              file=txt)


def main():
    global plot, ax, nribbons, ifo

    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    start_time = time.time()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    parser.add_argument('start', type=to_gps, action='store', nargs='?', help='Start of plot')
    parser.add_argument('end', type=to_gps, action='store', nargs='?', help='End of plot, default start + 24 hrs')
    parser.add_argument('--yesterday', action='store_true', help='set times to 24 hours covering yesterday')
    parser.add_argument('-E', '--epoch', type=float, action='store',
                        help='Delta < 10000000 or GPS', required=False)
    parser.add_argument('-i', '--ifo', type=str, default=ifo,
                        help='IFO (L1, H1, V1)')
    parser.add_argument('-l', '--log-file', type=Path, help='Save log messages to this file')
    parser.add_argument('-o', '--out', help='Base path to results: txt and png files. Default is '
                                            'a directory in ~/public_html/detchar-avail based on month and day')
    parser.add_argument('-t', '--text', action='store_true', help='Save a text file of all data plotted')

    parser.add_argument('--std', action='store_true', help='Add "standard" segment list')
    parser.add_argument('-S', '--segments', type=str, nargs='*',
                        help='List of segments to examine with "{ifo}" ',
                        default=' '.join(std_segments))
    parser.add_argument('-g', '--geometry', help='Width x Height')
    parser.add_argument('-c', '--config', type=Path, help='omicron config default is to look in ~/omicron/online')
    args = parser.parse_args()

    verbosity = args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    if args.log_file:
        log_file = Path(args.log_file)
        if not log_file.parent.exists():
            log_file.parent.mkdir(mode=0o775, parents=True)
        log_formatter = logging.Formatter(fmt=log_file_format,
                                          datefmt=log_file_date_format)
        log_file_handler = RotatingFileHandler(args.log_file, maxBytes=10 ** 7,
                                               backupCount=5)
        log_file_handler.setFormatter(log_formatter)
        logger.addHandler(log_file_handler)
        logger.info('Find gaps started')

    # debugging?
    logger.debug('{} called with arguments:'.format(__process_name__))
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    ifo = args.ifo
    datafind_server = os.getenv('GWDATAFIND_SERVER')
    datafind_server = default_datafind_server if datafind_server is None else datafind_server
    now_gps = int(tconvert())
    if args.start:
        start = int(args.start)
        if args.end:
            end = int(args.end)
        else:
            end = start + 24 * 3600
    elif args.yesterday:
        start, end = get_gps_day(offset=-1)
    else:
        start, end = get_gps_day()

    last_known = SegmentList([Segment(min(now_gps, end), end)])

    mon, day = gps2dirname(start)

    if args.out:
        plot_file = Path(args.out)
        if plot_file.is_dir():
            plot_file /= day
    else:
        plot_file = Path.home() / 'public_html' / 'detchar-avail' / mon / day
    plot_file.parent.mkdir(mode=0o775, parents=True, exist_ok=True)
    ext = plot_file.suffix
    if ext:
        plot_base = str(plot_file)[0:-len(ext)]
    else:
        plot_base = str(plot_file)
    plot_file = Path(plot_base + '.png')
    txt_file = Path(plot_base + '.txt')

    segments = list()
    if args.std or not args.segments:
        segments.extend(std_segments)

    if args.segments:
        segments += args.segments.split(' ')

    config = None
    conf_file = None
    if args.config:
        conf_file = Path(args.config)
    elif ifo is not None:
        conf_file = Path(f'{home}') / 'omicron' / 'online' / f'{ifo.lower()}-channels.ini'
    if conf_file is None or not conf_file.exists():
        logger.critical('Could not find the config file ')
    else:
        logger.info(f'Config file: {str(conf_file.absolute())}')
        config = configparser.ConfigParser()
        config.read(conf_file)

    frame_types = dict()

    # space command line frame types
    ifos = [ifo] if ifo is not None else ['L1', 'H1']
    for f in std_frames:
        for i in ifos:
            frame_type = f.replace('{ifo}', i)
            if i not in frame_types.keys():
                frame_types[i] = list()
            frame_types[i].append(frame_type)

    frame_segs = dict()
    axnum = -1
    for this_ifo, frlist in frame_types.items():
        frlist.sort()
        axnum += 1
        for fram in frlist:
            fr_avail = find_frame_availability(this_ifo, fram, start, end, logger, datafind_server)
            fr_avail.known -= last_known
            frame_segs[fram] = fr_avail
            plot_seg(fr_avail, axnum)

    trigger_segs = dict()

    dq_segs = dict()
    for i in ifos:
        dq_segs[i] = set()
        for segment in segments:
            seg_name = segment.replace('{ifo}', i)
            dq_segs[i].add(seg_name)

        logger.info(f'{len(dq_segs[i])} segs: {", ".join(dq_segs[i])}')
    logger.info(f'from {start} ({tconvert(start)}, to {end} ({tconvert(end)}')
    dqsegs = dict()

    for i in ifos:
        axnum += 1
        for seg_name in sorted(dq_segs[i]):
            try:
                qstrt = time.time()
                seg_data = DataQualityFlag. \
                    query_dqsegdb(seg_name, start, end,
                                  url='https://segments.ligo.org')
                logger.info(f'Segment query for {seg_name} {len(seg_data.known)} known {len(seg_data.active)} '
                            f'active. Query took {int(time.time()-qstrt)} seconds')
            except ValueError:
                qstrt = time.time()
                seg_data = DataQualityFlag. \
                    query_dqsegdb(seg_name, start, end,
                                  url='https://segments-backup.ligo.org/')
                logger.info(f'Backup query for {seg_name} took {int(time.time()-qstrt)} seconds')

            if len(seg_data.known) > 0:
                if not seg_data.isgood:
                    seg_data = ~seg_data
                seg_data.label = f'DQ seg: {seg_name}'
                dqsegs[seg_name] = seg_data
                plot_seg(seg_data, axnum)

    if ifo is not None and config is not None:
        axnum += 1
        groups = config.sections()
        groups.sort()
        for trig_group in groups:
            allchans = config[trig_group]['channels'].split('\n')
            trig_chan = allchans[0]

            active = find_trig_seg(trig_chan, start, end)
            known = SegmentList([Segment(start, end)]) - last_known
            trig_flag = DataQualityFlag(name=trig_chan, known=known, active=active,
                                        label=f'trig({trig_group}): {trig_chan} ({len(allchans)})')
            plot_seg(trig_flag, 2)
            trigger_segs[trig_chan] = trig_flag

    axis_titles = list()
    for i in ifos:
        axis_titles.append(f'{i}: Frame availability. Green -> datafind succeeded')
    for i in ifos:
        axis_titles.append(f'{i}: DQ segments. Green -> active segments, red -> known but not active, '
                           'gap -> no segments available')
    for i in ifos:
        axis_titles.append(f'{i}: Omicron triggers, one per (group). Green -> gwtrigfind succeeded')

    if plot is not None:
        n = 0
        for axis in ax:
            axis.xaxis.grid(True, color='b', linestyle='-', linewidth=0.8)
            axis.set_xlim(start, end)
            axis.set_title(axis_titles[n])
            n = n + 1

            if args.epoch:
                epoch = start
                if args.epoch <= 10000000:
                    epoch += args.epoch
                else:
                    epoch = args.epoch
                axis.set_epoch(epoch)
            strt_str = tconvert(start).strftime('%Y-%m-%d %H:%M')
            end_str = tconvert(end).strftime('%Y-%m-%d %H:%M')
            now_str = tconvert(now_gps).strftime('%Y-%m-%d %H:%M')
        loc = 'CIT' if ifo is None else 'LLO' if ifo == 'L1' else 'LHO'
        plot.suptitle(f'Detchar data availability at {loc}. {strt_str} to {end_str} at {now_str}', fontsize=18)

        height = nribbons * 0.5 + 1.20
        minhgt = 3.0
        logger.info(f'nribbons: {nribbons}, calculated height: {height:.2f}, min: {minhgt:.2f}')
        height = max(height, minhgt)

        plot.set_figwidth(18)
        plot.set_figheight(height)
        plot.savefig(plot_file, edgecolor='white', bbox_inches='tight')
        logger.info(f'Wrote plot to {plot_file}')
    else:
        logger.critical('None of the segment(s) were known during the requested times')
        sys.exit(2)

    if args.text:
        with txt_file.open('w') as txt:
            seg_dump(txt, dqsegs, 'Data Quality')
            print('', file=txt)
            seg_dump(txt, frame_segs, 'Frame')
            print('', file=txt)
            seg_dump(txt, trigger_segs, 'Omicron triggers')
            print('', file=txt)

        logger.info(f'Text summary of segments written to {str(txt_file.absolute())}')

    logger.info('Runtime: {:.1f} seconds'.format(time.time() - start_time))


if __name__ == "__main__":
    main()
