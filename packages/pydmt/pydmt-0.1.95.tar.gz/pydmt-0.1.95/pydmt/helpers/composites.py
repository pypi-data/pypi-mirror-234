import pydmt.helpers.apt
import pydmt.helpers.git

deb_version = f"{pydmt.helpers.git.get_git_version()}~{pydmt.helpers.apt.codename}"
