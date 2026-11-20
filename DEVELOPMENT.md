# Local development

If you're using Nix, `nix develop` (or direnv) sets up `@local/chordish` automatically.

If not, ~~go install it~~ symlink this repo into Typst's local packages directory under `chordish/<version>` (matching the version in `typst.toml`):

- **Linux:** `~/.local/share/typst/packages/local/chordish/<version>`
- **macOS:** `~/Library/Application Support/typst/packages/local/chordish/<version>`
- **Windows:** `%APPDATA%\typst\packages\local\chordish\<version>`

If you've changed `TYPST_PACKAGE_PATH`, you should be able to figure it out.

Then import from `@local` instead of `@preview`:

```typ
#import "@local/chordish:<version>": songbook, song, section
```
