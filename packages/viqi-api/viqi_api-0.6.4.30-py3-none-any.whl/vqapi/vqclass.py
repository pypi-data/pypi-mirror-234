import copy
import inspect
import json
import logging
import sys
import time
from typing import List, Tuple

from bq.metadoc.formats import Metadoc, anyxml_to_etree

from vqapi import BQSession
from vqapi.exception import BQApiError
from vqapi.vqquery import get_provenance, run_sparql_query

log = logging.getLogger("vqapi.vqclass")


def get_header(res, name):
    return res.headers.get(name, "").lstrip("W/")[
        1:-1
    ]  # remove entity tag and quotes (why is this not done by pyramid?)


def _get_param_types(param, default="string"):
    param_type = param.get_attr("type", default)
    if param_type == "resource":
        acc_types = param.path_query("./template/accepted_type")
        if len(acc_types) > 0:
            param_type = [acc_type.get_value() for acc_type in acc_types]
    if not isinstance(param_type, list):
        param_type = [param_type]
    return param_type


def _fetch_subdoc(sess: "VQSession", doc_id: str, node_id: str) -> Metadoc:
    meta = sess.service("meta")
    return meta.request(
        method="get",
        path=f"/{doc_id}@{node_id}",
        params={"view": "deep,clean"},
        render="doc",
    )


def copy_as_not_impl(other_class):
    """
    Decorator that adds a method returning "Not Implemented" for each method in other_class
    that has not been defined in this class.
    """

    def wrapper(cls):
        def _notimpl(*args, **kwargs):
            raise NotImplementedError()

        for func in other_class.__dict__:
            if callable(getattr(other_class, func)) and func not in cls.__dict__:
                setattr(cls, func, _notimpl)
        return cls

    return wrapper


class VQCollection:
    """
    Collection of resources (typically result of a query)
    """

    def __init__(self, sess: "VQSession", from_query: Tuple[str, str] = None):
        self._sess = sess
        self._from_query = from_query  # from_query = (sparql WHERE str, doc var)

    def __len__(self):
        if self._from_query is not None:
            query, doc_var = self._from_query
            matches = run_sparql_query(
                self._sess,
                f"SELECT COUNT(?{doc_var}/@resource_uniq) AS cnt WHERE {{ {query} }}",
            )
            return int(matches[0]["cnt"])

    def __iter__(self):
        if self._from_query is not None:
            query, doc_var = self._from_query
            for match in run_sparql_query(
                self._sess,
                f"SELECT ?{doc_var}/@resource_uniq AS docid WHERE {{ {query} }}",
            ):
                yield self._sess.load(match["docid"])

    def delete(self):
        if self._from_query is not None:
            # TODO: should use update query here
            query, doc_var = self._from_query
            patchdoc = Metadoc(tag="patch")
            matches = run_sparql_query(
                self._sess,
                f"SELECT ?{doc_var}/@resource_uniq AS docid WHERE {{ {query} }}",
            )
            for match in matches:
                patchdoc.add_tag("remove", sel=f"/{match['docid']}")
            meta = self._sess.service("meta")
            res = meta.request(method="patch", path="/", data=patchdoc, render=None)
            if res.status_code != 200:
                raise BQApiError(f"collection could not be deleted: {res.text}")


