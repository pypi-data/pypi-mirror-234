#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2022 Joseph Areeda <joseph.areeda@ligo.org>
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

"""Compares detector state, frame availability and trigger availability to
find time intervals we may be able to fill by running pyomicron"""
import time
from logging.handlers import RotatingFileHandler

from omicron_gap.gap_handler import gps2str

start_time = time.time()

import datetime
import shutil
import subprocess
from math import ceil
from pathlib import Path
from socket import gethostname
from gwpy.segments import (DataQualityFlag, Segment, SegmentList)

from gwpy.time import to_gps, tconvert
from .gap_utils import find_gaps, find_frame_gaps
import argparse
import configparser
import logging
import os
import matplotlib
from ._version import __version__


__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'find-gaps'

DEFAULT_SEGMENT_SERVER = os.environ.setdefault('DEFAULT_SEGMENT_SERVER', 'https://segments.ligo.org')
matplotlib.use('agg')

gw_data_find = shutil.which('gw_data_find')


def main():
    log_file_format = "%(asctime)s - %(levelname)s - %(funcName)s %(lineno)d: %(message)s"
    log_file_date_format = '%m-%d %H:%M:%S'
    logging.basicConfig(format=log_file_format, datefmt=log_file_date_format)
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    host = gethostname()
    if 'ligo-la' in host:
        ifo = 'L1'
    elif 'ligo-wa' in host:
        ifo = 'H1'
    else:
        ifo = None

    now = tconvert()

    parser = argparse.ArgumentParser(description=__doc__,
                                     prog=__process_name__)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-i', '--ifo', help='Specify which ifo to search, [%(default)s]', default=ifo)
    parser.add_argument('-g', '--groups', default='all', nargs='+',
                        help='Omicron groups to process, [%(default)s]')
    parser.add_argument('-o', '--output-dir', type=Path, help='Path to directory for command files')
    parser.add_argument('-f', '--config-file', type=Path, required=True,
                        help='Omicron config file')
    parser.add_argument('--condor-accounting-group-user', help='user to use for condor')
    parser.add_argument('-l', '--log-file', type=Path, help='Save log messages to this file')
    parser.add_argument('start', type=to_gps, default=now - 7 * 86400, nargs='?',
                        help='gps time or date/time to start looking for gaps [%(default)s] (7 days ago)')
    parser.add_argument('end', type=to_gps, help='end of interval [%(default)s] (now)',
                        nargs='?', default=now)
    parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                        help='Print commands but do not execute them')
    parser.add_argument('-n', '--njobs', type=int, default=8, help='Number of scripts to create, max = 100')
    parser.add_argument('--min-gap', type=int, default=128, help='Minimum length of a gap to processs [%(default)i]')
    parser.add_argument('--max-gap', type=int, default=3600,
                        help='Maximumlength of a gap to processs in each DAG [%(default)i]')

    args = parser.parse_args()

    verbosity = 0 if args.quiet else args.verbose
    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
        passon_verb = '--quiet'
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
        passon_verb = '-v'
    else:
        logger.setLevel(logging.DEBUG)
        passon_verb = '-vvv'

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

    for k, v in vars(args).items():
        if k == 'start' or k == 'end':
            s = f', ({tconvert(v)})'
        else:
            s = ''
        logger.debug(f'arg: {k} = {v}{s}')

    home = os.getenv('HOME')

    x509 = Path(home) / '.private' / 'x509p.pem'
    x509_str = os.getenv('X509_USER_PROXY')
    x509 = Path(x509_str) if x509_str is not None and len(x509_str) > 2 else x509
    if x509.exists():
        os.putenv('X509_USER_PROXY', str(x509.absolute()))
        logger.debug(f'Set environment X509_USER_PROXY={str(x509.absolute())}')
    else:
        logger.error(f'x509 not found at {str(x509.absolute())}')

    res = subprocess.run(['ecp-cert-info'], capture_output=True)
    stdout = res.stdout.decode('utf-8')
    stderr = res.stderr.decode('utf-8')
    logger.debug(f'ecp-cert-info returned {res.returncode}\n{stdout}\n{stderr}')
    njobs = min(args.njobs, 100)
    start = int(args.start)
    end = int(args.end)
    ifo = args.ifo

    ourfile = Path(__file__)
    logger.debug(f'runninng {str(ourfile.absolute())} version: {__version__}')
    omicron_run = shutil.which('omicron_run.sh')
    python_prog = shutil.which('python')
    groups = args.groups
    allgrp = ["GW", "STD1", "STD2", "LOW1", "STD3", "LOW2", "STD4",
              "PEM1", "PEM2", "PEM3", "PEM4", "PEM5", "LOW3"]
    if 'all' in groups:
        groups = allgrp

    output_dir = Path(args.output_dir)
    output_dir.mkdir(mode=0o775, exist_ok=True)
    outscripts = list()
    outidx = 0
    ngaps = 0
    config = configparser.ConfigParser()
    config_file = Path(args.config_file)
    config.read(config_file)

    for group in groups:
        chan, gaps = find_gaps(config[group], start, end)

        frames = find_frame_gaps(args.ifo, config[group]['frametype'], start, end, logger)
        plot = frames.plot(figsize=(12, 8))
        ax = plot.gca()
        if 'state-flag' in config[group].keys():
            logger.debug(f'Get DQ flag {config[group]["state-flag"]}, {start}, {end}, url={DEFAULT_SEGMENT_SERVER}')
            os.unsetenv('HTTPS_PROXY')
            state = DataQualityFlag.query_dqsegdb(config[group]['state-flag'], start, end, url=DEFAULT_SEGMENT_SERVER)
        else:
            state = frames
            state.name = 'state=all'
            state.label = 'state=all'
        ax.plot(state)

        gap_known = SegmentList([Segment(start, end)])
        gap_active = SegmentList([Segment(start, end)])
        proc_segs = SegmentList()
        gapset = set()
        for gap in gaps:
            gseg = Segment(int(gap[0]), int(gap[1]))
            if gseg in gapset:
                continue
            gapset.add(gseg)
            qsegl = SegmentList([gseg])
            psegl = qsegl & frames.active & state.active
            if len(psegl) == 0:
                continue
            proc_segs.extend(psegl)
            gap_active -= qsegl
        proc_segs.sort()
        proc_segs2 = SegmentList()
        maxg = args.max_gap
        for gap in proc_segs:
            tgap = Segment(gap)
            dt = tgap.end - tgap.start
            if dt >= args.min_gap:
                while dt > maxg * 2:
                    t1 = Segment(tgap.start, tgap.start + maxg)
                    proc_segs2.append(t1)
                    tgap = Segment(tgap.start + maxg, tgap.end)
                    dt = tgap.end - tgap.start
                if dt > 0 and dt > maxg:
                    t1 = Segment(tgap.start, tgap.start + dt / 2)
                    proc_segs2.append(t1)
                    tgap = Segment(tgap.start + dt / 2, tgap.end)
                    proc_segs2.append(tgap)
                elif dt > 0:
                    proc_segs2.append(tgap)

        for gap in proc_segs2:
            dt = gap[1] - gap[0]
            if dt >= args.min_gap:
                ngaps += 1
                if len(outscripts) <= outidx:
                    new_script = output_dir / f'fillgap-{outidx:02d}.sh'
                    outscripts.append(open(new_script, 'w'))
                    logger.debug(f'Created script {new_script.name}')
                sstr = tconvert(int(gap[0]))
                estr = tconvert(ceil(gap[1]))
                dstr = str(datetime.timedelta(seconds=gap[1] - gap[0]))
                pyomicrondir = output_dir / f'{group}-{gps2str(int(gap[0]))}-{gps2str(int(gap[1]))}'
                print(f'# gap from {sstr} to {estr}. {dstr}', file=outscripts[outidx])
                pyomicron_cmd = f'{omicron_run} {python_prog} -m omicron.cli.process {passon_verb} ' \
                                f'--gps {int(gap[0]):d} {int(gap[1]):d} ' \
                                f'--output-dir {pyomicrondir} --config-file {str(config_file.absolute())} ' \
                                f'--no-submit --submit-rescue-dag 1 --archive --ifo {ifo} {group} '
                if args.condor_accounting_group_user:
                    pyomicron_cmd += f' --condor-accounting-group-user {args.condor_accounting_group_user}'
                print(pyomicron_cmd, file=outscripts[outidx])
                outidx = (outidx + 1) % njobs

        gname = f'{chan}.h5'
        gap_flag = DataQualityFlag(name=gname, known=gap_known, active=gap_active, label=gname)
        ax.plot(gap_flag)

        prcnam = 'Segs to be processed'
        prcflag = DataQualityFlag(name=prcnam, known=gap_known, active=proc_segs, label=prcnam)
        ax.plot(prcflag)
        plot_name = output_dir / f'gap-plot-{group}.png'
        ax.xaxis.grid(True, color='b', linestyle='-', linewidth=0.8)
        plot.suptitle(f'Gap summary {group}', fontsize=18)
        ax.set_title(f'{len(gaps)} gaps found, {len(proc_segs)}')
        plot.savefig(plot_name, edgecolor='white', dpi=100, bbox_inches='tight')
        logger.info(f'Wrote gap plot to {str(plot_name)}')
    for fp in outscripts:
        fp.close()

    elap = time.time() - start_time
    logger.info(f'{ngaps} gaps found run time {elap:.1f} s')


if __name__ == "__main__":
    main()
