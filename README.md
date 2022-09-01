# index-registry
Centralized index of Bazel dependencies.

Currently bzlmod only knows how to use http to fetch repositories. In order for a computer to do this securely, it needs valid github credentials in `~/.netrc`. Your `~/.netrc` file should look like:
```
machine github.com
login <username>
password <PAT>
machine api.github.com
login <username>
password <PAT>
```
With `<username>` replaced by your github username (e.g. `john-klingner`) and `<PAT>` replaced by your github Personal Access Token (PAT). Such a token can be generated according to [this guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). I think you only need repo read access for that token, but my development token has a bit more than that.

