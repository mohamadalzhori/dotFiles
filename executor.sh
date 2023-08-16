#!/bin/bash

# Define your web browsers
BROWSER="brave-browser"

# Generate a custom list of choices (Google, YouTube, and Torn)
options="Apps\nGo\nYou\nTorn\nChat"

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
    *)
        # If no valid option selected, exit
        exit
        ;;
esac
