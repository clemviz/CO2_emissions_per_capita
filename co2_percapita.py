import pandas as pd
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_font
from highlight_text import ax_text, fig_text
from drawarrow import ax_arrow

#Load custom Fonts
google_font = "https://github.com/google/fonts/blob/main"
regular = load_font(f"{google_font}/ofl/martel/Martel-Regular.ttf?raw=true")
bold = load_font(f"{google_font}/ofl/martel/Martel-Bold.ttf?raw=true")
#Load Classic 10 colors
cmap = load_cmap("Classic_10")


""" _______________ Pandas Section _______________ """

#Read csv file from Our World in Data
df = pd.read_csv(rf"https://ourworldindata.org/grapher/co-emissions-per-capita.csv?v=1&csvType=full&useColumnShortNames=true")
#Filter to keep records after 1900
df = df[df['Year'] >= 1900]

#Define the entities (regions/countries) to plot
entities = [
    'Saudi Arabia',
    'United States',
    'Canada',
    'Russia',
    'China',
    'Europe',
    'United Kingdom',
    'Brazil',
    'Africa'
]

#Various Transformations
df_subset = df.loc[:,['Entity','Year','emissions_total_per_capita']] #keep columns
df_subset['Entity'] = df_subset['Entity'].replace({'European Union (27)':'Europe'}) #replace by Europe for better clarity
df_subset = df_subset[df_subset['Entity'].isin(entities)] #keep entities we want to plot
#Pivot the entities to simplify the plotting
df_subset = df_subset.pivot_table(values='emissions_total_per_capita',columns='Entity',index='Year')


""" _______________ Matplotlib Section _______________ """

#Create the fig and axes and adjust the subplots
fig, axs = plt.subplots(nrows = 3, ncols = 3, figsize = (12, 8), dpi = 200)
fig.subplots_adjust(hspace = 0.07, wspace= 0.07, bottom= 0.085)

color_background = "#FFFFFFFF" # define the color of the background

fig.set_facecolor(color_background)

colors = cmap.colors # extract the colors from the cmap

for ax, entity, color in zip(axs.flat, entities, colors):
    for sub_entity in entities:
        ax.plot(df_subset.index, df_subset[sub_entity], color='grey',alpha=0.15, linewidth = 0.7, zorder=5) # plot grey lines
        ax.plot(df_subset.index, df_subset[entity], color = color, linewidth = 1.3, zorder=5) # plot colored country lines
        ax.set_facecolor(color_background)

        ax.set_ylim(-2, 25)
        ax.set_axis_off()

        first_date = df_subset[entity].first_valid_index() # get the first date based on the first valid index
        first_value = df_subset[entity].loc[first_date] # get the first value
        last_date = df_subset[entity].last_valid_index() # get the last date
        last_value = df_subset[entity].loc[last_date] # get the last value
        # Plot the first and last data points
        ax.scatter(
            [first_date, last_date],
            [first_value, last_value],
            color = color,
            s=23
        ) 
        # Value of last data point
        ax.text(x=last_date + 2.5, y = last_value, s=f"{last_value:.1f}", color = color, size = 8, ha='left', font=regular)
        # Value of first data point. If very close to 0, don't write
        if first_value > 0.05:
            ax.text(x=first_date - 2.5, y = first_value, s=f"{first_value:.1f}", color = color, size = 8, ha='right', font=regular)
        # Write in a different location for first row
        if entity in ['Saudi Arabia','United States','Canada']:
            ax.text(x = 1980, y = 11, s=entity.upper(), color=color, fontsize = 9, font = bold)
        else:
            ax.text(x = 1960, y = 4, s=entity.upper(), color=color, fontsize = 9, font=bold)
        # Write the first and last dates at the bottom of the graphs
        ax.text(x = first_date , y= -1.5, s= first_date, color = 'darkgrey', size = 7, ha='center', va='center', font=regular)
        ax.text(x = last_date , y= -1.5, s= last_date, color = 'darkgrey', size = 7, ha='center', va='center', font=regular)


