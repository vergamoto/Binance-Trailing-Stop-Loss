# ~/.bashrc: executed by bash(1) for non-login shells.

export LS_COLORS=$LS_COLORS:'di=0;35:'

PS1='${debian_chroot:+($debian_chroot)}\[\033[01;33m\]\u@\h\[\033[00m\]($CLUSTER_NAME):\[\033[01;34m\]\w\[\033[00m\] \n\$ '
unset color_prompt force_color_prompt

alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'