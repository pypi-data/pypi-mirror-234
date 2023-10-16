#!/usr/bin/env python

"""
    mnc = mnc_Py(f_path=[_fileOutput], o_path=True, d_rm=True)
    mnc.compress_files()
    wave_5_without_compress.nc o_path = False -> cmpr_wave_5.nc
                               o_path = True  -> wave_5.nc
                               d_rm   = True  -> rm wave_5_without_compress.nc
                               d_rm   = False -> keep wave_5_without_compress.nc
"""

from __future__ import print_function
import os
import argparse
import xarray as xr
import numpy as np
from christmas.mncPy.common import get_file_paths, GlobalData

# pylint: disable=line-too-long, bad-whitespace, len-as-condition, invalid-name


def parse_args():
    # Parse the CLI arguments provided by the user
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', metavar='path', type=str, required=True, nargs='*',
                        help='path to hist file(s) to read. Multiple files and wild characters (*) accepted.')
    parser.add_argument('-x', metavar='excl', type=str, required=False,
                        help='(optional). File names that have the string provided after this flag'
                             ' will be discarded. ')
    return parser.parse_args()


class mnc_Py:
    def __init__(self, f_path, x_excl=None, o_path=False, d_rm=False):
        self.f = f_path
        self.x = x_excl
        self.o = o_path
        self.d = d_rm

    def compress_files(self):
        # sourcery skip: de-morgan, flip-comparison, for-append-to-extend, list-comprehension, low-code-quality, remove-redundant-slice-index, remove-str-from-fstring, use-fstring-for-concatenation
        """ compresses a given set of netcdf files """

        # get the list of files to compress
        filePaths = get_file_paths(self.f, self.x)
    
        # by default, exclude files that are already compressed by this script
        filePaths = [filePath for filePath in filePaths if len(filePath.name)>5 and "_without_compress"==filePath.name[-20:-3]]
    
        # determine files to be compressed by each proc
        nfiles = len(filePaths)
        lfiles = []
        for i in range(nfiles):
            lfiles.append(filePaths[i])

        #  compress the files:
        compr_dict = dict(zlib=True, complevel=1)
        compr_dict['_FillValue'] = None
        for lfile in lfiles:
    
            path_in = os.path.join(lfile.base, lfile.name)
            if self.o:
                path_out = os.path.join(lfile.base, lfile.name[:-20] + ".nc")
            else:
                path_out = os.path.join(lfile.base, "cmpr_" + lfile.name[:-20] + ".nc")
            write_mode = 'w'

            # get time dimension
            glob = GlobalData()
            glob.get_time_var_names(path_in, bound_required=False)
    
            # first, write the the coordinates
            with xr.open_dataset(path_in, decode_times=False, cache=False, decode_cf=False) as lfile_ds_in:
                with xr.Dataset(coords=lfile_ds_in.coords, attrs=lfile_ds_in.attrs) as lfile_ds_out:
                    var_list = lfile_ds_in.variables
                    if len(lfile_ds_in.coords)>0:
                        for var in lfile_ds_in.coords:
                            lfile_ds_out[var] = lfile_ds_in[var]
    
                        encoding_dict = {var: compr_dict for var in lfile_ds_in.coords}
                        lfile_ds_out.to_netcdf(path=path_out, mode=write_mode, unlimited_dims=[glob.time_str], encoding=encoding_dict)
                        write_mode = 'a'
    
            # now, write the remaining data arrays (one by one to eliminate memory limitation)
            for da in var_list:
                with xr.open_dataset(path_in, decode_times=False, cache=False, decode_cf=False) as lfile_ds_in:
                    with xr.Dataset(coords=lfile_ds_in.coords, attrs=lfile_ds_in.attrs) as lfile_ds_out:
                        if not da in lfile_ds_in.coords:
                            lfile_ds_out[da] = lfile_ds_in[da]
                            lfile_ds_out.to_netcdf(path=path_out, mode=write_mode, unlimited_dims=[glob.time_str], encoding={da: compr_dict})
                            write_mode = 'a'
            if self.d:
                os.remove(path_in)


if __name__ == "__main__":
    args = parse_args()
    mnc = mnc_Py(args.f, args.x)
    mnc.compress_files()
