set distro (awk '/^ID=/' /etc/*-release | awk -F '=' '{print tolower($2)}')
switch $distro
  case '*alpine*'
    set ICON " "
  case '*arch*'
    set ICON " "
  case '*centos*'
    set ICON " "
  case '*debian*'
    set ICON " "
  case '*fedora*'
    set ICON " "
  case '*gentoo*'
    set ICON " "
  case '*manjaro*'
    set ICON " "
  case '*linuxmint*'
    set ICON " "
  case '*opensuse*'
    set ICON " "
  case '*raspbian*'
    set ICON " "
  case '*rhel*'
    set ICON " "
  case '*ubuntu*'
    set ICON " "
  case '*'
    set ICON " "
end

set -gx PATH $PATH $HOME/.krew/bin
set -gx PATH $PATH $HOME/.local/bin
set -gx STARSHIP_DISTRO $ICON

# starship init fish | source
oh-my-posh init fish --config /root/.config/oh-my-theme.json | source
