# Ecosystem Evidence Reference

Read only the rows for ecosystems present in the target. Exact versions normally come from lockfiles or build outputs already present in the repository; a manifest constraint alone is not an installed version.

| Ecosystem | Declarations | Preferred exact-version evidence | Runtime/toolchain evidence | Important caveats |
|---|---|---|---|---|
| Node.js | `package.json`, workspace manifests | `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock`, Bun lockfiles | `.nvmrc`, `.node-version`, `engines`, Volta config, container and CI files | Record prod/dev/optional scope. npm audit submits a dependency description to the configured registry; do not run it without explicit disclosure authorization. |
| Python | `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`, `Pipfile` | Hash-pinned requirements, `poetry.lock`, `uv.lock`, `Pipfile.lock`, installed metadata supplied by the user | `.python-version`, `requires-python`, runtime/container/CI declarations | Requirements files may contain indexes or credentials; never print them wholesale. A lock for one platform may not resolve identically on another. |
| PHP | `composer.json` | `composer.lock` and installed metadata already present | `config.platform.php`, runtime/container/CI declarations | Separate `require` from `require-dev`. Composer audit may contact configured repositories; private repository names and package coordinates must not be disclosed without authorization. |
| Java / Maven | `pom.xml`, parent POMs, BOMs | Checked-in resolved reports, SBOMs, or artifact metadata; otherwise versions may remain unresolved | Maven toolchains, compiler release, container/CI/runtime declarations | Maven has no universal lockfile. Property substitution, dependency management, profiles, parents, plugins, and nearest-wins mediation can change the resolved graph. Do not fetch plugins or dependencies just to audit. |
| Java / Gradle | `build.gradle`, `build.gradle.kts`, version catalogs | `gradle.lockfile`, dependency lock directories, checked-in resolved reports, SBOMs | Gradle wrapper, JVM toolchains, container/CI/runtime declarations | Locks apply only to configurations where dependency locking is enabled. Plugins and buildscript classpaths may have separate evidence. Do not execute arbitrary build logic merely to inspect dependencies. |
| Go | `go.mod` | `go.sum`, `vendor/modules.txt`, existing build/module metadata | `go` directive, `toolchain` directive, container/CI declarations | `go.sum` proves checksums, not that every entry ships. Reachability analysis is stronger than module presence. `govulncheck` may query the public Go vulnerability database, whose service logs request URL paths. |
| Rust | `Cargo.toml` | `Cargo.lock`, vendored metadata | `rust-toolchain.toml`, container/CI declarations | Library repositories may intentionally omit a lockfile; distinguish published-library policy from deployed binary reproducibility. |
| Ruby | `Gemfile`, gemspecs | `Gemfile.lock` | `.ruby-version`, runtime/container/CI declarations | Check platform-specific lock sections and production groups; do not expose private gem sources or credentials. |

## Advisory and lifecycle sources

Prefer, in order:

1. maintainer or vendor security advisories and release notes;
2. authoritative ecosystem advisory databases;
3. the CVE record and national vulnerability databases;
4. original researcher disclosures;
5. secondary reporting only as a lead.

For active exploitation, CISA's Known Exploited Vulnerabilities catalog or an explicit vendor statement is stronger evidence than exploit-code availability, scanning telemetry, social posts, CVSS, or EPSS. Record the source's publication and last-updated dates.

For runtime support, use official release-policy and lifecycle pages:

- [Node.js releases and end-of-life](https://nodejs.org/en/about/previous-releases)
- [Python supported versions](https://devguide.python.org/versions/)
- [PHP supported versions](https://www.php.net/supported-versions.php)
- [Go release policy and history](https://go.dev/doc/devel/release)

Java support depends on the exact distribution and support contract; use that distributor's official lifecycle and do not infer support from the Java feature version alone. Re-check these live sources for every freshness audit rather than copying today's version numbers into a report.