@copy_as_not_impl(Metadoc)
class VQResource:
    """
    Class to store any ViQi-backed resource doc;
    same interface as Metadoc but has extra functions depending on resource type.
    """

    def __init__(self, sess: "VQSession", doc_uniq: str = None, doc_version: str = None, **attrs):
        tag = self.resource_type
        self._doc_uniq = doc_uniq
        self._doc_version = doc_version
        self._doc = Metadoc(tag=tag, **attrs)
        self._doc_lvls = 0
        self._sess = sess
        self._meta = sess.service("meta")

    @staticmethod
    def load(sess: "VQSession", uniq: str) -> "VQResource":
        return sess.load(uniq)

    @classmethod
    def find(cls, sess: "VQSession", **kwargs) -> "VQResource":
        raise NotImplementedError(f"find operation not implemented for resource type {cls.resource_type}")

    def _refresh(self, lvls: int):
        view = "short" if lvls == 1 else ("full" if lvls == 2 else "deep")
        if self._doc_uniq is not None:
            if lvls <= self._doc_lvls:
                headers = {"If-None-Match": self._doc_version}  # fetch only if newer version available
            else:
                headers = {}  # fetch always, need more levels
            res = self._meta.request(
                method="get",
                path="/" + self._doc_uniq,
                params={"view": view},
                headers=headers,
                render=None,
            )
            if res.status_code == 200:
                self._doc = res.doc()
                self._doc_version = get_header(res, "ETag")
                self._doc_lvls = lvls
            elif res.status_code == 304:  # not modified
                pass
            else:
                raise BQApiError(f"resource {self._doc_uniq} could not be refreshed")

    def __getattr__(self, name):
        if name in ("_doc_uniq", "_doc_version", "_doc", "_doc_lvls", "_sess", "_meta"):
            return self.__dict__[name]
        self._refresh(lvls=1)
        return self._doc.__getattr__(name)

    def __setattr__(self, name, val):
        if name in ("_doc_uniq", "_doc_version", "_doc", "_doc_lvls", "_sess", "_meta"):
            self.__dict__[name] = val
            return
        raise NotImplementedError(f'setting of doc attribute "{name}" not implemented')

    def get_docid(self):
        return self._doc_uniq

    def get_value(self):
        self._refresh(lvls=1)
        return self._doc.get_value()

    def get_attr(self, attr, default=None):
        self._refresh(lvls=1)
        return self._doc.get_attr(attr, default)

    def get(self, attr, default=None):
        self._refresh(lvls=1)
        return self._doc.get(attr, default)

    def to_json(self):
        self._refresh(lvls=sys.maxsize)  # avoid if possible
        return self._doc.to_json()

    def __str__(self):
        self._refresh(lvls=sys.maxsize)  # avoid if possible
        return self._doc.to_naturalxml()

    def path_query(self, path):
        self._refresh(lvls=sys.maxsize)  # TODO: maybe run as server side query?
        return self._doc.path_query(path)

    def add_sibling(self, tag, **attrs):
        if self._doc_uniq is not None:
            raise NotImplementedError("updates to stored docs not implemented")
        return self._doc.add_sibling(tag, **attrs)

    def add_tag(self, tag, **attrs):
        if self._doc_uniq is not None:
            raise NotImplementedError("updates to stored docs not implemented")
        return self._doc.add_tag(tag, **attrs)

    def delete(self):
        if self._doc_uniq is not None:
            raise NotImplementedError("updates to stored docs not implemented")
        return self._doc.delete()

    def add_child(self, newchild):
        if self._doc_uniq is not None:
            raise NotImplementedError("updates to stored docs not implemented")
        return self._doc.add_child(newchild)