# UK comment
# Draw Arrow
ax_arrow(
    tail_position=[1905,20],
    head_position=[1900,11.3],
    color='black',
    fill_head=False,
    ax=axs[2][0],
    radius=0.3,
    head_width=4,
    head_length=5
)
# Write Text
uk_text =f"The <UK> had the <highest>\nper capita CO2 emissions in the world."
ax_text(
    x=1907,
    y=20,
    s=uk_text,
    fontsize=5,
    color='black',
    font=regular,
    ax=axs[2][0],
    va='center',
    ha='left',
    highlight_textprops=[
        {'color': colors[6],'font':bold, 'fontsize':5.5},
        {'font':bold}
    ]

)


# China Comment
# Draw Arrow
ax_arrow(
    tail_position=[1955,20],
    head_position=[2000,3.5],
    color='black',
    fill_head=False,
    ax=axs[1][1],
    radius=-0.35,
    head_width=4,
    head_length=5
)
china_text =f"<China>'s per capita emissions\nhave almost <tripled> since 2000."

# Write Text
ax_text(
    x=1905,
    y=20,
    s=china_text,
    fontsize=5,
    color='black',
    font=regular,
    ax=axs[1][1],
    va='center',
    ha='left',
    highlight_textprops=[
        {'color': colors[4],'font':bold, 'fontsize':5.5},
        {'font':bold}
    ]

)

# North American Countries Comment
#Canada Arrow
ax_arrow(
    tail_position=[2000,23],
    head_position=[2015,17],
    color='black',
    fill_head=False,
    ax=axs[0][2],
    radius=-0.4,
    head_width=4,
    head_length=5
)
#USA Arrow
ax_arrow(
    tail_position=[2023,23],
    head_position=[2015,19],
    color='black',
    fill_head=False,
    ax=axs[0][1],
    radius=0.2,
    head_width=4,
    head_length=5
)

# Write Text
na_text =f"North America, represented by the <US> and <Canada>, has high per capita emissions\nbut both countries have steadily reduced them over time."
ax_text(
    x=1945,
    y=24,
    s=na_text,
    fontsize=5,
    color='black',
    font=regular,
    ax=axs[0][2],
    va='center',
    ha='center',
    highlight_textprops=[
        {'color': colors[1],'font':bold, 'fontsize':5.5},
        {'color': colors[2],'font':bold, 'fontsize':5.5}
    ]

)


#Title
title_text = """
How <CO2 Emissions per Person> have changed across Countries <(1900-2023)>
<Per capita Carbon Dioxide emissions (in tonnes) from fossil fuels and industry.>
<Regions and countries are sorted by their most recent value.>
"""
fig_text(
    x= 0.15,
    y=0.98,
    s=title_text,
    fontsize=15,
    color='black',
    ha='left',
    va='center',
    font = regular,
    highlight_textprops=[
        {'font':bold},
        {'font':bold},
        {'fontsize':11,'color':'darkgrey'},
        {'fontsize':11,'color':'darkgrey'}
        ]
    
)

# Data Source mention
data_source_text = "<Data:> Global Carbon Budget (2024); Population based on various sources (2024) - with major processing by Our World in Data"
fig_text(
    x = 0.9,
    y = 0.01,
    s = data_source_text,
    fontsize = 5,
    font = regular,
    ha='right',
    va = 'center',
    highlight_textprops=[
        {'font':bold}
    ]
)

# Author
design_text = f"<Design:> Clément Villalard\n<GitHub:> ClemViz"
fig_text(
    x = 0.12,
    y = 0.01,
    s = design_text,
    fontsize = 5,
    font = regular,
    ha = 'left',
    va = 'center',
    highlight_textprops=[
        {'font':bold},
        {'font':bold}
    ]
)

#fig.savefig(rf'C:\Users\cleme\Documents\matplotlib-journey\FinalProject\co2_emissions_per_capita.png', bbox_inches = 'tight', dpi=300)

#plt.show()