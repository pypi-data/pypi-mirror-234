#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2023 Joseph Areeda <joseph.areeda@ligo.org>
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
"""Set of functions to support finding omicron gaps"""

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'

import configparser
import os
import re
import shutil
import subprocess
from datetime import timezone, timedelta
from pathlib import Path
import socket

from astropy.time import Time
from gwpy.segments import Segment, SegmentList, DataQualityFlag
from gwpy.table import EventTable
from gwpy.time import tconvert
from gwtrigfind import find_trigger_files
from LDAStools import frameCPP
from gwdatafind import find_urls

gw_data_find = shutil.which('gw_data_find')
fpat = '^(.+)-(\\d+)-(\\d+).(.+)$'
fmatch = re.compile(fpat)


def filename2segment(path):
    """
    generate a segment from a trigger or frame file with a standard name
    :param path:
    :return:
    """
    _, _, a, b = Path(path).name.split('-')
    start = float(a)
    duration = float(b.split('.')[0])
    return Segment(start, start + duration)


def merge_segs(seg_list):
    """
    Merge any contiguous segments in list
    :param SegmentList seg_list: input list
    :return SegmentList: merged list
    """
    ret = SegmentList()
    n = len(seg_list)
    if n > 0:
        cur_seg = Segment(seg_list[0])
        for i in range(1, n):
            nxt_seg = Segment(seg_list[i])
            if cur_seg.end >= nxt_seg.start:
                cur_seg += nxt_seg
            else:
                ret.append(cur_seg)
                cur_seg = nxt_seg
        ret.append(cur_seg)
    return ret


def find_gaps(config, start, end):
    """
    Use gwtrigfind to locate any gaps in trigger files
    :param ConfigParser config: parsed omicron channel list ini file
    :param LIGOTimeGPS start: start of segment to search
    :param LIGOTimeGPS end: end of segment to search
    :return SegmentList: list of segments wth no gaps
    """
    search_interval = SegmentList([Segment(start, end)])
    chans = config['channels']
    chan = chans.splitlines()[0]
    tseg = find_trig_seg(chan, start, end)
    tseg = search_interval - tseg
    return chan, tseg


def find_trig_seg(chan, start, end):
    """
    Return segments when triggers are available
    :param str chan: channel name real
    :param int start: gps time of the start of search
    :param int end: gs time for end of search
    :return SegmentList: SegmentList of times when triggers are availabl
    """
    search_interval = SegmentList([Segment(start, end)])

    try:
        known_files = find_trigger_files(chan, 'omicron', start, end)
        known_files.sort()
        known_segs = SegmentList(map(filename2segment, known_files)) & search_interval
        known_segs = merge_segs(known_segs)
    except ValueError:
        # no directory for this channel/ETG
        known_segs = SegmentList()
    return known_segs


def find_frame_availability(ifo, frame_type, start, end, logger, datafind_server='ldrslave.ligo.caltech.edu:443'):
    """

    :param ifo:
    :param frame_type:
    :param start:
    :param end:
    :param logger:
    :param datafind_server:
    :return:
    """
    gaps = find_frame_gaps(ifo, frame_type, start, end, logger, datafind_server)
    gaps.label = f'frame: {ifo[0]}_{frame_type}'
    return gaps


def find_frame_gaps(ifo, frame_type, start, end, logger, datafind_server=None):
    """
    Use gw_datafind to report any gaps in frame availability
    :param ifo:
    :param frame_type:
    :param start:
    :param end:
    :param logger:
    :return DataQualityFlag:
    """
    known = SegmentList([Segment(start, end)])
    active = SegmentList([Segment(start, end)])
    if datafind_server is None:
        datafind_server = os.getenv('GWDATAFIND_SERVER')
    if datafind_server is None or len(datafind_server) < 2:
        datafind_server = os.getenv('LIGO_DATAFIND_SERVER')

    cmd = [gw_data_find, '-o', ifo[0], '-t', frame_type, '-s', str(int(start)), '-e', str(int(end)),
           '--gaps', '-r', datafind_server]
    logger.debug(f'getting gaps in frame: {frame_type}\n{" ".join(cmd)}')
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode == 1 or res.returncode == 2:
        stderr = res.stderr.decode('utf-8')
        gotgap = False
        frgaps = SegmentList()
        for line in stderr.splitlines(keepends=False):
            if gotgap:
                m = re.match('(\\d+)\\s+(\\d+)', line)
                if m:
                    frgaps.append(Segment(int(m.group(1)), int(m.group(2))))
            elif re.match('.*Missing segments:', line):
                gotgap = True
        active -= frgaps
    elif res.returncode != 0:
        logger.error(f'gw_data_find fail for frame type {frame_type}, return: {res.returncode}')
        active = SegmentList()
    flgname = f'{ifo[0]}_{frame_type}'
    ret = DataQualityFlag(name=flgname, known=known, active=active, label=flgname)
    return ret

def which_programs(progs):
    """
    Find the external programs needed by these programs
    :param list[str] progs: names of programs to find
    :return (dict, list): paths to programs, NB: keys substitute underscores for any non identifier characters and list
    of any programs not found
    """
    ret = dict()
    not_found = list()

    for prog_name in progs:
        prog_path = shutil.which(prog_name)
        if prog_path is None:
            not_found.append(prog_name)
        else:
            key = re.sub('[^a-zA-Z0-9_.]', '_', prog_name)
            ret[key] = Path(prog_path)
    return ret, not_found