class VQMex(VQResource):
    resource_type = "mex"

    def wait(self):
        """
        Wait for module to finish or fail.
        """
        while self.get_value() not in ("FINISHED", "FAILED"):
            time.sleep(10)

    def retry(self):
        """
        (Partially) re-run a failed module with same settings.
        For multi-runs, only failed submexes will be re-run.
        """
        mex_service = self._sess.service("mexes")
        try:
            update_doc = Metadoc(tag="patch")
            update_doc.add_tag("replace", sel="/mex/@value", value="RUNNING")
            mex_doc = mex_service.request(
                path=f"/{self.get_docid()}",
                method="patch",
                render="doc",
                data=update_doc,
            )
            if not isinstance(mex_doc, Metadoc):
                raise BQApiError(f"module could not be restarted: {mex_doc.text}")
        except Exception as exc:
            raise BQApiError(f"module could not be restarted: {str(exc)}")

    def get_build(self) -> "VQBuild":
        """
        Get build def for this mex.

        Returns:
            VQBuild: build doc
        """
        self._refresh(lvls=2)
        build_id = self._doc.path_query("//build")[0]
        return VQBuild.load(self._sess, build_id.get_value())

    def get_output(self, output_name: str) -> object:
        """
        Retrieve output of module.

        Args:
            output_name (str): name of output

        Returns:
            object: output value (may be any type, including VQResource subtype)
        """
        self.wait()
        self._refresh(lvls=sys.maxsize)
        mex_out = self._doc.path_query(f'/mex/outputs//{output_name}[not(@type) or @type != "group"]')
        if len(mex_out) == 0:
            if len(self._doc.path_query("/mex/mex")) > 0:
                raise BQApiError("this is a mex with submexes; please use get_sub_output or get_sub_outputs")
            else:
                raise BQApiError(f'output "{output_name}" not found')
        out_arg = mex_out[0]
        return self._get_output_single(
            out_arg_type=out_arg.get_attr("type", "doc"),
            out_arg_value=out_arg.get_value(),
            out_docid=self._doc_uniq,
            out_id=out_arg.get("_id"),
        )

    def get_qc(self, qc_name: str) -> object:
        """
        Retrieve generated qc data of module.

        Args:
            qc_name (str): name of qc output

        Returns:
            object: output value (may be any type, including VQResource subtype)
        """
        self.wait()
        self._refresh(lvls=sys.maxsize)
        mex_out = self._doc.path_query(f'/mex/qc//{qc_name}[not(@type) or @type != "group"]')
        if len(mex_out) == 0:
            raise BQApiError(f'qc data "{qc_name}" not found')
        out_arg = mex_out[0]
        return self._get_output_single(
            out_arg_type=out_arg.get_attr("type", "doc"),
            out_arg_value=out_arg.get_value(),
            out_docid=self._doc_uniq,
            out_id=out_arg.get("_id"),
        )

    def get_sub_output(self, output_name: str, **selectors) -> object:
        """
        Retrieve output in specific submex of a multimex run.

        Args:
            output_name (str): name of output
            selectors: one or more mex input tags/values to specify which submex

        Returns:
            object: output value (may be any type, including VQResource)
        """
        if len(selectors) == 0:
            raise BQApiError("need at least one selector to find output")
        self.wait()
        extra_patterns = []
        extra_filters = []
        for idx, (key, val) in enumerate(selectors.items()):
            val = val.get_docid() if isinstance(val, VQResource) else str(val)
            extra_patterns.append(f"?inputs :// tag:?tag{idx}")
            extra_filters.append(f'?tag{idx}/@name = "{key}" AND ?tag{idx}/@value_str = "{val}"')
        extra_patterns = ". ".join(extra_patterns)
        extra_filters = " AND ".join(extra_filters)
        query = f"""
            SELECT ?out/@resource_uniq AS out_docid
                   ?out/@node_id AS out_id
                   ?out/@type AS out_type
                   ?out/@value_str AS out_val
            WHERE {{
                /mex:?this :/ mex:?mexref. ?mexref :-> /mex:?submex. ?submex :/ tag:?outputs. ?outputs :/ tag:?out.
                ?submex :/ tag:?inputs. {extra_patterns}
                FILTER( ?this/@resource_uniq = "{self._doc_uniq}" AND
                        ?inputs/@name = "inputs" AND
                        ?outputs/@name = "outputs" AND
                        ?out/@name = "{output_name}" AND
                        {extra_filters} )
            }}
            """
        matches = run_sparql_query(self._sess, query)
        if len(matches) == 0:
            raise BQApiError(f'no outputs "{output_name}" with selectors found')
        if len(matches) > 1:
            raise BQApiError("selectors ambiguous")
        return self._get_sub_output_single(
            out_arg_type=matches[0]["out_type"] or "doc",
            out_arg_value=matches[0]["out_val"] or None,
            out_docid=matches[0]["out_docid"],
            out_id=matches[0]["out_id"],
        )

    def get_sub_outputs(self, output_name: str) -> List[object]:
        """
        Retrieve specific outputs in all submexes of a multimex run.

        Args:
            output_name (str): name of output

        Returns:
            List[object]: list of output values (each may be any type, including VQResource)
        """
        self.wait()
        query = f"""
            SELECT ?out/@resource_uniq AS out_docid
                   ?out/@node_id AS out_id
                   ?out/@type AS out_type
                   ?out/@value_str AS out_val
            WHERE {{
                /mex:?this :/ mex:?mexref. ?mexref :-> /mex:?submex. ?submex :/ tag:?outputs. ?outputs :/ tag:?out
                FILTER( ?this/@resource_uniq = "{self._doc_uniq}" AND
                        ?outputs/@name = "outputs" AND
                        ?out/@name = "{output_name}" )
            }}
            """
        matches = run_sparql_query(self._sess, query)
        if len(matches) == 0:
            raise BQApiError(f'no outputs "{output_name}" found')
        return [
            self._get_output_single(
                out_arg_type=match["out_type"] or "doc",
                out_arg_value=match["out_val"] or None,
                out_docid=match["out_docid"],
                out_id=match["out_id"],
            )
            for match in matches
        ]

    def _get_output_single(self, out_arg_type, out_arg_value, out_docid, out_id):
        if out_arg_type == "number":
            try:
                return int(out_arg_value)
            except ValueError:
                try:
                    return float(out_arg_value)
                except ValueError:
                    return out_arg_value
        elif out_arg_type == "string":
            return out_arg_value
        elif out_arg_type == "doc":
            return _fetch_subdoc(self._sess, out_docid, out_id)
        elif out_arg_type in self._sess.factory.resources:
            return self._sess.load(out_arg_value)
        else:
            return _fetch_subdoc(self._sess, out_docid, out_id)

    def get_sub_states(self) -> dict:
        """
        Retrieve states in all submexes of a multimex run.

        Returns:
            dict: submex states and counts
        """
        query = f"""
            SELECT ?submex/@value_str AS state
                   COUNT(?submex/@value_str) AS count
            WHERE {{
                /mex:?this :/ mex:?mexref. ?mexref :-> /mex:?submex
                FILTER( ?this/@resource_uniq = "{self._doc_uniq}" )
            }}
            GROUP BY ?submex/@value_str
            """
        matches = run_sparql_query(self._sess, query)
        return {match["state"]: int(match["count"]) for match in matches}

    def get_all_mexes(self) -> VQCollection:
        """
        Get collection of mex and all its submexes.

        Returns:
            VQCollection: collection of mex and submexes
        """
        query = f"""{{ /mex:?mex FILTER( ?mex/@resource_uniq = "{self._doc_uniq}" ) }} UNION
                    {{ /mex:?supermex :/ mex:?mexref. ?mexref :-> /mex:?mex FILTER( ?supermex/@resource_uniq = "{self._doc_uniq}" ) }}"""
        return VQCollection(self._sess, from_query=(query, "mex"))


