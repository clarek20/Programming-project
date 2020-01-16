import api

def run_interactive():
    # Print a welcome statement 
    print("Welcome the the heatmap generation script for the OpenPrescribing.net data")
    # Take input for a desired CCG code and assign it to a variable
    ccg_code = input("Please start by entering your desired CCG code (e.g 14L for the Manchester CCG): ")
    # Take input for a BNF code and assign it to a variable
    bnf_code = input("Now enter the desired BNF code (e.g. 5.1 for Antibacterials): ")
    # Take a year as input and assign it to a variable
    year = input("Now enter a desired year: ")
    # Make the string input into a year 
    year = int(year)
    print("Working...")
    # Call get_heatmap_df from api.py with a ccg_code, a bnf_code and a year
    heatmap_dataframe = api.get_heatmap_df(ccg_code, bnf_code, year)

    # If result is empty raise an error
    if len(heatmap_dataframe) == 0:
        raise Exception(f"Query with CCG code of {ccg_code}, BNF code of \
            {bnf_code} and year of {year} returned an empty result, perhaps\
                you made a typo?")

    # Plot the heatman dataframe using plot_heatmap 
    heatmap_plot = api.plot_heatmap(heatmap_dataframe, year)
    print("Done!")
    print("Please enter a filename to save to, or enter nothing to use the default")

    # Take desired filename as an input
    filename = input("naming scheme of YEAR_CCGCODE_BNFCODE: ")
    
    # If user inputs an empty filename, use the default file naming scheme.
    # If they enter their own filename, use that instead.
    if len(filename) == 0:
        filename = f"{year}_{ccg_code}_{bnf_code}.png"
    elif filename.endswith('.png'):
        filename = filename + '.png'
    
    # Print a message saying file is saving with the desired filename
    print(f"Writing file with filename: {filename}")

    # Save the heatmap to the disk
    heatmap_plot.figure.savefig(filename, pad_inches = 0.5, bbox_inches='tight')
    
if __name__ == "__main__":
    # Variable that is True to keep program running
    continue_running = True

    # While loop that keeps the program runnign while continue_running is True
    while continue_running == True:
        # Run the function above
        run_interactive()
        # Ask the user if they would like to run the script again
        continue_choice_input = input("Would you like to generate another plot (y/n): ")
        # Convert the input to lower case for simplicity
        continue_choice_input = continue_choice_input.lower()

        # See if user inputted y or yes and rerun loop if true
        if continue_choice_input in ['y', 'yes']:
            pass
        # set continue_running to false to stop loop if user did not enter y or yes
        else:
            continue_running = False
    print("Thanks for playing!")
