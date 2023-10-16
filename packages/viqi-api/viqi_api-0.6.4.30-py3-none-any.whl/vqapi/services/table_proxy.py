###############################################################################
##  ViQi BisQue                                                              ##
##  ViQi Inc                                                                 ##
## ------------------------------------------------------------------------- ##
##                                                                           ##
##     Copyright (c) 2007-2023                                               ##
##     by the ViQI Inc                                                       ##
##                            All rights reserved                            ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##                                                                           ##
##     1. Redistributions of source code must retain the above copyright     ##
##        notice, this list of conditions, and the following disclaimer.     ##
##                                                                           ##
##     2. Redistributions in binary form must reproduce the above copyright  ##
##        notice, this list of conditions, and the following disclaimer in   ##
##        the documentation and/or other materials provided with the         ##
##        distribution.                                                      ##
##                                                                           ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY         ##
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE         ##
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR        ##
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR           ##
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,     ##
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,       ##
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR        ##
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ##
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        ##
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              ##
##                                                                           ##
## The views and conclusions contained in the software and documentation     ##
## are those of the authors and should not be interpreted as representing    ##
## official policies, either expressed or implied, of <copyright holder>.    ##
###############################################################################
"""
SYNOPSIS
========


DESCRIPTION
===========

"""
import json
import logging
import os
import posixpath
import shutil
import tempfile

import numpy as np
import pandas as pd
import tables
from bq.metadoc.formats import Metadoc

from vqapi.exception import BQApiError

from .base_proxy import FuturizedServiceProxy

# from botocore.credentials import RefreshableCredentials
# from botocore.session import get_session


log = logging.getLogger("vqapi.services")


class TableProxy(FuturizedServiceProxy):
    service_name = "table"

    def load_array(self, table_uniq, path, slices=None, want_info=False):
        """
        Load array from BisQue.
        """
        slices = slices or []
        if table_uniq.startswith("http"):
            table_uniq = table_uniq.split("/")[-1]
        slice_list = []
        for single_slice in slices:
            if isinstance(single_slice, slice):
                slice_list.append(
                    "{};{}".format(
                        single_slice.start or "",
                        "" if single_slice.stop is None else single_slice.stop - 1,
                    )
                )
            elif isinstance(single_slice, int):
                slice_list.append(f"{single_slice};{single_slice}")
            else:
                raise BQApiError("malformed slice parameter")
        path = "/".join([table_uniq.strip("/"), path.strip("/")])
        info_url = "/".join([path, "info", "format:json"])
        info_response = self.get(info_url)
        try:
            num_dims = len(json.loads(info_response.text).get("sizes"))
        except ValueError:
            raise BQApiError("array could not be read")
        # fill slices with missing dims
        for _ in range(num_dims - len(slice_list)):
            slice_list.append(";")
        data_url = "/".join([path, ",".join(slice_list), "format:hdf"])
        response = self.get(data_url)
        # convert HDF5 to Numpy array (preserve indices??)
        with tables.open_file(
            "array.h5",
            driver="H5FD_CORE",
            driver_core_image=response.content,
            driver_core_backing_store=0,
        ) as h5file:
            res = h5file.root.array.read()
        if want_info:
            return res, json.loads(info_response.text)
        else:
            return res

    def store_array(self, array, storepath, name) -> Metadoc:
        """
        Store numpy array or record array in BisQue and return resource doc.
        """
        try:
            dirpath = tempfile.mkdtemp()
            # (1) store array as HDF5 file
            out_name = name + ".h5" if not name.endswith((".h5", ".hdf5")) else name  # importer needs extension .h5
            out_file = os.path.join(dirpath, out_name)
            with tables.open_file(out_file, "w", filters=tables.Filters(complevel=5)) as h5file:  # compression level 5
                if array.__class__.__name__ == "recarray":
                    h5file.create_table(h5file.root, name, array)
                elif array.__class__.__name__ == "ndarray":
                    h5file.create_array(h5file.root, name, array)
                else:
                    raise BQApiError("unknown array type")  # TODO: more specific error
            # (2) call bisque blob service with file
            mountpath = posixpath.join(storepath, out_name)
            blobs = self.session.service("blobs")
            blobs.create_blob(path=mountpath, localfile=out_file)
            # (3) register resource
            return blobs.register(path=mountpath)

        finally:
            shutil.rmtree(dirpath)

    def load_table(self, table_uniq, path, slices=None, as_dataframe=True):
        """
        Load table as a numpy recarray or pandas dataframe.
        """
        ndarr, info = self.load_array(table_uniq, path, slices, want_info=True)
        res = np.core.records.fromarrays(ndarr.transpose(), names=info["headers"], formats=info["types"])
        if as_dataframe is True:
            res = pd.DataFrame.from_records(res)
        return res

    def store_table(self, table, storepath, name) -> Metadoc:
        """
        Store numpy recarray or pandas dataframe in BisQue and return resource doc.
        """
        if isinstance(table, pd.DataFrame):
            table = table.to_records()
        if table.__class__.__name__ != "recarray":
            raise BQApiError("unknown table type")  # TODO: more specific error
        return self.store_array(table, storepath, name)
