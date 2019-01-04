#!/usr/bin/env python
import sys
import os
from collections import OrderedDict

import json
import time

def count_log(tex_file='ms.tex', log_file='word_count.csv', verbose=True):
    
    os.system('./texcount.pl -v0 -nosub -nobib {0} > /tmp/texcount.log'.format(tex_file))
    
    if verbose:
        print('{0}\n{1}\n{0}\n'.format(''.join(['=']*50), time.ctime()))
        os.system('cat /tmp/texcount.log')
        
    # Read the log file
    lines = open('/tmp/texcount.log','r').readlines()
    count_dict = OrderedDict()
    
    gmt = time.gmtime()
    iso = '{0}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d}'.format(gmt.tm_year, 
            gmt.tm_mon, gmt.tm_mday, gmt.tm_hour, gmt.tm_min, gmt.tm_sec)
    
    count_dict['time'] = iso
    
    for line in lines:
        if ':' in line:
            spl = line.strip().split(':')
            count_dict[spl[0]] = spl[1].strip()
            
    if os.path.exists(log_file):
        fp = open(log_file,'a')
    else:
        fp = open(log_file,'w')
        header = ', '.join([k.replace(',','') for k in count_dict])
        fp.write(header+'\n')
    
    data = ', '.join(['{0}'.format(count_dict[k]) for k in count_dict])
    fp.write(data+'\n')
    fp.close()

def make_plot(log_file='word_count.csv', plot_file='word_count.png', verbose=True):
    """ 
    Make plot with astropy
    """
    import datetime
    import matplotlib.pyplot as plt
    from matplotlib.dates import (DAILY, YEARLY, WEEKLY, DateFormatter,
                                  rrulewrapper, RRuleLocator, drange)
    
    import numpy as np
    
    from astropy.table import Table
    import astropy.time
        
    tab = Table.read(log_file)
    t = astropy.time.Time(tab['time'])
    last_count = tab['Words in text'].max()
    last_float = tab['Number of floats/tables/figures'].max()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    plt.ioff()
    
    fig = plt.figure(figsize=[8, 4])
    
    # by log
    ax = fig.add_subplot(121)
    ax.plot(tab['Words in text'], label='# Words', color=colors[0], marker='.', alpha=0.5)
    ax.set_ylim(-0.1, np.maximum(last_count,1)*1.2)
    ax.set_xlabel('Log #')
    ax.set_ylabel('Word count')
    
    axf = ax.twinx()
    axf.plot(tab['Number of floats/tables/figures'], label='# Words', color=colors[2], marker='.', alpha=0.5)
    axf.set_ylim(-0.1, np.maximum(last_float,1)*1.1)
    axf.set_yticklabels([])
    
    # By date    
    ax = fig.add_subplot(122)
    ax.plot_date(t.plot_date, tab['Words in text'], label='# Words', color=colors[0], marker='.', alpha=0.5, linestyle='-')
    ax.set_ylim(-0.1, np.maximum(last_count,1)*1.2)
    ax.set_xlabel('Date')
    ax.set_yticklabels([])
    
    axf = ax.twinx()
    axf.plot_date(t.plot_date, tab['Number of floats/tables/figures'], label='# Words', color=colors[2], marker='.', linestyle='-', alpha=0.5)
    axf.set_ylim(-0.1, np.maximum(last_float,1)*1.1)
    axf.set_ylabel('# Floats')
    
    rule = rrulewrapper(DAILY, interval=7)#, byeaster=1, interval=5)
    loc = RRuleLocator(rule)
    formatter = DateFormatter('%d.%m.%y')
    
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    
    limits = ['2019-01-07', '2019-03-01']
    tl = astropy.time.Time(limits)
    ax.set_xlim(tl.plot_date)
    
    # Ticks
    date1 = datetime.date(2019, 1, 7)
    date2 = datetime.date(2019, 3, 1)
    delta = datetime.timedelta(days=7)

    dates = drange(date1, date2, delta)
    ax.set_xticks(dates)
    
    fig.tight_layout(pad=0.1)
    fig.savefig(plot_file)
    
    if verbose:
        print('{0}\n{1} -> {2}\n{0}\n'.format(''.join(['=']*50), log_file, plot_file))
    
    
if __name__ == "__main__":
    
    if '-h' in sys.argv:
        print('Usage: ./texcount.py [ms.tex] [-plot-only] [-log-only]')
        exit()
        
    if len(sys.argv) > 1:
        tex_file = sys.argv[1]
    else:
        tex_file = "ms.tex"
    
    if '-plot-only' not in sys.argv:
        count_log(tex_file, verbose=True)
    
    if '-log-only' not in sys.argv:
        make_plot(verbose=True)
    