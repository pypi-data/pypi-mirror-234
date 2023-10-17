""" Shorcuts for Bash
    Docs::

    login shell: A login shell logs you into the system as a specific user. Necessary for this is a username and password. When you hit ctrl+alt+F1 to login into a virtual terminal you get after successful login: a login shell (that is interactive). Sourced files:

    /etc/profile and ~/.profile for Bourne compatible shells (and /etc/profile.d/*)
    ~/.bash_profile for bash
    /etc/zprofile and ~/.zprofile for zsh
    /etc/csh.login and ~/.login for csh


    non-login shell: A shell that is executed without logging in. Necessary for this is a current logged in user. When you open a graphic terminal in gnome, it is a non-login (interactive) shell. Sourced files:

    /etc/bashrc and ~/.bashrc for bash
    interactive shell: A shell (login or non-login) where you can interactively type or interrupt commands, for example, a gnome terminal (non-login) or a virtual terminal (login). In an interactive shell the prompt variable must be set ($PS1). Sourced files:
    /etc/profile and ~/.profile

    /etc/bashrc or /etc/bash.bashrc for bash
    non-interactive shell: A (sub)shell that is probably run from an automated process. You will see neither input nor output when the calling process doesn't handle it. That shell is normally a non-login shell, because the calling user has logged in already. A shell running a script is always a non-interactive shell, but the script can emulate an interactive shell by prompting the user to input values. Sourced files:
    /etc/bashrc or /etc/bash.bashrc for bash (but, mostly you see this at the beginning of the script: [ -z "$PS1" ] && return. That means don't do anything if it's a non-interactive shell).

    depending on shell; some of them read the file in the $ENV variable.



        ps faux  : Show all processe with sub-trees --> good to deliete extra bash in docker.

        df -h   :  Disk space size


        ps aux  : Show all processes including commandline arguments

        ps -AFl : Show all processes with threads in tree mode

        ps -AlFH : Show processes in a hierarchy

        ps -e -o pid,args --forest  : Show list of processes owned by a specific user

        ps -p pid
            ps uax | grep process_name  : Show all threads for a particular process by id

        ps -p pid -L -o pid,tid,pcpu,state,comm

        Get top 5 processes by CPU usage

            ps -e -o pcpu,cpu,nice,state,cputime,args --sort pcpu | sed '/^ 0.0 /d'| tac |head -5
            ps auxf | sort -nr -k 3 | head -5


        Get top 5 processes by memory usage

            ps -e -orss=,args= | sort -b -k1,1n | pr -TW$COLUMNS| tac | head -5
            ps auxf | sort -nr -k 4 | head -5


        Get security info
            ps -eo euser,ruser,suser,fuser,f,comm,label



        ls                    : The most frequently used command in Linux to list directories
        pwd                   : Print working directory command in Linux
        cd                    : Linux command to navigate through directories
        mkdir                 : Command used to create directories in Linux
        mv                    : Move or rename files in Linux
        cp                    : Similar usage as mv but for copying files in Linux
        rm                    : Delete files or directories
        touch                 : Create blank/empty files
        ln                    : Create symbolic links (shortcuts) to other files
        cat                   : Display file contents on the terminal
        clear                 : Clear the terminal display
        echo                  : Print any text that follows the command
        less                  : Linux command to display paged outputs in the terminal
        man                   : Access manual pages for all Linux commands
        uname                 : Linux command to get basic information about the OS
        whoami                : Get the active username
        tar                   : Command to extract and compress files in Linux
        grep                  : Search for a string within an output
        head                  : Return the specified number of lines from the top
        tail                  : Return the specified number of lines from the bottom
        diff                  : Find the difference between two files
        cmp                   : Allows you to check if two files are identical
        comm                  : Combines the functionality of diff and cmp
        sort                  : Linux command to sort the content of a file while outputting
        export                : Export environment variables in Linux
        zip                   : Zip files in Linux
        unzip                 : Unzip files in Linux
        ssh                   : Secure Shell command in Linux
        service               : Linux command to start and stop services
        ps                    : Display active processes
        kill and killall      : Kill active processes by process ID or name
        df                    : Display disk filesystem information
        mount                 : Mount file systems in Linux
        chmod                 : Command to change file permissions
        chown                 : Command for granting ownership of files or folders
        ifconfig              : Display network interfaces and IP addresses
        traceroute            : Trace all the network hops to reach the destination
        wget                  : Direct download files from the internet
        ufw                   : Firewall command
        iptables              : Base firewall for all other firewall utilities to interface with
        apt, pacman, yum, rpm : Package managers depending on the distro
        sudo                  : Command to escalate privileges in Linux
        cal                   : View a command:line calendar
        alias                 : Create custom shortcuts for your regularly used commands
        dd                    : Majorly used for creating bootable USB sticks
        whereis               : Locate the binary, source, and manual pages for a command
        whatis                : Find what a command is used for
        top                   : View active processes live with their system usage
        useradd and usermod   : Add new user or change existing users data
        passwd                : Create or update passwords for existing users


        ----------------  Glob in Bash
        setopt extendedglob
        ls *(<tab>                                                    # to get help regarding globbing
        rm ../debianpackage(.)                                        # remove files only
        ls -d *(/)                                                    # list directories only
        ls /etc/*(@)                                                  # list symlinks only
        ls -l *.(png|jpg|gif)                                         # list pictures only
        ls *(*)                                                       # list executables only
        ls /etc/**/zsh                                                # which directories contain 'zsh'?
        ls **/*(-@)                                                   # list dangling symlinks ('**' recurses down directory trees)
        ls foo*~*bar*                                                 # match everything that starts with foo but doesn't contain bar
        ls *(e:'file $REPLY | grep -q JPEG':)                         # match all files of which file says that they are JPEGs
        ls -ldrt -- *(mm+15)                                          # List all files older than 15mins
        ls -ldrt -- *(.mm+15)                                         # List Just regular files
        ls -ld /my/path/**/*(D@-^@)                                   # List the unbroken sysmlinks under a directory.
        ls -Lldrt -- *(-mm+15)                                        # List the age of the pointed to file for symlinks
        ls -l **/README                                               # Search for `README' in all Subdirectories
        ls -l foo<23->                                                # List files beginning at `foo23' upwards (foo23, foo24, foo25, ..)
        ls -l 200406{04..10}*(N)                                      # List all files that begin with the date strings from June 4 through June 9 of 2004
        ls -l 200306<4-10>.*                                          # or if they are of the form 200406XX (require ``setopt extended_glob'')
        ls -l *.(c|h)                                                 # Show only all *.c and *.h - Files
        ls -l *(R)                                                    # Show only world-readable files
        ls -fld *(OL)                                                 # Sort the output from `ls -l' by file size
        ls -fl *(DOL[1,5])                                            # Print only 5 lines by "ls" command (like ``ls -laS | head -n 5'')
        ls -l *(G[users])                                             # Show only files are owned from group `users'
        ls *(L0f.go-w.)                                               # Show only empty files which nor `group' or `world writable'
        ls *.c~foo.c                                                  # Show only all *.c - files and ignore `foo.c'
        print -rl /home/me/**/*(D/e{'reply=($REPLY/*(N[-1]:t))'})     # Find all directories, list their contents and output the first item in the above list
        print -rl /**/*~^*/path(|/*)                                  # Find command to search for directory name instead of basename
        print -l ~/*(ND.^w)                                           # List files in the current directory are not writable by the owner
        print -rl -- *(Dmh+10^/)                                      # List all files which have not been updated since last 10 hours
        print -rl -- **/*(Dom[1,10])                                  # List the ten newest files in directories and subdirs (recursive)
        print -rl -- /path/to/dir/**/*(D.om[5,10])                    # Display the 5-10 last modified files
        print -rl -- **/*.c(D.OL[1,10]:h) | sort -u                   # Print the path of the directories holding the ten biggest C regular files in the current directory and subdirectories.
        setopt dotglob ; print directory/**/*(om[1])                  # Find most recent file in a directory
        for a in ./**/*\ *(Dod); do mv $a ${a:h}/${a:t:gs/ /_}; done  # Remove spaces from filenames





"""





def adocker():
    """ All Dockre command useful
    Docs::












    """






























