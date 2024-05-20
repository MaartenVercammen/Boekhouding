import pandas as pd

def main():

    file_in_directory = 'exports'
    file_out_directory = 'out/'

    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(file_in_directory) if isfile(join(file_in_directory, f))]

    print(f"Files in directory: {onlyfiles}")
    df = pd.DataFrame()

    df = pd.concat((pd.read_csv(f'{file_in_directory}/{f}', sep=';', encoding='latin-1') for f in onlyfiles), ignore_index=True)

    # Get coloms Afschriftnummer, Datum, Rubrieknaam,Bedrag, Omschrijving
    print("Formatting files...")
    df = df[['Afschriftnummer', 'Datum', 'Omschrijving', 'Bedrag','Vrije mededeling']]
    df = df.rename(columns={'Afschriftnummer': 'afschriftnummer', 'Datum': 'datum', 'Omschrijving': 'omschrijving', 'Bedrag': 'bedrag', 'Vrije mededeling': 'vrije_mededeling'})

    # Add empty one column at place 3 and 14 from 6 to 20 

    df.insert(loc=3, column='empty', value=['' for i in range(df.shape[0])])

    for i in range(5, 19):
        df.insert(loc=i, column=f'empty{i}', value=['' for i in range(df.shape[0])])

    print("Sorting entries by date...")
    #Sort by date
    df['datum'] = pd.to_datetime(df['datum'], format='%d/%m/%Y')
    df = df.sort_values(by='datum')

    # format bedrag to float
    print("Updating amounts...")
    df['bedrag'] = df['bedrag'].str.replace(',', '.').astype(float)

    # Only get first word from omschrijving
    print("Updating descriptions...")
    df['omschrijving'] = df['omschrijving'].str.split(' ').str[0]


    print("Splitting inkomsten and uitgaven...")
    # Only get the inkomsten and safe to other dataframe
    df_in = df[df['bedrag'] > 0]

    # Only get the uitgaven and safe to other dataframe
    df_uit = df[(df['bedrag'] < 0)]
    df_new_uit = df_uit.copy()
    df_new_uit['bedrag'] = df_uit['bedrag'] * -1

    # Save to csv
    print("Saving files...")
    df_in.to_csv(f'{file_out_directory}/inkomsten.csv', sep=',', index=False, encoding='latin-1')
    df_new_uit.to_csv(f'{file_out_directory}/uitgaven.csv', sep=',', index=False, encoding='latin-1')

    print("Done!")

if __name__ == '__main__':
    main()