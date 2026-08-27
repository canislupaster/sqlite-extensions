# Built SQLite extensions for NPM

[![npm version](https://img.shields.io/npm/v/sqlite-extensions)](https://www.npmjs.com/package/sqlite-extensions)
[![npm downloads](https://img.shields.io/npm/dm/sqlite-extensions)](https://www.npmjs.com/package/sqlite-extensions)
[![npm provenance](https://img.shields.io/badge/npm_provenance-verified-brightgreen)](https://www.npmjs.com/package/sqlite-extensions)
[![build](https://github.com/canislupaster/sqlite-extensions/actions/workflows/build.yml/badge.svg)](https://github.com/canislupaster/sqlite-extensions/actions/workflows/build.yml)
[![license](https://img.shields.io/npm/l/sqlite-extensions)](https://github.com/canislupaster/sqlite-extensions/blob/main/LICENSE)
![extension count](https://img.shields.io/badge/SQLite_extensions-51-blue)

**All 51 [SQLite extensions](https://sqlite.org/src/file/ext/misc) in a convenient NPM package** to save you the trouble of building them yourself.

I've tried to make this as low-code and easy to verify as possible; everything is done and attested by GitHub actions. Take a look in [index.ts](./index.ts) for the supported extensions and API (it's like, two functions).

## Spellfix1 example

Here's an example using the [spellfix extension](https://www.sqlite.org/spellfix1.html) which allows for fuzzy searching in conjunction with [FTS](https://sqlite.org/fts5.html) (usually bundled).
```typescript
import Database from "better-sqlite3";
import {
	extensionPath,
	loadExtension,
	SQLITE_EXTENSIONS,
} from "sqlite-extensions";

const database = new Database("database.sqlite");
// Calls `database.loadExtension(extensionPath(SQLITE_EXTENSIONS.SPELLFIX));`
loadExtension(database, SQLITE_EXTENSIONS.SPELLFIX);

database.exec(`
	CREATE VIRTUAL TABLE vocabulary USING spellfix1;
	INSERT INTO vocabulary(word) VALUES ('dog'), ('cat');
`);

const result = database.prepare(`
	SELECT distance FROM vocabulary WHERE word MATCH 'dot';
`).get();

console.log(result.distance) // -> 75
```

Note the GitHub Actions workflow is loosely based on [better-sqlite3](https://github.com/WiseLibs/better-sqlite3)'s.

## Extension documentation

**This is an unverified LLM-generated dump of the available extensions.** Use at your own risk.

| Status | Extension | What it does | Example | Last updated |
|---|---|---|---|---|
| ![Great](https://geps.dev/progress/100?label=Great) | [fileio](#fileio) | Reads files, writes files, and lists directory contents from SQL. | `SELECT length(readfile('input.bin'));` | 2026-07-05  |
| ![Great](https://geps.dev/progress/100?label=Great) | [series](#series) | Generates integer sequences with start, stop, and step values. | `SELECT value FROM generate_series(1,10,2);` | 2026-06-27  |
| ![Great](https://geps.dev/progress/100?label=Great) | [decimal](#decimal) | Performs arbitrary-precision decimal operations and exact decimal sums. | `SELECT decimal_add('0.1','0.2'), decimal_mul('12.5','8');` | 2026-06-26  |
| ![Great](https://geps.dev/progress/100?label=Great) | [spellfix](#spellfix) | Searches a maintained vocabulary for likely spelling corrections. | `SELECT word, distance FROM vocabulary WHERE word MATCH 'acommodation';` | 2026-06-26  |
| ![Great](https://geps.dev/progress/100?label=Great) | [zipfile](#zipfile) | Reads and writes ZIP archive entries as table rows. | `SELECT name, sz FROM zipfile('bundle.zip');` | 2026-06-26  |
| ![Great](https://geps.dev/progress/100?label=Great) | [percentile](#percentile) | Adds percentile, median, and window aggregate functions. | `SELECT median(score), percentile_cont(score,0.95) FROM results;` | 2026-06-03  |
| ![Great](https://geps.dev/progress/100?label=Great) | [base64](#base64) | Converts a BLOB to Base64 text, or Base64 text to a BLOB. | `SELECT base64(x'4869');` | 2026-04-01  |
| ![Great](https://geps.dev/progress/100?label=Great) | [csv](#csv) | Exposes a CSV file as a virtual table. | `CREATE VIRTUAL TABLE temp.people USING csv(filename='people.csv');` | 2026-04-01  |
| ![Great](https://geps.dev/progress/100?label=Great) | [regexp](#regexp) | Adds POSIX regular-expression matching and the REGEXP operator. | `SELECT 'abc123' REGEXP '^[a-z]+[0-9]+$';` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [fossildelta](#fossildelta) | Creates, applies, inspects, and parses Fossil binary deltas. | `SELECT delta_apply(old_blob, delta_create(old_blob,new_blob));` | 2026-07-06  |
| ![Good](https://geps.dev/progress/80?label=Good)| [amatch](#amatch) | Finds weighted approximate matches from a vocabulary table. | `SELECT word, distance FROM suggestions WHERE word MATCH 'recieve' AND distance<200;` | 2026-06-27  |
| ![Good](https://geps.dev/progress/80?label=Good)| [explain](#explain) | Exposes EXPLAIN bytecode rows as a virtual table. | `SELECT p2 FROM explain('SELECT * FROM sqlite_schema') WHERE opcode='OpenRead';` | 2026-06-23  |
| ![Good](https://geps.dev/progress/80?label=Good)| [unionvtab](#unionvtab) | Presents matching rowid tables from attached databases as one read-only table. | `CREATE VIRTUAL TABLE all_events USING unionvtab('SELECT ''main'', ''events'', 1, 999999');` | 2026-06-23  |
| ![Good](https://geps.dev/progress/80?label=Good)| [compress](#compress) | Compresses and uncompresses BLOBs with zlib. | `SELECT uncompress(compress(CAST('payload' AS BLOB)));` | 2026-06-03  |
| ![Good](https://geps.dev/progress/80?label=Good)| [base85](#base85) | Converts a BLOB to SQLite Base85 text, or back again. It can also validate Base85 text. | `SELECT base85(x'4869'), is_base85('NJUI');` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [completion](#completion) | Returns candidate words for a partially typed SQL statement. | `SELECT candidate FROM completion('sel','select * from ');` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [memstat](#memstat) | Shows connection and global memory counters. | `SELECT name, value, hiwtr FROM sqlite_memstat;` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [sqlar](#sqlar) | Compresses a BLOB only when doing so saves space, and expands it again. | `SELECT sqlar_uncompress(sqlar_compress(readfile('a.txt')), length(readfile('a.txt')));` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [stmtrand](#stmtrand) | Returns repeatable pseudo-random integers within one SQL statement. | `SELECT stmtrand(123), stmtrand(), stmtrand();` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [vfsstat](#vfsstat) | Counts VFS I/O calls and exposes the counters as a virtual table. | `SELECT * FROM vfsstat WHERE count>0;` | 2026-04-01  |
| ![Good](https://geps.dev/progress/80?label=Good)| [sha1](#sha1) | Calculates SHA-1 hashes for values and query results. | `SELECT sha1('hello'), sha1_query('SELECT 1');` | 2026-03-07  |
| ![Good](https://geps.dev/progress/80?label=Good)| [ieee754](#ieee754) | Shows the parts of a floating-point value and converts values to or from an IEEE-754 BLOB. | `SELECT ieee754(45.25), ieee754_to_blob(1.0);` | 2026-02-20  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [fuzzer](#fuzzer) | Generates weighted string changes from a starting word. | `SELECT word, distance FROM f WHERE word MATCH 'colour' AND distance<200 LIMIT 20;` | 2026-06-27  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [closure](#closure) | Walks a parent-child hierarchy and returns IDs and depths. | `SELECT id, depth FROM ct WHERE root=42 AND depth<=2;` | 2026-06-26  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [nextchar](#nextchar) | Finds the next valid characters after a text prefix from an indexed column. | `SELECT next_char('cha','dictionary','word');` | 2026-06-23  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [prefixes](#prefixes) | Returns every prefix of a string, from longest to shortest. | `SELECT prefix FROM prefixes('abcdefg');` | 2026-06-03  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [qpvtab](#qpvtab) | Shows the planner data SQLite passes to a virtual table. | `SELECT * FROM qpvtab(102) WHERE a=19;` | 2026-04-01  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [templatevtab](#templatevtab) | Returns ten fixed rows as a small virtual-table starting point. | `SELECT rowid, a, b FROM templatevtab;` | 2026-04-01  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [vtablog](#vtablog) | Logs calls SQLite makes to a virtual-table module. | `CREATE VIRTUAL TABLE temp.log USING vtablog(rows=25);` | 2026-04-01  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [vtshim](#vtshim) | Provides C APIs that help garbage-collected runtimes clean up virtual tables and cursors. | `SELECT 'Use from C; this extension has no SQL interface';` | 2026-04-01  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [wholenumber](#wholenumber) | Generates integers from 1 through 4,294,967,295. | `SELECT value FROM wholenumber WHERE value<10;` | 2026-04-01  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [tmstmpvfs](#tmstmpvfs) | Adds per-page timestamps and optional write trace files through a VFS. | `.filectrl reserve_bytes 16` | 2026-02-17  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [btreeinfo](#btreeinfo) | Shows estimated size, depth, and row counts for database B-trees. | `SELECT name, nEntry FROM sqlite_btreeinfo ORDER BY nEntry DESC;` | 2025-12-31  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [cksumvfs](#cksumvfs) | Stores and verifies a checksum in reserved bytes of every database page. | `SELECT verify_checksum(data) FROM sqlite_dbpage;` | 2025-08-13  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [zorder](#zorder) | Encodes integer coordinates as a Morton, or Z-order, key and can decode the key. | `SELECT zorder(1,2,3,4);` | 2025-08-05  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [shathree](#shathree) | Calculates SHA-3 hashes for values, groups, and query results. | `SELECT sha3('hello',256);` | 2025-02-27  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [uint](#uint) | Sorts runs of digits in text by numeric value, so file2 comes before file10. | `SELECT name FROM t ORDER BY name COLLATE uint;` | 2025-02-27  |
| ![Ok](https://geps.dev/progress/65?label=Ok) | [totype](#totype) | Converts values to integer or real only when the conversion meets its stricter rules. | `SELECT tointeger('123'), toreal('1.25e2');` | 2025-02-25  |
| ![Ok](https://geps.dev/progress/50?label=Ok) | [randomjson](#randomjson) | Generates repeatable JSON or JSON5 text from a numeric seed. | `SELECT random_json(1), random_json5(1);` | 2023-12-19  |
| ![Ok](https://geps.dev/progress/50?label=Ok) | [stmt](#stmt) | Lists prepared statements and counters such as scans, sorts, steps, and memory use. | `SELECT sql, nscan, nsort, nstep FROM sqlite_stmt;` | 2023-10-06  |
| ![Ok](https://geps.dev/progress/50?label=Ok) | [basexx](#basexx) | Builds the Base64 and Base85 extensions into one loadable module. | `SELECT base64(x'4869'), base85(x'4869');` | 2023-05-13  |
| ![Ok](https://geps.dev/progress/50?label=Ok) | [uuid](#uuid) | Generates UUIDv4 values and converts UUID text and BLOBs. | `SELECT uuid(), uuid_str(uuid_blob(uuid()));` | 2020-01-07  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [appendvfs](#appendvfs) | Uses a VFS that can find an SQLite database appended to another file. | `.open host-file` | 2021-06-15  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [urifuncs](#urifuncs) | Reports a database filename, URI options, and related paths. | `SELECT sqlite3_db_filename('main'), sqlite3_uri_parameter('main','mode');` | 2020-01-14  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [rot13](#rot13) | Adds a ROT13 function and collation for ASCII text. | `SELECT rot13('Uryyb');` | 2020-01-08  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [blobio](#blobio) | Reads or overwrites a range in an existing BLOB. | `SELECT readblob('main','files','data',42,0,16);` | 2019-05-27  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [remember](#remember) | Passes an integer through SQL and writes it through a C pointer supplied by the host program. | `UPDATE counter SET n=remember(n,$ptr)+1 WHERE id=1;` | 2017-07-17  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [anycollseq](#anycollseq) | Lets SQLite open schemas that name unknown collations by treating them as BINARY. | `SELECT name FROM t ORDER BY name COLLATE legacy_collation;` | 2017-04-16  |
| ![Poor](https://geps.dev/progress/30?label=Poor) | [showauth](#showauth) | Prints every SQLite authorization request to standard output. | `SELECT * FROM t;` | 2014-09-21  |
| ![Unmaintained](https://geps.dev/progress/10?label=Unmaintained) | [noop](#noop) | Provides identity functions with different SQLite flags for tests. | `SELECT noop_i('value'), multitype_text(42);` | 2024-01-20  |
| ![Unmaintained](https://geps.dev/progress/10?label=Unmaintained) | [eval](#eval) | Runs SQL text and joins the result values into text. | `SELECT eval('SELECT 1 UNION ALL SELECT 2', ',');` | 2020-01-07  |

- **Status** combines recency and estimated popularity. The table is sorted by status, then by last update, then by extension name. It gives up to three points for the last source update (2026: 3, 2025: 2, 2023–2024: 1, older: 0) and up to two for popularity. Green is 4–5 points, yellow is 2–3, and red is 0–1.
- **Reliability** is a source-review judgment, not a security audit.
- **Popularity** is a relative estimate. It is not usage or download data.
- **Last updated** is the most recent commit for the source file in the nested SQLite checkout, checked on 2026-08-28.

### anycollseq

**What it does:** Lets SQLite open schemas that name unknown collations by treating them as BINARY.

```sql
SELECT name FROM t ORDER BY name COLLATE legacy_collation;
```

**Status:** Last updated: 2017-04-16. Reliability: **Good for recovery and inspection; do not use it when the original collation affects correctness**. Popularity: **Low**.

### base64

**What it does:** Converts a BLOB to Base64 text, or Base64 text to a BLOB.

```sql
SELECT base64(x'4869');
```

**Status:** Last updated: 2026-04-01. Reliability: **Good. It validates types and handles SQLite size limits**. Popularity: **Medium-high**.

### base85

**What it does:** Converts a BLOB to SQLite Base85 text, or back again. It can also validate Base85 text.

```sql
SELECT base85(x'4869'), is_base85('NJUI');
```

**Status:** Last updated: 2026-04-01. Reliability: **Good. It has separate encode, decode, and validation paths**. Popularity: **Medium**.

### basexx

**What it does:** Builds the Base64 and Base85 extensions into one loadable module.

```sql
SELECT base64(x'4869'), base85(x'4869');
```

**Status:** Last updated: 2023-05-13. Reliability: **Good for packaging. It is a small wrapper around the two extensions**. Popularity: **Low-medium**.

### completion

**What it does:** Returns candidate words for a partially typed SQL statement.

```sql
SELECT candidate FROM completion('sel','select * from ');
```

**Status:** Last updated: 2026-04-01. Reliability: **Good for interactive tools. It favors useful suggestions over speed**. Popularity: **Medium**.

### ieee754

**What it does:** Shows the parts of a floating-point value and converts values to or from an IEEE-754 BLOB.

```sql
SELECT ieee754(45.25), ieee754_to_blob(1.0);
```

**Status:** Last updated: 2026-02-20. Reliability: **Good for diagnostics and precision work. It is not a replacement for decimal math**. Popularity: **Medium**.

### memstat

**What it does:** Shows connection and global memory counters.

```sql
SELECT name, value, hiwtr FROM sqlite_memstat;
```

**Status:** Last updated: 2026-04-01. Reliability: **Good diagnostic code. Results are a point-in-time view**. Popularity: **Medium**.

### randomjson

**What it does:** Generates repeatable JSON or JSON5 text from a numeric seed.

```sql
SELECT random_json(1), random_json5(1);
```

**Status:** Last updated: 2023-12-19. Reliability: **Good for tests. It is not a security random-number generator**. Popularity: **Medium**.

### remember

**What it does:** Passes an integer through SQL and writes it through a C pointer supplied by the host program.

```sql
UPDATE counter SET n=remember(n,$ptr)+1 WHERE id=1;
```

**Status:** Last updated: 2017-07-17. Reliability: **Safe for its narrow demo purpose. It needs host-side pointer binding**. Popularity: **Low**.

### rot13

**What it does:** Adds a ROT13 function and collation for ASCII text.

```sql
SELECT rot13('Uryyb');
```

**Status:** Last updated: 2020-01-08. Reliability: **Good for a small text example. ROT13 is not encryption**. Popularity: **Low**.

### showauth

**What it does:** Prints every SQLite authorization request to standard output.

```sql
SELECT * FROM t;
```

**Status:** Last updated: 2014-09-21. Reliability: **Debug-only. It reports requests but does not enforce policy**. Popularity: **Low**.

### sqlar

**What it does:** Compresses a BLOB only when doing so saves space, and expands it again.

```sql
SELECT sqlar_uncompress(sqlar_compress(readfile('a.txt')), length(readfile('a.txt')));
```

**Status:** Last updated: 2026-04-01. Reliability: **Good for its SQL Archive use case. It requires zlib**. Popularity: **Medium**.

### stmt

**What it does:** Lists prepared statements and counters such as scans, sorts, steps, and memory use.

```sql
SELECT sql, nscan, nsort, nstep FROM sqlite_stmt;
```

**Status:** Last updated: 2023-10-06. Reliability: **Good diagnostic tool. Output applies only to the current connection**. Popularity: **Medium**.

### stmtrand

**What it does:** Returns repeatable pseudo-random integers within one SQL statement.

```sql
SELECT stmtrand(123), stmtrand(), stmtrand();
```

**Status:** Last updated: 2026-04-01. Reliability: **Good for repeatable tests. It is not cryptographic**. Popularity: **Medium**.

### totype

**What it does:** Converts values to integer or real only when the conversion meets its stricter rules.

```sql
SELECT tointeger('123'), toreal('1.25e2');
```

**Status:** Last updated: 2025-02-25. Reliability: **Good, but conversion edge cases deserve tests in your own data pipeline**. Popularity: **Medium**.

### uint

**What it does:** Sorts runs of digits in text by numeric value, so file2 comes before file10.

```sql
SELECT name FROM t ORDER BY name COLLATE uint;
```

**Status:** Last updated: 2025-02-27. Reliability: **Good for ASCII digits. It does not treat signs, decimals, or exponents as numbers**. Popularity: **Medium**.

### urifuncs

**What it does:** Reports a database filename, URI options, and related paths.

```sql
SELECT sqlite3_db_filename('main'), sqlite3_uri_parameter('main','mode');
```

**Status:** Last updated: 2020-01-14. Reliability: **Useful for testing and inspection. Results depend on how the database was opened**. Popularity: **Low**.

### vtshim

**What it does:** Provides C APIs that help garbage-collected runtimes clean up virtual tables and cursors.

```sql
SELECT 'Use from C; this extension has no SQL interface';
```

**Status:** Last updated: 2026-04-01. Reliability: **Specialized lifecycle code. It is useful only to virtual-table implementers**. Popularity: **Low**.

### zorder

**What it does:** Encodes integer coordinates as a Morton, or Z-order, key and can decode the key.

```sql
SELECT zorder(1,2,3,4);
```

**Status:** Last updated: 2025-08-05. Reliability: **Good with input checks. A signed 64-bit result limits coordinate width and dimensions**. Popularity: **Low-medium**.

### appendvfs

**What it does:** Uses a VFS that can find an SQLite database appended to another file.

```sql
.open host-file
```

**Status:** Last updated: 2021-06-15. Reliability: **Good for a specialized packaging pattern. Combined files are limited to 1 GiB**. Popularity: **Low**.

### btreeinfo

**What it does:** Shows estimated size, depth, and row counts for database B-trees.

```sql
SELECT name, nEntry FROM sqlite_btreeinfo ORDER BY nEntry DESC;
```

**Status:** Last updated: 2025-12-31. Reliability: **Useful estimates, not exact measurements. It also needs sqlite_dbpage**. Popularity: **Low-medium**.

### cksumvfs

**What it does:** Stores and verifies a checksum in reserved bytes of every database page.

```sql
SELECT verify_checksum(data) FROM sqlite_dbpage;
```

**Status:** Last updated: 2025-08-13. Reliability: **Strong integrity feature with clear setup limits. It needs reserved page bytes**. Popularity: **Medium**.

### csv

**[Official docs](https://sqlite.org/csv.html)**

**What it does:** Exposes a CSV file as a virtual table.

```sql
CREATE VIRTUAL TABLE temp.people USING csv(filename='people.csv');
```

**Status:** Last updated: 2026-04-01. Reliability: **Good practical CSV reader. Use another tool for complex ETL workflows**. Popularity: **High**.

### eval

**What it does:** Runs SQL text and joins the result values into text.

```sql
SELECT eval('SELECT 1 UNION ALL SELECT 2', ',');
```

**Status:** Last updated: 2020-01-07. Reliability: **Works as designed, but never pass untrusted SQL to it**. Popularity: **Medium**.

### noop

**What it does:** Provides identity functions with different SQLite flags for tests.

```sql
SELECT noop_i('value'), multitype_text(42);
```

**Status:** Last updated: 2024-01-20. Reliability: **Test fixture, not production functionality**. Popularity: **Low**.

### qpvtab

**What it does:** Shows the planner data SQLite passes to a virtual table.

```sql
SELECT * FROM qpvtab(102) WHERE a=19;
```

**Status:** Last updated: 2026-04-01. Reliability: **Good developer tool. It describes planning behavior, not application data**. Popularity: **Low**.

### regexp

**What it does:** Adds POSIX regular-expression matching and the REGEXP operator.

```sql
SELECT 'abc123' REGEXP '^[a-z]+[0-9]+$';
```

**Status:** Last updated: 2026-04-01. Reliability: **Good bounded matcher. Its syntax is smaller than PCRE**. Popularity: **High**.

### sha1

**What it does:** Calculates SHA-1 hashes for values and query results.

```sql
SELECT sha1('hello'), sha1_query('SELECT 1');
```

**Status:** Last updated: 2026-03-07. Reliability: **Fine for legacy IDs and checksums. Do not use SHA-1 for new collision-resistant security work**. Popularity: **Medium**.

### shathree

**What it does:** Calculates SHA-3 hashes for values, groups, and query results.

```sql
SELECT sha3('hello',256);
```

**Status:** Last updated: 2025-02-27. Reliability: **Good modern hash support. Only run trusted SQL through query hashing**. Popularity: **Medium**.

### templatevtab

**What it does:** Returns ten fixed rows as a small virtual-table starting point.

```sql
SELECT rowid, a, b FROM templatevtab;
```

**Status:** Last updated: 2026-04-01. Reliability: **Teaching code, not an application feature**. Popularity: **Low**.

### tmstmpvfs

**What it does:** Adds per-page timestamps and optional write trace files through a VFS.

```sql
.filectrl reserve_bytes 16
```

**Status:** Last updated: 2026-02-17. Reliability: **Specialized tracing tool. It needs reserved page bytes and careful operations setup**. Popularity: **Low**.

### uuid

**What it does:** Generates UUIDv4 values and converts UUID text and BLOBs.

```sql
SELECT uuid(), uuid_str(uuid_blob(uuid()));
```

**Status:** Last updated: 2020-01-07. Reliability: **Good validation and conversion support for common UUID use cases**. Popularity: **High**.

### vfsstat

**What it does:** Counts VFS I/O calls and exposes the counters as a virtual table.

```sql
SELECT * FROM vfsstat WHERE count>0;
```

**Status:** Last updated: 2026-04-01. Reliability: **Useful for profiling. Counters can be inaccurate with concurrent access**. Popularity: **Low-medium**.

### vtablog

**What it does:** Logs calls SQLite makes to a virtual-table module.

```sql
CREATE VIRTUAL TABLE temp.log USING vtablog(rows=25);
```

**Status:** Last updated: 2026-04-01. Reliability: **Debug-only and stdout-based. It is not a production table module**. Popularity: **Low**.

### closure

**What it does:** Walks a parent-child hierarchy and returns IDs and depths.

```sql
SELECT id, depth FROM ct WHERE root=42 AND depth<=2;
```

**Status:** Last updated: 2026-06-26. Reliability: **Experimental and disabled unless built for SQLite tests. Prefer recursive CTEs for new work**. Popularity: **Very low**.

### decimal

**What it does:** Performs arbitrary-precision decimal operations and exact decimal sums.

```sql
SELECT decimal_add('0.1','0.2'), decimal_mul('12.5','8');
```

**Status:** Last updated: 2026-06-26. Reliability: **Good for exact decimals. Very large inputs can be slower by design**. Popularity: **Medium-high**.

### fileio

**What it does:** Reads files, writes files, and lists directory contents from SQL.

```sql
SELECT length(readfile('input.bin'));
```

**Status:** Last updated: 2026-07-05. Reliability: **Good platform-aware utility. Only load it when SQL users are trusted; it can access the filesystem**. Popularity: **High**.

### fuzzer

**What it does:** Generates weighted string changes from a starting word.

```sql
SELECT word, distance FROM f WHERE word MATCH 'colour' AND distance<200 LIMIT 20;
```

**Status:** Last updated: 2026-06-27. Reliability: **Use small distance limits. Time and memory grow quickly as the limit increases**. Popularity: **Low**.

### nextchar

**What it does:** Finds the next valid characters after a text prefix from an indexed column.

```sql
SELECT next_char('cha','dictionary','word');
```

**Status:** Last updated: 2026-06-23. Reliability: **Useful but specialized. Do not pass untrusted SQL expressions as its table or filter arguments**. Popularity: **Very low**.

### percentile

**What it does:** Adds percentile, median, and window aggregate functions.

```sql
SELECT median(score), percentile_cont(score,0.95) FROM results;
```

**Status:** Last updated: 2026-06-03. Reliability: **Good. Large groups and windows use memory for sorting**. Popularity: **High**.

### series

**[Official docs](https://sqlite.org/series.html)**

**What it does:** Generates integer sequences with start, stop, and step values.

```sql
SELECT value FROM generate_series(1,10,2);
```

**Status:** Last updated: 2026-06-27. Reliability: **Mature and planner-aware. Always give bounds to avoid a very large scan**. Popularity: **Very high**.

### unionvtab

**[Official docs](https://sqlite.org/swarmvtab.html)**

**What it does:** Presents matching rowid tables from attached databases as one read-only table.

```sql
CREATE VIRTUAL TABLE all_events USING unionvtab('SELECT ''main'', ''events'', 1, 999999');
```

**Status:** Last updated: 2026-06-23. Reliability: **Good when source tables meet its strict schema and rowid rules. Swarm mode adds file-management complexity**. Popularity: **Medium**.

### blobio

**What it does:** Reads or overwrites a range in an existing BLOB.

```sql
SELECT readblob('main','files','data',42,0,16);
```

**Status:** Last updated: 2019-05-27. Reliability: **Good for debugging. Writes change existing BLOB ranges in place**. Popularity: **Low**.

### wholenumber

**What it does:** Generates integers from 1 through 4,294,967,295.

```sql
SELECT value FROM wholenumber WHERE value<10;
```

**Status:** Last updated: 2026-04-01. Reliability: **Simple and reliable. Always add bounds because its full range is large**. Popularity: **Low**.

### amatch

**What it does:** Finds weighted approximate matches from a vocabulary table.

```sql
SELECT word, distance FROM suggestions WHERE word MATCH 'recieve' AND distance<200;
```

**Status:** Last updated: 2026-06-27. Reliability: **Good for a specialized tool. It needs vocabulary indexes and a low distance bound**. Popularity: **Low-medium**.

### compress

**What it does:** Compresses and uncompresses BLOBs with zlib.

```sql
SELECT uncompress(compress(CAST('payload' AS BLOB)));
```

**Status:** Last updated: 2026-06-03. Reliability: **Small and conventional. It needs zlib at build time**. Popularity: **Medium**.

### explain

**What it does:** Exposes EXPLAIN bytecode rows as a virtual table.

```sql
SELECT p2 FROM explain('SELECT * FROM sqlite_schema') WHERE opcode='OpenRead';
```

**Status:** Last updated: 2026-06-23. Reliability: **Good for inspection and tests. Opcode output can change between SQLite versions**. Popularity: **Medium among SQLite developers**.

### fossildelta

**What it does:** Creates, applies, inspects, and parses Fossil binary deltas.

```sql
SELECT delta_apply(old_blob, delta_create(old_blob,new_blob));
```

**Status:** Last updated: 2026-07-06. Reliability: **Good for its established delta format. It is not a general text diff API**. Popularity: **Low-medium**.

### prefixes

**What it does:** Returns every prefix of a string, from longest to shortest.

```sql
SELECT prefix FROM prefixes('abcdefg');
```

**Status:** Last updated: 2026-06-03. Reliability: **Small and reliable. It works on bytes, not user-perceived Unicode characters**. Popularity: **Low**.

### spellfix

**[Official docs](https://sqlite.org/spellfix1.html)**

**What it does:** Searches a maintained vocabulary for likely spelling corrections.

```sql
SELECT word, distance FROM vocabulary WHERE word MATCH 'acommodation';
```

**Status:** Last updated: 2026-06-26. Reliability: **Feature-rich and solid. Test its language settings with your own vocabulary**. Popularity: **Medium-high**.

### zipfile

**[Official docs](https://sqlite.org/zipfile.html)**

**What it does:** Reads and writes ZIP archive entries as table rows.

```sql
SELECT name, sz FROM zipfile('bundle.zip');
```

**Status:** Last updated: 2026-06-26. Reliability: **Good for standard ZIP files. It does not support ZIP64, encryption, split archives, or non-deflate compression**. Popularity: **High**.