class VQModule(VQResource):
    resource_type = "module"

    @property
    def inputs(self) -> List[Tuple[str, str, object]]:
        """
        Get list of input names.

        Returns:
            List[Tuple[str,str,object]]: list of (input name, input type, default value)
        """
        self._refresh(lvls=sys.maxsize)
        return [
            (module_arg.get_attr("name"), _get_param_types(module_arg))
            for module_arg in self._doc.path_query('/module/inputs//*[not(@type) or @type != "group"][./template]')
        ]

    @property
    def outputs(self) -> List[Tuple[str, str]]:
        """
        Get list of output names.

        Returns:
            List[Tuple[str,str]]: list of (output name, output type)
        """
        self._refresh(lvls=sys.maxsize)
        return [
            (module_arg.get_attr("name"), _get_param_types(module_arg, "doc"))
            for module_arg in self._doc.path_query('/module/outputs//*[not(@type) or @type != "group"][./template]')
        ]


class VQBuild(VQResource):
    resource_type = "build"

    @classmethod
    def find(cls, sess: "VQSession", module_name: str, version: str) -> "VQBuild":
        """
        Fetch build doc for given module/version combo.

        Args:
            sess (VQSession): session
            module_name (str): name of the module
            version (str): version tag of build

        Returns:
            VQBuild: build doc

        Raises:
            BQApiError
        """
        # TODO: the following could be moved into the lower level build api
        query = f"""
            SELECT ?bld/@resource_uniq AS build_id
            WHERE {{
                /build:?bld :/ module:?modref. ?modref :-> /module:?mod
                FILTER( ?mod/@name = "{module_name}" AND
                        ?bld/@name = "{version}" )
            }}
            """
        matches = run_sparql_query(sess, query)
        if len(matches) == 0:
            raise BQApiError(f'module "{module_name}" (version "{version}") not found')
        if len(matches) > 1:
            raise BQApiError(f'multiple modules "{module_name}" (version "{version}") found')
        return VQResource.load(sess, matches[0]["build_id"])

    def get_module(self) -> VQModule:
        """
        Get module def for this build.

        Returns:
            VQModule: module doc
        """
        self._refresh(lvls=2)
        module_id = self._doc.path_query("//module")[0]
        return VQModule.load(self._sess, module_id.get_value())

    @property
    def inputs(self) -> List[Tuple[str, str, object]]:
        """
        Get list of input names.

        Returns:
            List[Tuple[str,str,object]]: list of (input name, input type, default value)
        """
        self._refresh(lvls=sys.maxsize)
        return [
            (module_arg.get_attr("name"), _get_param_types(module_arg))
            for module_arg in self._doc.path_query('/build/inputs//*[not(@type) or @type != "group"][./template]')
        ]

    @property
    def outputs(self) -> List[Tuple[str, str]]:
        """
        Get list of output names.

        Returns:
            List[Tuple[str,str]]: list of (output name, output type)
        """
        self._refresh(lvls=sys.maxsize)
        return [
            (module_arg.get_attr("name"), _get_param_types(module_arg, "doc"))
            for module_arg in self._doc.path_query('/build/outputs//*[not(@type) or @type != "group"][./template]')
        ]

    def start(
        self,
        _keep_log: bool = False,
        _extra_tags: dict = None,
        _execute_options: dict = None,
        _merge_outputs: list = None,
        **kwargs,
    ) -> VQMex:
        """
        Start this build with the given input parameters.

        Args:
            _keep_log (bool): preserve log of run in module execution dir
            _extra_tags (dict): extra tags to be added to Mex
            _execute_options (dict): override execute options (e.g., "requested_memory", "requested_gpus")
            _merge_outputs (list): list of output names for submex output merging
            kwargs: input parameters (will be mapped to module inputs)

        Returns:
            VQMex: mex doc

        Raises:
            BQApiError
        """

        self._refresh(lvls=sys.maxsize)  # we need most of the doc anyway

        # create new mex resource based on build doc
        mex_doc = Metadoc(tag="mex")

        # find out if there are iterable inputs
        iterable_nodes = self._doc.path_query("/build/execute_options/iterable")
        iterables = {iterable_node.get_value(): iterable_node.get("type", "string") for iterable_node in iterable_nodes}

        # copy inputs from build doc, remove templates and overwrite any params
        build_inputs = self._doc.path_query("/build/inputs")[0]
        mex_inputs = copy.deepcopy(build_inputs)

        # fill in parameters from kwargs
        add_iterables = {}
        for param_name, param_val in kwargs.items():
            module_arg = mex_inputs.path_query(f'/inputs//{param_name}[not(@type) or @type != "group"][./template]')
            if len(module_arg) == 0:
                raise BQApiError(f'Unknown module parameter "{param_name}"')
            module_arg = module_arg[0]
            single_param_val = param_val
            skip_typecheck = False
            if isinstance(param_val, VQDataset) and param_name in iterables and iterables[param_name] == "dataset":
                add_iterables[param_name] = "dataset"
                skip_typecheck = True  # would need to check the type of elements of dataset
            elif isinstance(param_val, list) and not any(
                ptype.startswith("list") for ptype in _get_param_types(module_arg)
            ):
                if param_name in iterables and iterables[param_name] == "list":
                    add_iterables[param_name] = "list"
                    single_param_val = param_val[0]
                    param_val = ",".join(param_val)
                else:
                    raise BQApiError(f'List of values provided for non-iterable parameter "{param_name}"')
            if not skip_typecheck:
                if (
                    (isinstance(single_param_val, bool) and "boolean" not in _get_param_types(module_arg))
                    or (
                        isinstance(single_param_val, (int, float, complex))
                        and "number" not in _get_param_types(module_arg)
                    )
                    or (isinstance(single_param_val, str) and "string" not in _get_param_types(module_arg))
                    or (
                        isinstance(single_param_val, list)
                        and not any(ptype.startswith("list") for ptype in _get_param_types(module_arg))
                    )
                    or (
                        isinstance(single_param_val, VQResource)
                        and single_param_val.resource_type not in _get_param_types(module_arg)
                        and "resource" not in _get_param_types(module_arg)
                    )
                ):
                    raise BQApiError(
                        f'Type mismatch for module parameter "{param_name}"; expected: {_get_param_types(module_arg)} got: {type(single_param_val)}'
                    )
            if isinstance(param_val, VQResource):
                module_arg.set_value(param_val.get_docid())
                module_arg.set_attr("type", param_val.resource_type)
            elif isinstance(param_val, list):
                module_arg.set_value(";".join(str(param) for param in param_val))
            else:
                module_arg.set_value(str(param_val))

        # remove templates
        for templ in mex_inputs.path_query("//template"):
            templ.delete()

        # add inputs to mex
        mex_doc.add_child(mex_inputs)

        # add iterable / keep_log options / overrides
        if len(add_iterables) > 0 or _keep_log or _execute_options:
            ex_opt_tag = mex_doc.add_tag("execute_options")
            for iter_name, iter_type in add_iterables.items():
                ex_opt_tag.add_tag("iterable", type=iter_type, value=iter_name)
            if _keep_log:
                ex_opt_tag.add_tag("keep_log", value="true")
            if _merge_outputs:
                for out_name in _merge_outputs:
                    ex_opt_tag.add_tag("mergeable", type="dataset", value=out_name)
            if _execute_options:
                for key, val in _execute_options.items():
                    ex_opt_tag.add_tag(key, value=val)

        # add build reference
        mex_doc.add_tag("build", value=self.get_docid())

        # add any extra tags
        if _extra_tags:
            extra_tag = mex_doc.add_tag("optional-tags")
            for key, val in _extra_tags.items():
                extra_tag.add_tag(key, value=val)

        # POST mex doc to mex_service to start module
        mex_service = self._sess.service("mexes")
        try:
            mex_doc = mex_service.request(path="/", method="post", render="doc", data=mex_doc)
            if not isinstance(mex_doc, Metadoc):
                raise BQApiError(f"module could not be started: {mex_doc.text}")
        except Exception as exc:
            raise BQApiError(f"module could not be started: {str(exc)}")

        # return created mex resource
        return VQMex.load(self._sess, mex_doc.get_docid())


