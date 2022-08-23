''' parse.py
'''
import itertools
import json

import jq
from bs4 import BeautifulSoup, Tag

from nkparser.help import *

def parse_text(data_type, text, entity_id):
    """ HTML parser by config file
    :param data_type: data type of target such as ENTRY, RESULT, ODDS and HORSE
    :param entity_id: entity id of target such as race id or horse id
    :return: :class:`Response <Response>` object
    """
    parser = TextParser(data_type, text, entity_id)
    return parser.exec()

def parse_json(data_type, text, entity_id):
    """ JSON parser by config file
    """
    parser = JsonParser(data_type, text, entity_id)
    return parser.exec()

class Parser():
    """ base class of Loaders """
    def __init__(self, data_type, text, entity_id):
        self.data_type = data_type
        self.entity_id = entity_id
        self.soup = BeautifulSoup(text, "html.parser")
        self.text = text
        self.selector = load_config(data_type)['property']['selector']
        self.columns = load_config(data_type)['columns']
        self.validator = load_config(data_type)['property']['validator']

    def _apply_format(self, col, rec):
        val = rec[col["col_name"]]
        if "reg" in col and val is not None:
            val = formatter(col["reg"], val, col["var_type"])
        return val

    def _add_entity_id(self, col, rec):
        val = rec[col["col_name"]]
        if "index" in col and col["index"] == "entity_id":
            val = self.entity_id
        return val

    def _apply_pre_func(self, col, rec):
        val = rec[col["col_name"]]
        if "pre_func" in col:
            # Apply Pre Function if it is defined
            val = self._call_functions(col, rec, "pre_func")
        elif "pre_func" not in col and isinstance(val, Tag):
            # Apply to String if pre_func is not defined
            val = val.text if val is not None else None
        return val

    def _apply_post_func(self, col, rec):
        val = rec[col["col_name"]]
        if "post_func" in col:
            # Apply Post Function if it is defined
            val = self._call_functions(col, rec, "post_func")
        return val

    def _call_functions(self, col, rec, key):
        func_name = col[key]["name"]
        args = ", ".join([f"rec['{a}']" for a in col[key]["args"]])
        # メモ: 複数の変数をevalした場合Toupleで戻される
        return globals()[func_name](eval(args))

class TextParser(Parser):
    """ base class of Loaders """
    def exec(self):
        """ execute Job
        """
        # Scraping Area
        clipped = self._clip(self.soup, self.selector)
        # Parsing HTML and Creating dict file
        kv1 = [self._parse_data(self.columns, rec) for rec in clipped]
        # Pre Processing
        kv2 = [{col["col_name"]: self._apply_pre_func(col, rec) for col in self.columns} for rec in kv1]
        # Apply format
        kv3 = [{col["col_name"]: self._apply_format(col, rec) for col in self.columns} for rec in kv2]
        # Add Entity ID
        kv4 = [{col["col_name"]: self._add_entity_id(col, rec) for col in self.columns} for rec in kv3]
        # Post Processing
        kv5 = [{col["col_name"]: self._apply_post_func(col, rec) for col in self.columns} for rec in kv4]
        # specific process for cal
        if self.data_type in ["cal"]:
            work = [rec.get("race_id") for rec in kv5 if rec["race_id"] is not None]
            kv5 = sum([['20' + row + str(i + 1).zfill(2) for i in range(12)] for row in work], [])

        return kv5

    def _clip(self, soup, selector):
        # Selector に該当する要素があり、かつ、validator に該当する要素がある場合
        return soup.select(selector) if len(soup.select(self.validator)) > 0 else []

    def _parse_data(self, cols, rec):
        return {c['col_name']: rec.select_one(c['selector']) for c in cols}

class JsonParser(Parser):
    """ base class of Loaders """
    def exec(self):
        """ execute Job
        """
        # Parsing JSON and Creating touple
        clipped = self._create_matrix(json.loads(self.text))
        # Converting touple to dict
        kv1 = [self._add_header(rec_tuple) for rec_tuple in clipped]
        # Pre Processing
        kv2 = [{col["col_name"]: self._apply_pre_func(col, rec) for col in self.columns} for rec in kv1]
        # Apply format
        kv3 = [{col["col_name"]: self._apply_format(col, rec) for col in self.columns} for rec in kv2]
        # Add Entity ID
        kv4 = [{col["col_name"]: self._add_entity_id(col, rec) for col in self.columns} for rec in kv3]
        # Post Processing
        kv5 = [{col["col_name"]: self._apply_post_func(col, rec) for col in self.columns} for rec in kv4]

        return kv5

    def _create_matrix(self, data):
        matrix = [self._parse_json(col, data) for col in self.columns]

        # Blank data check
        if len(sum(matrix, [])) > 2:
            return list(itertools.zip_longest(*matrix))
        else:
            return []

    def _parse_json(self, col, data):
        try:
            return jq.compile(col['selector']).input(data).all()
        except ValueError:
            return []

    def _add_header(self, record):
        keys = [col["col_name"] for col in self.columns]
        return {key: val for key, val in zip(keys, record)}
