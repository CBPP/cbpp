#!/bin/sh
#    cb-places-pipemenu - a places openbox pipe menu
#    Copyright (C) 2010  John Crawley
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    Version 2012/09/27-cb

#    NB The shell, not bash, is invoked in the hope that
#    dash will be used, as it is much faster.

# Usage: add
# <menu id="places" label="Places" execute="/path/to/cb-places-pipemenu ~/" />
# to your .config/openbox/menu.xml

# or, if you want the "recent files" menu incorporated at the top, use:
# <menu id="places" label="Places" execute="/path/to/cb-places-pipemenu --recent ~/" />
# make sure you have cb-recent-files-pipemenu somewhere, and enter its path below.

# path to your "recent files" script, if you want to incorporate it:
recent_script=/usr/bin/cb-recent-files-pipemenu

# Command to open folders at "Browse here..." - any file manager
open_folder_cmd=thunar
# Default command to open files with - others might be xdg-open, gnome-open, pcmanfm...
default_open_cmd=exo-open  # exo-open comes with thunar
# Text editor of choice
text_editor=geany

# function to open files with default open command, or alternative command for certain files
# - add other conditions to choice
open_file() {
	[ -x "$1" ] && exec "$text_editor" "$1"     # comment out this line if you don't want to edit executables instead of executing
	#[ -x "$1" ] && exec "terminator -e" "$1"     # uncomment this and comment out previous line to run executables in terminal instead of editing
	[ "${1##*.}" = desktop ] && exec "$text_editor" "$1"     # comment out this line if you don't want to edit .desktop files instead of executing
	exec "$default_open_cmd" "$1"     # use default open command if above conditions not satisfied
}

# extra dotfiles to display in HOME folder (dotfiles are hidden by default)
# edit the list (space separated, surrounded by single quotes) or comment this line out, to taste:
shown_dotfiles='.config .local .Xdefaults .bash_aliases .bashrc .fonts.conf .gtkrc-2.0.mine .profile .xsession-errors'

# By default, this script will display directories separately, before files.
# To change this behaviour, see NOTE1, NOTE2 and NOTE3 below, near end of page.

#######################################################################

case $1 in
# if "--open" option is sent as $1, open file ($2) instead of generating menu
--open)
    open_file "$2"
    echo "$0 : failed to open $2" >&2
    exit;;    # in case exec command fails
# if "--recent" option is sent, incorporate "recent files" menu
--recent)
    shift
    output='<openbox_pipe_menu>
'
    if [ -x "$recent_script" ]
    then
        output="$output"'<separator label="Recently opened..." />
<menu execute="'"$recent_script"'" id="recent" label="files" />
'
    else
        echo "$0 : cannot find executable script $recent_script" >&2
    fi;;
*)
    output='<openbox_pipe_menu>
';;
esac

path="${1:-$HOME}"  # default starting place is ~, otherwise $1
path="$( echo "${path}"/ | tr -s '/' )"    # ensure one final slash
[ -d "$path" ] || { echo "$0 : $path is not a directory" >&2; exit 1; }

case "$path" in    # only escape if string needs it
*\&*|*\<*|*\>*|*\"*|*\'*) pathe=$(sed "s/\&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g;s/'/\&apos;/g;" <<XXX
$path
XXX
)
;;
*)pathe=$path;;
esac

case "$pathe" in
*\&apos\;*) pathe_apos=$(sed 's/\&apos;/\&apos;\&quot;\&apos;\&quot;\&apos;/g;'<<XXX
$pathe
XXX
)
;;
*) pathe_apos=$pathe;;
esac

output="$output"'<separator label="'$pathe'" />
<item label="Browse here...">
	<action name="Execute">
		<command>
		 &apos;'"$open_folder_cmd"'&apos; &apos;'"$pathe_apos"'&apos;
		</command>
	</action>
</item>
<separator />
'

unset extra_entries directories_menu files_menu
[ "$path" = "$HOME"/ ] && extra_entries="$shown_dotfiles"
for i in "$path"* $extra_entries
do
    [ -e "$i" ] || continue    # only output code if file exists
    shortname="${i##*/}"
	case $shortname in
	*\&*|*\<*|*\>*|*\"*|*\'*) shortnamee=$(sed "s/\&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g;s/'/\&apos;/g;" <<XXX
$shortname
XXX
)
    ;;
    *) shortnamee=$shortname;;
    esac
    case $shortnamee in
    *\&apos\;*) shortnamee_apos=$(sed 's/\&apos;/\&apos;\&quot;\&apos;\&quot;\&apos;/g;'<<XXX
$shortnamee
XXX
)
    ;;
    *) shortnamee_apos=$shortnamee;;
    esac
    case $shortnamee in
    *_*) shortnamee_label=$(sed 's/_/__/g;'<<XXX
$shortnamee
XXX
)
    ;;
    *) shortnamee_label=$shortnamee;;
    esac
	[ -d "$i" ] && {
# NOTE1 If you want directories and files listed together
# change next line (directories_menu="$directories_menu"') to read:	files_menu="$files_menu"' (note the one single quote at the end)
	directories_menu="$directories_menu"'
<menu id="'"${pathe_apos}${shortnamee_apos}"'" label="'"$shortnamee_label"'" execute="&apos;'"$0"'&apos; &apos;'"${pathe_apos}${shortnamee_apos}"'&apos;" />'; continue; }
	files_menu="$files_menu"'
<item label="'"$shortnamee_label"'">
    <action name="Execute">
        <command>
        &apos;'"$0"'&apos; --open &apos;'"${pathe_apos}${shortnamee_apos}"'&apos;
        </command>
    </action>
</item>'
done

[ -n "$directories_menu" ] && {
# NOTE2 comment out next 2 lines if you don't want "Directories" label
output="${output}"'<separator label="Directories" />
'
output="${output}${directories_menu}"'
'; }
[ -n "$files_menu" ] && {
# NOTE3 comment out next 2 lines if you don't want "Files" label
output="${output}"'<separator label="Files" />
'
output="${output}${files_menu}"'
'; }
output="${output}"'</openbox_pipe_menu>
'
printf '%s' "$output"
exit
