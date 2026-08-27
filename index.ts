import type { Database } from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { SQLITE_EXTENSIONS as MANIFEST_SQLITE_EXTENSIONS } from "./manifest";

/** Names of all SQLite extensions.
 *
 * The docs for each extension are taken wholesale from its source code via some
 * simple parsing. See build_manifest.py.  */
export const SQLITE_EXTENSIONS: typeof MANIFEST_SQLITE_EXTENSIONS =
	MANIFEST_SQLITE_EXTENSIONS;

/**
 * Deduce the path to the built extensions. This is almost directly from
 * better-sqlite3:
 * https://github.com/WiseLibs/better-sqlite3/blob/f8e2d541208281368129929a96f70f937c0735ef/lib/binding.js#L41
 *
 * @returns The path to the prebuilt extensions for this platform /
 * architecture.
 */
function getPrebuildPath() {
	const isMusl = process.platform == "linux"
		&& (process.report.getReport() as {
				header?: { glibcVersionRuntime?: string };
			}).header?.glibcVersionRuntime == null;
	const target = `${isMusl ? "linuxmusl" : process.platform}-${process.arch}`;
	const prebuildPath = path.join(import.meta.dirname, target);
	if (fs.existsSync(prebuildPath)) {
		return prebuildPath;
	}
	return null;
}

/** Possible SQLite extension keys. Use SQLITE_EXTENSIONS to get these. */
export type SqliteExtension =
	typeof SQLITE_EXTENSIONS[keyof typeof SQLITE_EXTENSIONS];

/**
 * Get the path to the SQLite extension for the current platform and
 * architecture.
 *
 * @param extension - The name of the extension to resolve.
 * @returns The path to the extension's shared library (.so/.dll/.dylib file).
 * @throws If the extension is unsupported or no compatible prebuild is found.
 */
export function extensionPath(extension: SqliteExtension): string {
	if (!Object.values(SQLITE_EXTENSIONS).includes(extension)) {
		throw new Error("Unsupported extension");
	}
	const prebuildPath = getPrebuildPath();
	if (prebuildPath == null) {
		throw new Error("Unsupported platform / architecture");
	}
	const extensionSuffix = process.platform == "win32"
		? "dll"
		: process.platform == "darwin"
		? "dylib"
		: "so";
	return path.join(prebuildPath, `${extension}.${extensionSuffix}`);
}

/**
 * Load an extension into a better-sqlite3 `Database`.
 *
 * @param database - The database to load the extension into.
 * @param extension - The name of the extension.
 * @throws If the extension cannot be resolved or loaded.
 */
export function loadExtension(
	database: Database,
	extension: SqliteExtension,
): void {
	database.loadExtension(extensionPath(extension));
}