class VQTableContainer(VQResource):
    resource_type = "tablecontainer"

    @staticmethod
    def concat(
        sess: "VQSession",
        table_containers: List["VQTableContainer"],
        in_path: str,
        out_path: str,
        dim: int,
    ) -> "VQTableContainer":
        pass  # !!!

    def get_array(self, path, slices=None):
        table_service = self._sess.service("tables")
        return table_service.load_array(table_uniq=self.get_docid(), path=path, slices=slices)

    def get_table(self, path, slices=None, as_dataframe=True):
        table_service = self._sess.service("tables")
        return table_service.load_table(
            table_uniq=self.get_docid(),
            path=path,
            slices=slices,
            as_dataframe=as_dataframe,
        )


class VQTable(VQResource):
    resource_type = "table"


class VQDataset(VQResource):
    resource_type = "dataset"


class VQConnoisseur(VQResource):
    resource_type = "connoisseur"


class VQPlotly(VQResource):
    resource_type = "plotly"

    def show(self):
        """
        Get plot as plotly figure.

        Returns:
            plotly.graph_objects.Figure
        """
        try:
            from plotly.graph_objects import Figure
        except ImportError:
            raise BQApiError("show requires installed plotly package")

        blob_service = self._sess.service("blobs")
        with blob_service.read_chunk(self.get_docid(), as_stream=True) as f:
            stored_fig = json.loads(f.readall().decode("utf-8"))
            return Figure(data=stored_fig[0], layout=stored_fig[1])


