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
import proxy plugin

DESCRIPTION
===========

Client side import methods

"""

import logging
import os
import posixpath
import random
import string
import time
from typing import BinaryIO, Callable, Dict, Optional
from urllib.parse import quote as urlquote

import boto3
import botocore
import tenacity
from bq.metadoc.formats import Metadoc
from requests_toolbelt import MultipartEncoder

from vqapi.exception import BQApiError, code_to_exception
from vqapi.util import normalize_unicode

from .base_proxy import FuturizedServiceProxy

log = logging.getLogger("vqapi.services")


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class ImportProxy(FuturizedServiceProxy):
    service_name = "import"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.upload_prefix = "/home/uploads"  # TODO fetch from user prefences
        self.upload_default_mount = "/home"  # TODO fetch from user
        self.protocol_info_map = {"/home": None}  # Map of store to best protocol

    def destination_path(self, srcpath, dstpath):
        """Create a valid destination path from src and dst

        Examples:
          Source known, destination None
          destination_path("filename.tif", None) -> upload_prefix/filename.tif
          destination_path("path2/to/file/filename.tif", None) -> upload_prefix/path/to/file/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", None) -> upload_pefix/filename.tif

          Source None, destination
          destination_path(None, "filename.tif") -> upload_mount/filename.tif
          destination_path(None, "relatitive_path/filename.tif") -> upload_mount/relative_path/filename.tif
          destination_path(None, "/home/project/to/path/filename.tif") -> "/home/project/to/path/filename.tif"

          Source and Destination -> use dest
          destination_path("filename.tif", "filename.tif") -> upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "filename.tif") -> $upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "relative_path/filename.tif") -> $upload_mount/path/to/file/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/poject/path2/filename.tif") -> /home/project/path2/filename.tif

          Source and Destination Dir (marked by trailing "/" -> use src + dest
          destination_path("filename.tif", "apath/") -> $upload_mount/apath/tfilename.tif
          destination_path("path2/to/file/filename.tif", "apath/") -> $upload_mount/apath/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/mount/apath/") -> /home/mount/apath/filename.tif

        """
        if dstpath is None:
            dstpath = self.upload_prefix
            if srcpath == "/":
                return posixpath.join(dstpath, srcpath[1:])
            return posixpath.join(dstpath, srcpath)

        if dstpath[-1] == "/":  # DIR destination
            dstpath = posixpath.join(dstpath, os.path.basename(srcpath))

        if dstpath[0] != "/":  # NOT absolute upload, join with def
            return posixpath.join(self.upload_default_mount, dstpath)

        return dstpath

    # @functools.lru_cache(maxsize=None)
    def transfer_protocol_info(self, path: str = None, protocol: str = None) -> Optional[Metadoc]:
        """Return proto info for best transfer_protocol

        Args:
            path : the destination storepath
        Returns:
           A proto_info dict: with protocol specific information
        """
        if path is None:
            path = self.upload_prefix
        if path[0] == "/":
            path = path[1:]

        dirpath = os.path.dirname(path)
        mount = dirpath.split("/")[0]  # 'home/hello/aaa.jpg' -> ['home', 'hello', 'aaa.jpg']
        if (mount, protocol) in self.protocol_info_map:
            return self.protocol_info_map[(mount, protocol)]

        if protocol is not None:
            available_protocols = [Metadoc.create_doc("prototcol", type=protocol)]
        else:
            protocols = self.fetch(posixpath.join("/transfer_protocol", urlquote(dirpath)))
            # Choose the preferred one by order
            code_to_exception(protocols)
            proto_doc = protocols.doc()
            # log.info("PROTO %s", str(proto_doc))
            available_protocols = proto_doc.path_query("protocol")

        for proto in available_protocols:
            # check if we know one
            if hasattr(self, "transfer_" + proto.attrib["type"]):
                # we know how to transfer, grab info
                proto_info = self.fetch(
                    posixpath.join("/transfer_protocol", dirpath),
                    params={"protocol": proto.attrib["type"]},
                )
                code_to_exception(proto_info)
                proto_info = proto_info.doc()
                self.protocol_info_map[(mount, None)] = proto_info
                self.protocol_info_map[(mount, proto)] = proto_info
                return proto_info
        return None

    def transfer_file(
        self,
        srcpath: str,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
        register: bool = True,
    ):
        """Transfer a file to the system
        Args:
          srcpath : the path to the local file or filename to give to the file object
          xml     :
        """
        with open(srcpath, "rb") as src:
            return self.transfer_fileobj(
                src, xml=xml, callback=callback, srcpath=srcpath, dstpath=dstpath, protocol=protocol, register=register
            )

    def transfer_fileobj(
        self,
        fileobj: BinaryIO,
        srcpath: str = None,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
        register: bool = True,
    ):
        if srcpath is None and hasattr(fileobj, "name"):
            srcpath = fileobj.name
        dstpath = self.destination_path(srcpath, dstpath)
        transfer_info = self.transfer_protocol_info(path=dstpath, protocol=protocol)
        # log.info("TRANS %s", str(transfer_info))
        # Use the protocol to  find a method to transfer the file
        if transfer_info is not None:
            protocol = transfer_info.path_query("protocol")[0]
            transfer_fct = getattr(self, "transfer_" + protocol.attrib["type"])
            if transfer_fct is not None:
                return transfer_fct(
                    fileobj=fileobj,
                    dstpath=dstpath,
                    xml=xml,
                    callback=callback,
                    transfer_info=transfer_info,
                    register=register,
                )
        raise BQApiError("No transfer protocol supported for file transfer")

    def transfer_multipart(
        self, fileobj: BinaryIO, dstpath: str, xml=None, callback=None, transfer_info=None, register=True
    ):
        fields = {}
        filename = normalize_unicode(fileobj.__name__)
        fields["file"] = (
            os.path.basename(filename),
            fileobj,
            "application/octet-stream",
        )
        if xml is not None:
            fields["file_resource"] = (None, xml, "application/xml")
        if fields:
            # https://github.com/requests/toolbelt/issues/75
            m = MultipartEncoder(fields=fields)
            m._read = m.read  # pylint: disable=protected-access
            # filesize = os.fstat (fileobj).st_size
            # haveread = 0

            def reader(size):
                buff = m._read(8192 * 1024)  # 8MB
                # haveread += 8192
                if callable(callback):
                    callback(len(buff))
                return buff

            m.read = reader
            # ID generator is used to force load balancing operations
            response = self.post(
                "transfer_" + id_generator(),
                data=m,
                headers={"Accept": "text/xml", "Content-Type": m.content_type},
            )
            code_to_exception(response)
            return response.doc()

    def transfer_binary(self, fileobj, dstpath, xml=None, callback=None, transfer_info=None, register=True):
        response = self.post(
            posixpath.join("transfer_direct", urlquote(dstpath[1:])),
            data=fileobj,
            headers={"Content-Type": "application/octet-stream"},
        )
        code_to_exception(response)

        if xml is None:
            return None

        blobs = self.session.service("blobs")

        blob = blobs.register(path=dstpath[1:], resource=xml)

        # blob = blobs.register(posixpath.join(path, filename))
        # if xml:
        #     meta = self.session.service('meta')
        #     # Find the uploaded blob and register with XML
        #     for kid in Metadoc.from_tagxml(xml):
        #         blob.append(kid)
        #     meta.put(blob.get("resource_uniq"), data=blob)
        return blob

    def transfer_s3(
        self,
        fileobj: BinaryIO,
        dstpath,
        xml=None,
        callback=None,
        transfer_info=None,
        register=True,
        **kw,
    ):
        """Transfer a file to s3
        Args :
            fileob  : the options open file object
            dstpath : a store path i.e. /storename/d1/d2
            xml     : xml to registered
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                              <Uid>1000</Uid>
                              <Gid>1000</Gid>
                            </S3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        # Get cliend creds from info

        filename = os.path.basename(dstpath)
        # partial_path = "/".join(dstpath.split("/")[2:-1])
        partial_path = ""
        try:
            upload_ok = False
            s3client = None
            for _ in range(3):  # Attempt upload 3 times with expired token handling
                info = transfer_info.path_query("//info")[0].to_json()
                s3_info = info["info"]
                log.debug(
                    "INFO %s destpath:%s filename:%s fileobj:%s",
                    s3_info,
                    dstpath,
                    filename,
                    fileobj,
                )
                if s3client is None:
                    s3client = self._s3_session(s3_info["Credentials"])

                try:
                    if not self._s3_dir_exists(s3client, s3_info, partial_path):
                        self._s3_create_dirs(s3client, s3_info, partial_path)
                    s3client.upload_fileobj(
                        fileobj,
                        Bucket=s3_info["Destination"]["S3"]["Bucket"],
                        Key=posixpath.join(
                            s3_info["Destination"]["S3"]["Folder"],
                            partial_path,
                            filename,
                        ),
                        Callback=callback,
                        ExtraArgs={
                            "Metadata": {
                                "user-agent": "aws-fsx-lustre",
                                "file-permissions": "0100660",
                                "file-owner": s3_info["Destination"]["S3"]["Uid"],
                                "file-group": s3_info["Destination"]["S3"]["Gid"],
                            }
                        },
                    )
                    fileobj.close()
                    upload_ok = True
                    break
                except botocore.exceptions.ClientError as error:
                    code = error.response["Error"]["Code"]
                    log.warn("AWS Client error %s -> code %s", error, code)
                    if code in ("ExpiredToken", "AccessDenied"):
                        transfer_info = self._s3_refresh(transfer_info)
                        s3client = None
                        fileobj = open(fileobj.name, "rb")  # Potential File Obj Leak
                        continue

            if not upload_ok:
                raise BQApiError(f"Failed upload of {filename}. S3 token invalid")

            if xml is None or not register:
                return None

            # register the uploaded file with xml if available
            blobs = self.session.service("blobs")
            if isinstance(xml, str):
                xml = Metadoc.from_naturalxml(xml)

            try:
                time.sleep(2)
                for attempt in tenacity.Retrying(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(2)):
                    log.info(f"REGISTER {dstpath}")
                    blobdoc = blobs.register(path=dstpath, resource=xml)
                    return blobdoc
            except tenacity.RetryError:
                log.error("Regsitration failed after upload")

        except boto3.exceptions.S3UploadFailedError:
            log.exception("During upload of %s", filename)
        return None

    def _s3_create_dirs(self, s3client, s3_info: dict, path: str):
        """Ensure directory exists and has proper metadata (permissions)"""
        head, tail = posixpath.split(path)
        if not tail:  # special case for trailing '/'
            head, tail = posixpath.split(head)
        if head and tail:
            # check if head exists
            if not self._s3_dir_exists(s3client, s3_info, head):
                # log.debug("recurse %s", head)
                self._s3_create_dirs(s3client, s3_info, head)
        #
        self._s3_mkdir(s3client, s3_info, path)

    def _s3_dir_exists(self, s3client, s3_info, dirpath):
        """Check if user rooted directory exists"""
        try:
            # log.debug("s3_direxists %s", dirpath)
            s3client.head_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
            )
            return True
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("s3direxists error %s", code)
        return False

    def _s3_mkdir(self, s3client, s3_info, dirpath):
        try:
            # log.debug("s3_mkdir %s ", dirpath)
            s3client.put_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
                Metadata={
                    "file-owner": s3_info["Destination"]["S3"]["Uid"],
                    "file-group": s3_info["Destination"]["S3"]["Gid"],
                },
            )
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("ended on %s", code)

    def _s3_session(self, s3_info: Dict):
        """Create a long-lasting s3 Session suitable for caching
        Args:
           s3_info : {"AccessKeyId": "ID",
                       "SessionToken": "Token", "SecretAccessKey":
                       "Secret", "Expiration": "Expires"}

        Returns:
          a S3 boto client
        TODO :  Utilize a refreshable credential provider
                https://stackoverflow.com/questions/61899028/where-can-i-find-the-documentation-for-writing-custom-aws-credential-provider-us
        """
        session = boto3.session.Session()  # see https://github.com/boto/boto3/issues/801
        s3client = session.client(
            "s3",
            aws_access_key_id=s3_info["AccessKeyId"],
            aws_secret_access_key=s3_info["SecretAccessKey"],
            aws_session_token=s3_info["SessionToken"],
        )
        return s3client

        raise BQApiError("transfer_s3 not implemented")

    def _s3_refresh(self, transfer_info: Metadoc) -> Metadoc:
        """Fetch new credential when expired
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                            </3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        transfer_info = self.post("transfer_protocol", data=transfer_info)
        return transfer_info

    def transfer_fsxlustre(self, *args, **kw) -> Metadoc:
        return self.transfer_s3(*args, **kw)

    def ingester_list(self) -> Metadoc:
        """List available scripts"""
        scripts = self.fetch("ingest")
        code_to_exception(scripts)
        return scripts.doc()

    def ingester_run(self, script_name, storepath, preview=True) -> Metadoc:
        """Run a registration script"""
        run = Metadoc(tag="resource")
        run.add_tag("processor", value=script_name)
        run.add_tag("path", value=storepath)
        resp = self.post("ingest", data=run, params={"preview": preview})
        code_to_exception(resp)
        return resp.doc()
