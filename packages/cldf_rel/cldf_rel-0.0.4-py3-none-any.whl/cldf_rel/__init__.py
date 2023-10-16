import logging
import pathlib

from pycldf import Dataset

log = logging.getLogger(__name__)

__author__ = "Florian Matter"
__email__ = "flmt@mailbox.org"
__version__ = "0.0.4"


def table_label(table):
    if hasattr(table, "url"):
        return str(table.url).replace(".csv", "")
    return str(table).replace(".csv", "")


class Record:
    def __init__(self, dic, table, dataset, orm=None):
        self.dataset = dataset
        self.fields = dic
        self.table = table
        self.label = table.label
        if orm:
            self.cldf = orm.cldf
            self.related = orm.related

    def __getattr__(self, target):
        if target in self.backrefs:
            backrefs = []
            col, tcol = self.backrefs[target]
            for rec in self.dataset[target].records.values():
                if rec[tcol] == self[col]:
                    backrefs.append(rec)
            return backrefs
        if target in self.assocs:
            col = self.assocs[target]
            table, tcol = self.foreignkeys[self.assocs[target]]
            if not self[col]:
                return None
            if isinstance(self[col], list):
                target = self[col]
                res = []
            else:
                target = [self[col]]
                res = None
            for rec in self.dataset[table].records.values():
                if rec[tcol] in target:
                    if res is None:
                        return rec
                    else:
                        res.append(rec)
            if res:
                return res
        raise AttributeError(target)

    @property
    def backrefs(self):
        return self.table.backrefs

    @property
    def foreignkeys(self):
        return self.table.foreignkeys

    @property
    def assocs(self):
        out = {}
        for field in self.dataset.foreignkeys.get(self.label, {}).keys():
            out[field.replace("_ID", "").lower()] = field
        return out

    def items(self):
        return self.fields.items()

    def get(self, val, optional_value=None):
        return self.fields.get(val, optional_value)

    def __repr__(self):
        return (
            f"{self.table.label}: ["
            + ",".join([f"{k}: {v}" for k, v in self.fields.items()])
            + "]"
        )

    @property
    def single_refs(self):
        out = {}
        for key in self.assocs:
            res = getattr(self, key)
            if not isinstance(res, list):
                out[key] = res
        return out

    @property
    def multi_refs(self):
        out = {}
        for key in self.assocs:
            res = getattr(self, key)
            if isinstance(res, list):
                out[key+"s"] = res
        for key in self.backrefs:
            out[key] = getattr(self, key)
        return out

    def __getitem__(self, item):
        return self.fields[item]


class Table:
    """A table holding entities of a specific kind, e.g. languages or morphemes.

    Args:
        records (list): List of table records (dicts)
        label (str): Human-readable label of the table (languages, morphemes).
        name (str): LanguageTable, morphemes.csv.
        dataset (CLDFDataset): The dataset to which the table belongs.
        orm_records (list, optional): If the table is implemented in the [pycldf ORM module](https://github.com/cldf/pycldf/blob/master/src/pycldf/orm.py),
            dataset.objects("<TableName") can be passed.
    """

    def __init__(self, records, label, name, dataset, orm_records=None):
        orm_entities = {}
        if orm_records:
            for rec in orm_records:
                orm_entities[rec.id] = rec
        self.dataset = dataset
        self.label = label
        self.records = {}
        self.name = name
        for rec in records:
            self.records[rec["ID"]] = Record(
                rec, self, dataset, orm=orm_entities.get(rec.get("ID"))
            )

    @property
    def backrefs(self):
        """Returns all backrefs for this table."""
        return self.dataset.backrefs.get(self.label, {})

    @property
    def foreignkeys(self):
        return self.dataset.foreignkeys.get(self.label, {})

    def __getitem__(self, item):
        return self.records[item]


def get_table_name(table):
    if table.asdict().get("dc:conformsTo", "").endswith("Table"):
        return table.asdict()["dc:conformsTo"].split("#")[-1]
    return str(table.url)

class CLDFDataset:
    tables: dict = {}
    foreignkeys: dict = {}
    backrefs: dict = {}
    dataset = None
    orm: bool = False

    def __init__(self, metadata, orm=False):
        self.tables = {}
        self.foreignkeys = {}
        self.backrefs = {}
        self.orm = orm
        if isinstance(metadata, Dataset):
            self.dataset = metadata
        elif isinstance(metadata, str) or isinstance(metadata, pathlib.Path):
            self.dataset = Dataset.from_metadata(metadata)
        else:
            raise ValueError(metadata)
        for table in self.dataset.tables:
            label = table_label(table)
            fkeys = table.tableSchema.foreignKeys
            if not fkeys:
                continue
            self.foreignkeys[label] = {}
            for key in fkeys:
                target = table_label(key.reference.resource)
                col = key.columnReference[0]
                self.foreignkeys.setdefault(label, {})
                self.backrefs.setdefault(target, {})
                fcol = key.reference.columnReference[0]
                self.foreignkeys[label][col] = (target, fcol)
                self.backrefs[target][label] = (fcol, col)

        for table in self.dataset.tables:
            orm_records = None
            name = get_table_name(table)
            if name.endswith("Table"):
                if self.orm:
                    try:
                        orm_records = self.dataset.objects(name)
                    except KeyError:
                        pass
            label = table_label(table)
            self.tables[label] = Table(
                records=self.dataset.iter_rows(table),
                orm_records=orm_records,
                label=label,
                name=name,
                dataset=self,
            )

    def __getitem__(self, item):
        return self.tables[item]