def gps2utc(gps):
    """Convert GPS time to string"""
    gps_time = Time(int(gps), format='gps', scale='utc')
    utc = gps_time.datetime.strftime('%Y-%m-%d %H:%M:%S')
    return utc


def get_gps_day(gps=None, offset=None):
    """
    Return gps times from midnight UTC before arg to after
    :param int offset: number of days from today < 0) past > 0 future
    :param gps: Time in the day of interest, default = today (UTC)
    :return int:  start,end of day
    """
    ingps = gps if gps is not None else int(tconvert())
    ingps += offset * 24 * 3600 if offset is not None else 0
    dt = Time(int(ingps), format='gps', scale='utc').to_datetime(timezone.utc)
    start = int(tconvert(dt.strftime('%Y-%m-%d')))
    end = int(tconvert((dt + timedelta(days=1)).strftime('%Y-%m-%d')))
    return start, end


def gps2dirname(gps):
    """
    use gps time to produce month and day strings
    :param gps: input time
    :return str: YYYYMM, YYYYMMDD
    """
    dt = Time(int(gps), format='gps', scale='utc').to_datetime(timezone.utc)
    day = dt.strftime('%Y%m%d')
    mon = dt.strftime('%Y%m')
    return mon, day


def get_default_ifo():
    # if at a site we have a default ifo
    host = socket.getfqdn()
    if 'ligo-la' in host:
        ifo = 'L1'
    elif 'ligo-wa' in host:
        ifo = 'H1'
    else:
        ifo = os.getenv('IFO')
    return ifo, host


def read_trig_file(infile):
    """
    Determine type of file, decode file name, read triggers
    :param str infile: pathlike pointer to trigger file
    :return: EventTable, channel name, start gps, duration
    """
    inpath = Path(infile)
    if inpath.exists():
        m = fmatch.match(str(inpath.name))
        if m:
            name = m.group(1)
            strt = int(m.group(2))
            dur = int(m.group(3))

            if inpath.name.endswith('.h5'):
                table = EventTable.read(inpath, path='/triggers')
            elif inpath.name.endswith('.xml.gz') or inpath.name.endswith('.xml'):
                try:
                    table = EventTable.read(inpath, tablename='sngl_burst')
                except ValueError as ex:
                    print(ex)
                    raise ex
            elif inpath.name.endswith('.root'):
                # reading root files fail if there is a : in the name
                table = EventTable.read(inpath, treename='triggers;1')
            else:
                raise ValueError(f'Trigger type is unknown {inpath.name}')
        else:
            raise ValueError(f'File not in standard format: {inpath.name}')
    else:
        raise FileNotFoundError(f'{inpath.absolute()} not found.')

    return table, name, strt, dur


def get_default_config(ifo):
    """
    Load the omicron confiuration fie for this ifo
    :param str ifo: Which observatory
    :return ConfigParser: configuration object
    """
    config_file = Path(f'{os.getenv("HOME")}/omicron/online/{ifo[0].lower()}1-channels.ini')
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def seglist_print(out_dir, seg_list, name, append=False, write_h5=False):
    """
    Print a SegmentList to a text file for humans and an hdf5 file for machines
    :param bool write_h5: if true write segments go an hdf5 file as well as text
    :param Path out_dir: directory for files
    :param SegmentList seg_list: segments to print
    :param str name: base name for output files [no exteension]
    :param bool append: if true append to existing file else replace
    :return: None
    """
    if write_h5:
        out_h5 = out_dir / f'{name}.h5'
        if out_h5.exists():
            os.remove(str(out_h5.absolute()))
        seg_list.write(out_h5, path='/segments')

    out_txt = out_dir / f'{name}.txt'
    mode = 'a' if append else 'w'
    with out_txt.open(mode) as out:
        for seg in seg_list:
            duration = seg[1] - seg[0]
            print(f'{seg[0]}, {seg[1]}, {tconvert(seg[0])}, {tconvert(seg[1])}, {sec2hrdur(duration)}', file=out)


def sec2hrdur(dur):
    """
    conver secons to human readable form <days> H:MM:SS
    :param int dur: seconds
    :return str: hr duraation
    """
    td = timedelta(seconds=int(dur))
    return str(td)


def get_chan_list(obs, typ, start, end, logger=None):
    """
    get a list of all channels in this frame
    :param obs:
    :param typ:
    :param start:
    :param end:
    :return:
    """
    ret = list()

    flist = find_urls(obs[0], typ, start, end)
    if len(flist) > 0:
        f = flist[0]
        gwf = re.sub(r'file://localhost', '', f)
        stream = frameCPP.IFrameFStream(str(gwf))
        toc = stream.GetTOC()
        adcList: list = toc.GetADC()
        procList: list = toc.GetProc()
        ret = adcList if len(adcList) > 0 else list()
        if len(procList) > 0:
            ret.extend(procList)
        if logger:
            logger.info(f'We found {len(ret)} in {Path(gwf).name}')
    return ret
