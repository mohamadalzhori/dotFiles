#!/bin/bash

# Define your web browsers
BROWSER="brave-browser"

# change working directory to script's directory
cd "$(dirname "$0")"

# Generate a custom list of choices (Google, YouTube, and Torn)
options="Apps\nGo\nYou\nTorn\nChat\nGitHub\nWassap\nKeep\nMusic\nLogout\nShutdown\nReboot"

# Show the list in Rofi and let the user select an option
selected_option=$(echo -e "$options" | rofi -dmenu -mesg ">>> Tab = Autocomplete" -i -p "run: ")

# Check the selected option and perform the corresponding action
case "$selected_option" in
    Go)
        # Use surfraw to search on Google
        search_term=$(rofi -dmenu -mesg ">>> Tab = Autocomplete" -i -p "run: ")
        surfraw -browser="$BROWSER" google $search_term
        ;;
    You)
        # Use surfraw to search on YouTube
        search_term=$(rofi -dmenu -mesg ">>> Tab = Autocomplete" -i -p "search: ")
        surfraw -browser="$BROWSER" youtube $search_term
        ;;
    Torn)
        # Open the website www.torn.com
        xdg-open "https://www.torn.com"
        ;;
    Chat)
        # Open the website www.torn.com
        xdg-open "https://chat.openai.com/"
        ;;	
    Apps)
        # run apps
        rofi -combi-modi window,drun -show combi
        ;;
    GitHub)
        # Open the website www.torn.com
        xdg-open "https://github.com/mohamadalzhori?tab=repositories"
        ;;	
    Logout)
	# Logout using Qtile's exit command
        qtile cmd-obj -o cmd -f shutdown
	;;
    Shutdown)
        # Shutdown the system
        systemctl poweroff
        ;;
    Reboot)
        # Reboot the system
        systemctl reboot
        ;;
    Music)
        rhythmbox
        ;;	
    Wassap)
        # Open whatsapp.com
	xdg-open "https://web.whatsapp.com"
        ;;
    Keep)
    	xdg-open "https://keep.google.com"	    
	;;
    *)
        # If no valid option selected, exit
        exit
        ;;
esac

