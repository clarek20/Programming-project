import api

def run_interactive():
    print("Welcome the the heatmap generation script for the OpenPrescribing.net data")
    ccg_code = input("Please start by entering your desired CCG code (e.g 14L for the Manchester CCG): ")
    bnf_code = input("Now enter the desired BNF code (e.g. 5.1 for Antibacterials): ")
    year = input("Now enter a desired year: ")
    year = int(year)
    print("Working...")
    heatmap_dataframe = api.get_heatmap_df(ccg_code, bnf_code, year)
    if len(heatmap_dataframe) == 0:
        raise Exception(f"Query with CCG code of {ccg_code}, BNF code of \
            {bnf_code} and year of {year} returned an empty result, perhaps\
                you made a typo?")
    heatmap_plot = api.plot_heatmap(heatmap_dataframe, year)
    print("Done!")
    print("Please enter a filename to save to, or enter nothing to use the default")
    filename = input("naming scheme of YEAR_CCGCODE_BNFCODE: ")
    if len(filename) == 0:
        filename = f"{year}_{ccg_code}_{bnf_code}.png"
    elif filename.endswith('.png'):
        filename = filename + '.png'
    
    print(f"Writing file with filename {filename}")
    heatmap_plot.figure.savefig(filename, pad_inches = 0.5, bbox_inches='tight')
    
if __name__ == "__main__":
    continue_running = True
    while continue_running == True:
        run_interactive()
        continue_choice_input = input("Would you like to generate another plot (y/n): ")
        continue_choice_input = continue_choice_input.lower()
        if continue_choice_input in ['y', 'yes']:
            pass
        else:
            continue_running = False
    print("Thanks for playing!")
