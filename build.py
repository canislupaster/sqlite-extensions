import os
import pathlib
import shlex
import subprocess
import sys

import build_manifest


def main() -> None:
    """Build the SQLite extensions or their docs in ./sqlite into ./build.

    This should only be run from the GH build workflow, see
    .github/workflows/build.yml
    """

    target = sys.argv[1]
    is_windows = target.startswith("win32-")
    is_macos = target.startswith("darwin-")

    # Install platform-specific dependencies.
    match target:
        case "manifest":
            build_manifest.build_manifest()
            return
        case "linux-arm64" | "linux-x64":
            subprocess.check_call(
                "sudo apt install -y build-essential zlib1g-dev", shell=True
            )
        case "linuxmusl-arm64" | "linuxmusl-x64":
            subprocess.check_call(
                "apk add --no-cache make gcc make libc-dev zlib-dev", shell=True
            )
        case "win32-x64" | "win32-arm64":
            vcpkg_triplet = (
                "arm64-windows-static-md"
                if target == "win32-arm64"
                else "x64-windows-static-md"
            )
            subprocess.check_call(rf'vcpkg install "zlib:{vcpkg_triplet}"', shell=True)

    build_dir = (pathlib.Path("build") / "lib" / target).resolve()
    build_dir.mkdir(parents=True)
    extensions = build_manifest.collect_extensions()
    os.chdir("sqlite")

    # Configure SQLite.
    if is_windows:
        subprocess.check_call(
            "nmake /f Makefile.msc sqlite3.h sqlite3ext.h", shell=True
        )
        # Fix for the fileio.c extension is very recent, fetch and apply it.
        subprocess.check_call(
            "git fetch origin 63984b6ab762c97d6377013ab33b9116e12aa113"
            " && git restore --source=63984b6ab762c97d6377013ab33b9116e12aa113 ext/misc/fileio.c",
            shell=True,
        )
    else:
        subprocess.check_call("./configure")
        subprocess.check_call("make sqlite3.h sqlite3ext.h", shell=True)

    # Build each extension's source file using the built headers.
    for extension in extensions:
        # This is defined in sqlite3ext.h and defines the SQLite API constant. Any
        # source files without this are probably not extensions and should be
        # skipped.
        if "SQLITE_EXTENSION_INIT1" not in extension.read_text(errors="replace"):
            continue

        if is_windows:
            output = build_dir / extension.with_suffix(".dll").name
            vcpkg_dir = (
                pathlib.Path(os.environ["VCPKG_INSTALLATION_ROOT"])
                / "installed"
                / vcpkg_triplet
            )
            command = [
                *shlex.split("cl /nologo /LD /O2 /I."),
                f"/I{vcpkg_dir / 'include'}",
                extension,
                "/link",
                f"/LIBPATH:{vcpkg_dir / 'lib'}",
                "zs.lib",
                f"/OUT:{output}",
            ]

            # There's a small windows compatibility bug in the percentile addon
            # introduced by ef7c69 (Git) / 831e2b (Fossil), and we have to
            # export this manually.
            if extension.stem == "percentile":
                command.append("/EXPORT:sqlite3_percentile_init")

            subprocess.check_call(command)
        else:
            if is_macos:
                output = build_dir / extension.with_suffix(".dylib").name
                command = "cc -dynamiclib -undefined dynamic_lookup -lz -I. -O2"
            else:
                output = build_dir / extension.with_suffix(".so").name
                command = "gcc -shared -fPIC -lz -I. -O2"

            subprocess.check_call([*shlex.split(command), extension, "-o", output])

        print(f"Built {output.name!r}")


if __name__ == "__main__":
    main()