class VQImage(VQResource):
    resource_type = "image"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._geometry = None
        self._imgmeta = None
        self._imginfo = {}
        self._histogram = None

    def __getattr__(self, name):
        if name in ("_imgmeta", "_imginfo", "_geometry", "_histogram"):
            return self.__dict__[name]
        return super().__getattr__(name)

    def __setattr__(self, name, val):
        if name in ("_imgmeta", "_imginfo", "_geometry", "_histogram"):
            self.__dict__[name] = val
            return
        return super().__setattr__(name, val)

    def meta(self):
        "return image meta as doc"
        if self._imgmeta is None:
            info = self.pixels().meta().fetch(want_str=True)
            self._imgmeta = Metadoc(et=anyxml_to_etree(info))
            self._imginfo = self._imgmeta.to_json()["resource"]
        return self._imgmeta

    def info(self):
        "return image meta as dict"
        if self._imgmeta is None:
            self.meta()
        return self._imginfo

    def geometry(self):
        "return x,y,z,t,ch of image"
        if self._geometry is None:
            info = self.meta()
            geom = []
            for n in "xyztc":
                tn = info.path_query(f"//image_num_{n}")
                geom.append(tn[0].get("value"))
            self._geometry = tuple(map(int, geom))
        return self._geometry

    def histogram(self):
        "returns image histogram"
        if self._histogram is None:
            s = self.pixels().command("histogram", arguments="json").fetch(want_str=True)
            h = json.loads(s)
            if "histogram" in h:
                self._histogram = h["histogram"]
        return self._histogram

    def pixels(self):
        return self._sess.service("pixels").pixels(self.get_docid())


