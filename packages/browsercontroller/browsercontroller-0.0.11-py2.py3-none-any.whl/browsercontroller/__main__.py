"""Entry point for the project."""


from browsercontroller.selenium.check_if_firefox_is_installed import (
    run_bashardcodedommand,
)
from browsercontroller.selenium.get_controller import (
    get_ubuntu_apt_firefox_controller,
)

# Check if apt version of firefox is installed, if not, ensure it is.
ensure_apt_firefox_command: str = (
    'bash -c "source src/browsercontroller/selenium/firefox_version.sh '
    + 'swap_snap_firefox_with_ppa_apt_firefox_installation"'
)
run_bashardcodedommand(bashCommand=ensure_apt_firefox_command)

get_ubuntu_apt_firefox_controller(
    url="https://www.github.com", default_profile=False
)
