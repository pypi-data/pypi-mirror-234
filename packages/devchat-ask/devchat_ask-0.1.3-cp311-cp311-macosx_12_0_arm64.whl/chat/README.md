# DevChat

Ask everything about your dev data beyond the code.

## Dependencies

Please install the following dependencies and ensure their installation path are added to your `PATH` environment variable (or export environment variables: `CINDEX_CMD_PATH` and `CSEARCH_CMD_PATH`).

| Name | Description                                                                                                                                                                           | Installation |
| ---- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------ |
| cindex | Cindex prepares the trigram index for use by csearch. The index is the file named by $CSEARCHINDEX, or else $HOME/.csearchindex.<br />Usage:<br />&nbsp;&nbsp;`cindex [-list] [-reset] [path...]` | `go get github.com/google/codesearch/cmd/cindex@latest` |
| csearch | Csearch behaves like grep over all indexed files, searching for regexp, an RE2 (nearly PCRE) regular expression.<br />Usage:<br />&nbsp;&nbsp;`csearch [-c] [-f fileregexp] [-h] [-i] [-l] [-n] regexp` | `go get github.com/google/codesearch/cmd/csearch@latest` |