class VQFactory:
    resources = {
        x[1].resource_type: x[1]
        for x in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(x[1]) and hasattr(x[1], "resource_type")
    }

    def load(self, session: BQSession, uniq: str) -> VQResource:
        """
        Establish link to ViQi-backed resource via its uniq.

        Args:
            session (BQSession): initialized session
            uniq (str): resource uniq

        Returns:
            VQResource: the resource object
        """
        meta = session.service("meta")
        res = meta.request(method="get", path="/" + uniq, params={}, view="short", render=None)
        if res.status_code != 200:
            raise BQApiError(f"resource {uniq} could not be loaded")
        doc_version = get_header(res, "ETag")
        doc = res.doc()
        resource_type = doc.tag
        attrs = {"value": doc.get_value()}
        for attr in doc.attrib:
            attrs[attr] = doc.get(attr)
        c = self.resources.get(resource_type)
        return c(session, doc_uniq=uniq, doc_version=doc_version, **attrs)

    def find(self, session: BQSession, resource_type: str, **kwargs) -> VQResource:
        """
        Find a resource based on resource specific search args.

        Args:
            session (BQSession): initialized session
            resource_type (str): the type of the resource
            kwargs: type-specific search args

        Returns:
            VQResource: the found resource
        """
        c = self.resources.get(resource_type)
        return c.find(session, **kwargs)


class VQSession(BQSession):
    def __init__(self):
        super().__init__()
        self.factory = VQFactory()
        self._deltas = []

    def __getstate__(self):
        return super().__getstate__(), self.factory, self._deltas

    def __setstate__(self, state):
        super().__setstate__(state[0])
        self.factory = state[1]
        self._deltas = state[2]

    def init(
        self,
        bisque_url,
        credentials=None,
        moduleuri=None,
        create_mex=False,
        enable_cache=True,
    ):
        res = super().init(bisque_url, credentials, moduleuri, create_mex, enable_cache=enable_cache)
        # self.factory = VQFactory()
        # self._init_cache()
        return res

    def init_local(
        self,
        user,
        pwd,
        moduleuri=None,
        bisque_root=None,
        create_mex=True,
        as_user=None,
        enable_cache=False,
    ):
        res = super().init_local(
            user,
            pwd,
            moduleuri,
            bisque_root,
            create_mex,
            as_user,
            enable_cache=enable_cache,
        )
        # self.factory = VQFactory()
        # self._init_cache()
        return res

    def init_mex(self, mex_url, token, user=None, bisque_root=None, enable_cache=False):
        res = super().init_mex(mex_url, token, user, bisque_root, enable_cache=enable_cache)
        ##self.factory = VQFactory()
        # self._init_cache()
        return res

    def init_request(self, request, enable_cache=True):
        res = super().init_request(request, enable_cache=enable_cache)
        # self.factory = VQFactory()
        # self._init_cache()
        return res

    def load(self, uniq: str) -> VQResource:
        return self.factory.load(self, uniq)

    def flush(self):
        """
        Write any pending doc changes back to ViQi server.
        """
        if len(self._deltas) > 0:
            # some local changes => try to write them back as PATCH
            raise NotImplementedError(
                "write back of metadata docs not implemented"
            )  # need to write back if any changes or new doc (might throw version conflict!)

    def find(self, resource_type: str, **kwargs) -> VQResource:
        return self.factory.find(self, resource_type, **kwargs)

    def select_from_sparql(self, pattern: str, select_var: str) -> VQCollection:
        return VQCollection(self, from_query=(pattern, select_var))

    def get_provenance(
        self,
        seed: VQResource,
        upstream: bool = True,
        downstream: bool = True,
        max_fanout: int = 3,
        out_format: str = "dot",
    ) -> object:
        """
        Experimental fct to retrieve provenance graph.

        Args:
            seed (VQResource): starting resource for graph
            upstream (bool): find upstream provenance
            downstream (bool): find downstream provenance
            max_fanout (int): max fanout from/to mex after which "(More)" nodes are added
            out_format (str): desired return format ("dot" or "list")

        Returns:
            object: either DOT string or list of VQResources
        """
        return get_provenance(
            self,
            seed,
            upstream=upstream,
            downstream=downstream,
            max_fanout=max_fanout,
            out_format=out_format,
        )
