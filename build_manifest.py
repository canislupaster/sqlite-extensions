import pathlib
import re
from collections.abc import Mapping, Sequence

# Map SQLite filenames to CONSTANT_CASE enum values.
NAME_MAPPING: Mapping[str, str] = {
    "blobio": "BLOB_IO",
    "amatch": "A_MATCH",
    "nextchar": "NEXT_CHAR",
    "sha1": "SHA1",
    "uint": "UINT",
    "anycollseq": "ANY_COLL_SEQ",
    "decimal": "DECIMAL",
    "noop": "NOOP",
    "shathree": "SHA3",
    "unionvtab": "UNION_VTAB",
    "appendvfs": "APPEND_VFS",
    "showauth": "SHOW_AUTH",
    "urifuncs": "URI_FUNCS",
    "base64": "BASE64",
    "eval": "EVAL",
    "spellfix": "SPELLFIX",
    "uuid": "UUID",
    "base85": "BASE85",
    "explain": "EXPLAIN",
    "percentile": "PERCENTILE",
    "sqlar": "SQLAR",
    "basexx": "BASEXX",
    "fileio": "FILE_IO",
    "prefixes": "PREFIXES",
    "vfsstat": "VFS_STAT",
    "btreeinfo": "BTREE_INFO",
    "fossildelta": "FOSSIL_DELTA",
    "qpvtab": "QP_VTAB",
    "stmt": "STMT",
    "cksumvfs": "CKSUM_VFS",
    "fuzzer": "FUZZER",
    "randomjson": "RANDOM_JSON",
    "stmtrand": "STMT_RAND",
    "vtablog": "VTAB_LOG",
    "closure": "CLOSURE",
    "ieee754": "IEEE754",
    "regexp": "REGEXP",
    "vtshim": "VT_SHIM",
    "completion": "COMPLETION",
    "memstat": "MEM_STAT",
    "remember": "REMEMBER",
    "templatevtab": "TEMPLATE_VTAB",
    "wholenumber": "WHOLE_NUMBER",
    "compress": "COMPRESS",
    "rot13": "ROT13",
    "tmstmpvfs": "TMSTMP_VFS",
    "zipfile": "ZIP_FILE",
    "csv": "CSV",
    "series": "SERIES",
    "totype": "TO_TYPE",
    "zorder": "Z_ORDER",
}


def collect_extensions() -> Sequence[pathlib.Path]:
    """Find SQLite extension C source files in ./sqlite/ext/misc."""
    return [
        extension.resolve()
        for extension in pathlib.Path("sqlite/ext/misc").glob("*.c")
        # This is defined in sqlite3ext.h and defines the SQLite API constant.
        # Any source files without this are probably not extensions and should
        # be skipped.
        if "SQLITE_EXTENSION_INIT1" in extension.read_text(errors="replace")
    ]


def build_manifest() -> None:
    """Create the manifest file with documentation for each extension."""

    out = "export const SQLITE_EXTENSIONS = {\n"

    for extension in collect_extensions():
        # Collect documentation comments. See ext/misc/*.c in the SQLite repo
        # for examples.
        lines = extension.read_text().splitlines()
        assert lines[0] == "/*"
        skipped_separator = False

        out += f"\t/** # {extension.name}\n"
        for comment in lines[1:]:
            if "*/" in comment:
                # */, **/, etc. We didn't miss any content.
                assert re.fullmatch(r"\**/", comment)
                break

            if skipped_separator:
                # Convert this from "** comment" to " * comment" (JSDoc).
                clean_comment = re.sub(r"^\**", "", comment)
                out += f"\t *{clean_comment}\n"

            if comment.startswith("*" * 10):
                skipped_separator = True

        out += "\t */\n"
        out += f"\t{NAME_MAPPING[extension.stem]}: {extension.stem!r},\n"

        print(f"Parsed {extension.name!r}")

    out += "} as const;\n"

    # This will be copied into the root directory by future GitHub actions.
    pathlib.Path("build").mkdir(parents=True)
    pathlib.Path("build/manifest.ts").write_text(out)
