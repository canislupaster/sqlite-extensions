import Database from "better-sqlite3";
import assert from "node:assert";
import { existsSync } from "node:fs";
import { readdir } from "node:fs/promises";
import path from "node:path";
import test, { suite } from "node:test";
import {
	extensionPath,
	loadExtension,
	SQLITE_EXTENSIONS,
} from "sqlite-extensions";

test("extension list has correct length", async () => {
	for (const entry of await readdir("./lib", { withFileTypes: true })) {
		if (entry.isDirectory()) {
			assert.deepEqual(
				Object.values(SQLITE_EXTENSIONS).toSorted(),
				(await readdir(path.join(entry.parentPath, entry.name))).map(file =>
					path.basename(file, path.extname(file))
				).sort(),
			);
		}
	}
});

suite("load all extensions", () => {
	for (const extension of Object.values(SQLITE_EXTENSIONS)) {
		test(`loads ${extension}`, () => {
			assert(existsSync(extensionPath(extension)));
			const database = new Database(":memory:");
			try {
				loadExtension(database, extension);
			} finally {
				database.close();
			}
		});
	}
});

test("spellfix extension works", () => {
	const database = new Database(":memory:");
	try {
		loadExtension(database, "spellfix");

		database.exec(`
			CREATE VIRTUAL TABLE vocabulary USING spellfix1;
			INSERT INTO vocabulary(word) VALUES
				('hello'),
				('help'),
				('shell'),
				('world');
		`);

		assert.deepEqual(
			database.prepare(`
				SELECT word, distance
				FROM vocabulary
				WHERE word MATCH 'helo'
				ORDER BY distance, word
			`).all(),
			// Scores come from SQLite's spellfix1 edit-distance rules. Missing a repeat
			// is +10, and substitution is +100 (the max) in this case.
			// https://sqlite.org/spellfix1.html
			[{ word: "hello", distance: 10 }, { word: "help", distance: 100 }],
		);
	} finally {
		database.close();
	}
});
