import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def transform_csv_data(filename):
    """ 
        Transform the CSV data and return 2 list of transformed and cleaned data
    """
    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(filename)

    # Data transposing
    df_countries = df.transpose()

    # Remove header
    df_countries.columns = df_countries.iloc[0]
    df_countries = df_countries.iloc[1:]

    # replace column headers with the first row:
    df_countries.columns = df_countries.iloc[0]
    df_countries = df_countries.iloc[1:]
    return df, df_countries

def series_dataframe(df, series_type):
    """ 
        Return data that matches specific series name
    """
    return df.loc[df['Series Name'] == series_type]

def plot_line_chart(dfa):
    """
        Plot and display line chart for the dataframe data of CO2
    """
    dfa = dfa[['Country Name', '2010 [YR2010]', '2011 [YR2011]', '2012 [YR2012]',
            '2013 [YR2013]', '2014 [YR2014]', '2015 [YR2015]', '2016 [YR2016]',
            '2017 [YR2017]', '2018 [YR2018]', '2019 [YR2019]', '2020 [YR2020]']]

    # Melt the dataframe to create a timeseries
    df_melt = dfa.melt(id_vars='Country Name', var_name='Year', value_name='Emissions')

    # Convert year column to actual years
    df_melt['Year'] = df_melt['Year'].str.slice(0,4)

    # Plot the timeseries
    fig, ax = plt.subplots(figsize=(10, 8))
    for country, data in df_melt.groupby('Country Name'):
        data.plot(x='Year', y='Emissions', ax=ax, label=country)

    ax.set_ylabel("CO2 Emissions (kg per GDP)")
    ax.set_title("European Countries CO2 Emissions Per GDP from 2010 to 2020")
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))

    plt.tight_layout()
    return plt.show()


def plot_group_bar_chart(df):
    """
        Plot and display grouped bar chart for the dataframe data
    """

    df = pd.read_csv('climate_data.csv', index_col=[0,1,2,3]) 

    # Filter years  
    years = ['2010 [YR2010]', '2015 [YR2015]', '2020 [YR2020]']
    df = df[years]

    # Pivot data
    plot_data = df.pivot_table(index='Country Name', columns='Series Name', aggfunc='sum')

    # Plot
    ax = plot_data.plot(kind='bar', rot=0)
    ax.set_xlabel('Country')
    ax.set_ylabel('Emissions')
    ax.set_title('Greenhouse Gas Emissions by Country')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.xticks(rotation='vertical')
    return plt.show()


def plot_stacked_bars(df):
    """
        Plot and display stacked bar chart for the dataframe data
    """
    years = ['2010 [YR2010]','2011 [YR2011]','2012 [YR2012]','2013 [YR2013]','2014 [YR2014]',
             '2015 [YR2015]','2016 [YR2016]','2017 [YR2017]','2018 [YR2018]','2019 [YR2019]',
             '2020 [YR2020]'
            ]
    uk_intensity = df.loc[df['Country Name']=='United Kingdom'][years]

    uk_green_gas_emission = uk_intensity.loc[df['Series Name']=='Total greenhouse gas emissions (kt of CO2 equivalent)']
    uk_green_gas_emission = uk_green_gas_emission.values.tolist()[0]

    uk_co2_emission = uk_intensity.loc[df['Series Name']=='CO2 emissions (kt)']
    uk_co2_emission = uk_co2_emission.values.tolist()[0]

    print(uk_green_gas_emission)
    print(uk_co2_emission)

    # Sample data
    data = {'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
            'co2_emission': uk_co2_emission,
            'green_emission': uk_green_gas_emission,
          }

    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.bar(df['Year'], df['co2_emission'], color='blue')
    ax.bar(df['Year'], df['green_emission'], bottom=df['co2_emission'], color='green')

    ax.set_ylabel("Change compared to previous year")
    ax.set_title("UK: Yearly Change in CO2 and Green house gases emissions")
    ax.legend(['CO2 Emission', 'Greenhouse Gas Emission'])

    return plt.show()


if __name__ == "__main__":

    # Function which takes a filename as argument, 
    # reads a dataframe in World- bank format and returns two dataframes
    df_first, df_second = transform_csv_data('./climate_data.csv')
    
    # Get information needed for specific series
    co2_df_data = series_dataframe(df_first, 'CO2 emissions (kg per 2015 US$ of GDP)')

    # Plot Line chart
    plot_line_chart(co2_df_data)

    # Plot Bar chart
    plot_group_bar_chart(df_first)

    # Plot Stacked chart
    plot_stacked_bars(df_first)

    # Describe the data
    co2_df_data.describe()
    df_first.describe()
