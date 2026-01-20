# -*- coding: utf-8 -*-
"""
Katarzyna Goch
13.02.2024
"""

# Install dependencies
import pandas as pd
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
# from matplotlib.lines import Line2D
import matplotlib.colors as mcolors
from scipy.stats import kruskal
from scipy.stats import mannwhitneyu
from scipy.stats import spearmanr
import itertools
import shutil
# import matplotlib.colors as colors
# import matplotlib.cm as cmx
import numpy as np
import os
# from upsetplot import from_contents, UpSet
# from upsetplot import plot as upset_plot
import matplotlib as mpl
from scipy.stats import linregress
mpl.rcParams['figure.dpi'] = 300
plt.rcParams.update({'font.size': 8})
plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams['font.family'] = "sans-serif"
plt.style.use('ggplot')
# plt.style.use('seaborn-v0_8-whitegrid')

v = 11
# Assign directories
root = 'C:\\Users\\KatarzynaGoch\\OneDrive - Instytut Geografii i PZ PAN\\Dokumenty\Doktorat\Paper_1_Literature_review'
in_file = os.path.join(root,"GLURB_Modelling systemic changes in urban systems_v%s.xlsx"%v)
# Copy master table to ta temp directory
temp_dir=os.path.join(root, 'temp')
master_file = os.path.join(temp_dir, 'master.xlsx')

if not os.path.exists(temp_dir): os.mkdir(temp_dir)
# if not os.path.isfile(master_file): shutil.copyfile(in_file, master_file)
shutil.copyfile(in_file, master_file)


# Read master table as a dataframe and kill last row
pdf = pd.read_excel(master_file, sheet_name='Final_database_v%s'%v, header=[0,1])

# Shorten the thematic group names

d = {'Planning and policies for sustainable development': 'Planning and policies',
     'Resilience (based on the concept of resilience)':'Resilience',
     "System's approach (based on the system’s theory nomenclature) ":"System's approach"}
pdf = pdf.rename(columns=d)
# Sort by year
pdf = pdf.sort_values(by=('Year', 'x'))
time_span = range(int(min(pdf[('Year', 'x')])), int(max(pdf[('Year', 'x')]))+1)

# Select data from master Excel to extract 
idxs_main_all = [('Year','x'),
             ("Systems approach", 'max'),
             ('Resilience', 'max'),
             ('Land use change', 'max'),
             ('Planning and policies', 'max'),
             ('Infrastructure', 'max'),
             ('Climate change', 'max'),
             ('Global scale models', 'max')]

# idxs_main = idxs_main_all[:-1]

idxs_sub = [
    ("Systems approach", 'urban system as a whole – a holistic approach '),
    ("Systems approach", 'complexity theory, Complex Adaptive Systems approach'),
    ("Systems approach", 'social-ecological systems (SES), social-ecological-technological systems (SETS) '),
    ('Resilience', 'urban resilience (the concept)'),
    ('Resilience', 'assessment of urban system resilience (explicit concept) '),
    ('Resilience', 'adaptation and response scenarios (implicit concept)'),
    ('Planning and policies', 'urbanization processes and policies '),
    ('Planning and policies', 'policy and planning support systems (PSS)'),
    ('Planning and policies', 'sustainable transformation (e.g. shift to non-zero building stock, to shared economy) '),
    ('Planning and policies', 'resources management (energy, woodland, soils) '),
    ('Planning and policies', 'management of urban system and sub-systems (e.g. urban water system, urban growth management) '),
    ('Planning and policies', 'sustainability of the urban system’s development'),
    ('Land use change', '(de)urbanization (growth or decline of urban areas)'),
    ('Land use change', 'urban sprawl (uncontrolled development of urban areas))'),
    ('Land use change', 'land-use conversion(e.g. from forest to farmland)'),
    ('Land use change', '    environmental impact assessment of the land-use change '),
    ('Land use change', 'land-use change processes (e.g. deforestation, migration)'),
    ('Infrastructure', 'drainage; sewage; groundwater; storm water'),
    ('Infrastructure', 'transportation'),
    ('Infrastructure', 'housing'),
    ('Infrastructure', 'energy'),
    ('Infrastructure', 'other'),
    ('Climate change', 'climate risks assessement (what could happen?) '),
    ('Climate change', 'climate impact assessment (what would be the outcome?)'),
    ('Climate change', 'climate change adaptation and (urban) design optimisation '),
    ('Climate change', 'climate models'),
    ('Global scale models', 'model input'),
    ('Global scale models','model output')]


# Create selected dataframes
df_all = pdf[idxs_main_all]#pdf[[pdf.columns[i] for i in idxs_main_all] ]
df_all.columns = [x[0] for x in df_all.columns]
# df_main = pdf[idxs_main]
# df_main.columns = [x[0] for x in df_main.columns]
df_sub = pdf[idxs_sub]

## Number of studies
trend_file = 'C:\\DATA\\2024_Thelwall_Sud_article_trends\\trend.xlsx'
trend_df = pd.read_excel(trend_file)
trend_apx = pd.DataFrame(index=[2021], columns=['Scopus'])
# trend_apx['Scopus'][2021] = trend_df[trend_df['Year']==2020].Scopus * 1.125

# Count the total number of studies
total_count = df_all.groupby(['Year']).size()
total_count = total_count.reindex(time_span, fill_value=np.nan)

# Count the number of paper per-group
all_count = df_all[df_all>0].count().drop('Year')
all_count.to_clipboard()
# Count the number of paper per sub-group
sub_count = df_sub[df_sub>0].count()
sub_count.to_clipboard()

## Temporal trends by main group of studies
main_trend = df_all[df_all>0].groupby('Year').count()
main_trend = main_trend.reindex(time_span, fill_value=np.nan)
md = {'Planning and policies':'Planning and policies for sustainable development'}
main_trend = main_trend.rename(columns=md)

# Create the trend of the global studies 2020-2024
# Assign annual growth rate of 5.6% based on  https://doi.org/10.1162/qss_a_00327
gr = 0.056
start_idx = 37 # year 2016
def no_publications(idx):
    t = idx - start_idx
    return trend_df.loc[start_idx,'Scopus']*(1+gr)**t

for i in range(start_idx,42):
    trend_df.loc[i,'Extrapolated'] = no_publications(i)

# Get the trend of the global studies 1996 - 2023 from Scimago database
    
# Path to the directory containing the Excel files
directory = 'C:\\DATA\\2025_No_of_publications_Scimago_1996-2023'


# Initialize an empty list to hold the results
results = []

# Loop through all the files in the directory
for filename in os.listdir(directory):
    # Check if the file is an Excel file (you can adjust the condition if needed)
    if filename.endswith('.xls') or filename.endswith('.xlsx'):
        file_path = os.path.join(directory, filename)
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            # Check if the 'Citable documents' column exists
            if 'Citable documents' in df.columns:
                # Sum the values in the 'Citable documents' column
                total_citable_documents = df['Citable documents'].sum()
                
                # Extract the year from the filename (assuming year is part of the filename)
                # Modify this part depending on your filename format
                year = filename.split('rank ')[-1].split('.')[0]  # Example: extracting year from filename like "scimago_1999.xls"
                
                # Add the result to the list
                results.append({'Year': year, 'Total Citable Documents': total_citable_documents})
            else:
                print(f"'Citable documents' column not found in {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

# Convert the results list into a pandas DataFrame
scimago_df = pd.DataFrame(results)

# Set the 'Year' column as the index
scimago_df.set_index(
    pd.RangeIndex(start=1996, stop=2024), inplace=True)

# Reindex the dataframe, to include years from the whole period
scimago_df = scimago_df.reindex(time_span, fill_value=np.nan)
scimago_df.reset_index(inplace=True)

###############################################################################
### FIGURE 1 - Number of studies  in total and by thematic group, by year
### Figure with 8 subplots (4x2)
### First subplot shows the number of studies in total
### First subplot shows the number of studies in total

fig, axs = plt.subplots(4,2, figsize=(9,6), sharex=True, sharey=True, dpi=300)

# First subplot: Plot the number of studies as bars as primary ax
ax1 = total_count.plot.bar(ylabel = 'no_studies', fontsize=8, ax=axs[0,0])
# Add trend data as secondary ax
trend_source = "Scimago"
if trend_source == 'Scopus':
    ax2 = trend_df['Scopus'].plot(kind='line', ax=axs[0,0], secondary_y=True, color='k',
                            ylim = [0,5e6],#ylim=[0,trend_df['Scopus'].max()*1.4], 
                            fontsize=8)
    
    # Plot the extrapolated trend
    plt.plot(range(start_idx,42), trend_df.loc[37:41,'Extrapolated'],'k', 
             ls='--', dashes=(2, 1))
    plt.text(len(total_count)/4,trend_df['Scopus'].max()*0.45,'Global trend',#weight="bold",
             ha='center', fontsize=8)
    
elif trend_source =="Scimago":
    ax2 = scimago_df['Total Citable Documents'].plot(kind='line', ax=axs[0,0], secondary_y=True, color='k',
                            ylim = [0,5e6],#ylim=[0,trend_df['Scopus'].max()*1.4], 
                            fontsize=8)

    plt.text(13,scimago_df['Total Citable Documents'].max()*0.45,'Global trend',#weight="bold",
             ha='left', fontsize=8)
    
# Set the title of the frst subplot
axs[0,0].set_title('ALL', fontsize=8, weight="bold")

# # set the primary (left) y label
ax1.set_ylabel("")

# adjust the ticks for the secondary y axes
ax2.tick_params(axis='y', labelsize=8)
ax2.yaxis.get_offset_text().set_fontsize(8)

# set the secondary (right) y label from ax1
ax1.right_ax.set_yticks([0, 1e6, 2e6, 3e6, 4e6, 5e6])

ax1.set_ylim([0,5])
ax1.set_yticks(np.arange(0,6))

# Print the nunmber of studies (n=56)
axs[0,0].text(0.01, .95, 'n=%s'%(int(total_count.sum())),# weight="bold",
         fontsize=8, ha='left', va='top', transform=axs[0,0].transAxes)

# Following axes: Number of studies by group
axs_flat = axs.reshape(-1)[1:]
for ig, a in enumerate(axs_flat):   
    main_trend[main_trend.columns[ig]].plot(kind='bar', ax=a)
    a.set_title(main_trend.columns[ig], fontsize=8, weight="bold")
    a.set_yticks([0,1,2,3,4,5], [0,1,2,3,4,5], fontsize=8)
    a.set_xlim(-3, len(main_trend)+1) # From 1980
    a.set_xticks(
        range(-3, len(main_trend)+1, 5), 
        range(1980, 2030, 5), 
        fontsize=8, rotation=0)
    a.set_xlabel("")
    a.set_ylabel("")#"Number of studies", fontsize=8)
    a.text(0.01, .95, 'n=%s'%int(np.nansum((main_trend[main_trend.columns[ig]]))),# weight="bold",
             fontsize=8, ha='left', va='top', transform=a.transAxes)

# Add x axis label in the middle   
fig.text(0.5, -0.01, 'Year', ha='center', fontsize=8, color='k')
# Add y axis label in the middle   
fig.text(-0.0, 0.5, 'Number of studies', ha='center', va='center',rotation=270,
         fontsize=8, color='k')  
 
plt.tight_layout()
out_file = os.path.join(root,'figures','highres', 'number_of_studies_by_year_all_and_thematic_group.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.show()

###############################################################################
### FIGURE 2
### Aggregated ranking by thematic group and year of publication (sum or mean)
###
rank_sum = df_all.groupby('Year').sum()

# Get the index 
r_index = rank_sum.index.astype('int64')
rank_sum.index = r_index
# Create a range of numbers between min and max date
r_range = range(r_index[0],r_index[-1])
# Create a list of missing years
na_index = [r for r in r_range if r not in r_index]
# Append rows with missing data
for na_i in na_index: rank_sum.loc[na_i] = pd.Series()
rank_sum.sort_values(by='Year', inplace=True)
# Revert the order of columns
rank_sum_r=rank_sum[rank_sum.columns[::-1]]
# sns.heatmap(rank_sum.T, annot=True, cmap='coolwarm', ax=axs)

# Create a set of circles with radius equal sum of ranks
N = len(rank_sum_r.columns)
M = len(rank_sum_r.index)
ylabels = rank_sum_r.columns
xlabels = rank_sum_r.index

x, y = np.meshgrid(np.arange(M), np.arange(N))
s = rank_sum_r.T.to_numpy()#np.random.randint(0, 180, size=(N,M))
R = s/np.nanmax(s)/1.5

# Create the figure
fig, axs = plt.subplots(1,2,figsize=(10,2), dpi=300, 
                        gridspec_kw={"width_ratios" : (20,1)})

circles = [plt.Circle((j,i), radius=r) for r, j, i in zip(R.flat, x.flat, y.flat)]
col = PatchCollection(circles, color='r', alpha=0.7)

axs[0].add_collection(col)
fontdict={'fontsize': 8, 'rotation':90}
axs[0].set(xticks=np.arange(M), yticks=np.arange(N), 
       xlim=[-1, M], ylim=[-1, N])

axs[0].set_xticklabels(xlabels, **fontdict)
axs[0].set_yticklabels(ylabels, fontsize= 8)

# Store the minimum and the maximum summed rank
N=N-1
rmin = np.nanmin([i for i in s.flat if i!=0])
rmax =  np.nanmax(s)
# s1 = np.zeros((N,1))
s1 = np.reshape([rmin+i * (rmax-rmin)/(N-1) for i in range(N)], (N,1))
# Override the selected values to make the legend look better
s1 = np.array([[1],[2],[3],[5],[7],[10]])

# Change 1 - -1 list indices to look better
for i,n in enumerate(s1):
    # if n%0.5 !=0: s1[i] = [round(n[0] * 2) / 2-.5 ]
    if n%0.5 !=0: s1[i] = [math.floor(n[0])]
# Find tick / circle locations
ar = np.array(s1.flat)
new_ticks = (ar - ar.min()) / np.ptp(ar) * (N-1)

# Create array of size equal to number of thematic groups
x1, y1 = np.meshgrid(np.arange(1), np.array([y for y in new_ticks.flat]))

# Standardize radius
R1 = s1/np.nanmax(s1)/1.5
# Create circles showing min and max summed rank
circles1 = [plt.Circle((j,i), radius=r) for r, j, i in zip(R1.flat, x1.flat, y1.flat)]
col1 = PatchCollection(circles1, color='r', alpha=0.7)

axs[1].add_collection(col1)
# Assign second ax labels and title
axs[1].set(xticks=[],yticks=new_ticks,xlim=[-1, 1], ylim=[-1, N])
axs[1].set_yticklabels([x for x in s1.flat], fontsize= 8)
axs[1].set_ylabel('Sum of scores',fontsize= 8)

plt.tight_layout()
out_file = os.path.join(root,'figures','highres', 'sum_of_scores_by_year_by_thematic_group.png')
# plt.savefig(out_file, dpi=600)
plt.show()

### Print some statistics
# Change the values of NaN to zero, indicating the absence of a thematic group
scores_stats = rank_sum.copy()
spearman_df = pd.DataFrame(index = scores_stats.columns, columns=['Spearmanns correlation', 'Spearmanns correlation after 2010'])
scores_stats['Year'] = scores_stats.index
# Calculate the 5-year moving average using the rolling function
for tg in scores_stats.columns:
    # Change NaN values to zeros, to observe averaged trend in the presence of topics in time
    tg_MA = scores_stats[tg].replace({np.nan:0}).rolling(window=5, min_periods=1).mean()
    moving_avg_col = f'{tg}_5_year_MA'
    scores_stats[moving_avg_col] = tg_MA
    
    # Compute and display the correlation between 'Year' and the moving averages
    # correlation = scores_stats['Year'].corr(scores_stats[moving_avg_col])
    correlation, p_val = spearmanr(
        scores_stats['Year'],
        scores_stats[moving_avg_col],
        nan_policy='omit')
    
    if p_val<0.05: 
        print(f'Correlation between Year and {moving_avg_col}: {correlation}')
        spearman_df.loc[tg, 'Spearmanns correlation']=np.round(correlation,2)
    
    scores_contemp = scores_stats[scores_stats.Year>=2010]
    # corr_contemp = scores_contemp['Year'].corr(scores_contemp[moving_avg_col])
    corr_contemp, p_val_contemp = spearmanr(
        scores_contemp['Year'],
        scores_contemp[moving_avg_col],
        nan_policy='omit')
    if p_val_contemp<0.05:
        print(f'Correlation after 2010 between Year and {moving_avg_col}: {corr_contemp}\n')
        spearman_df.loc[tg, 'Spearmanns correlation after 2010']=np.round(corr_contemp,2)
spearman_df.to_clipboard()    
# Check the System's Approach only for the shape of the trend
scores_sa = scores_stats[['Year',"Systems approach_5_year_MA"]]
# Simplify colunm names
scores_sa.columns = ['Year',"SystemsApproach_5_year_MA"]
# Change NaN values to zeros 
# scores_sa = scores_sa.fillna(0) 

# Extract the data
X = scores_sa['Year'].values
y = scores_sa['SystemsApproach_5_year_MA'].values

# Linear Regression using scipy.stats.linregress
slope, intercept, r_value, _, _ = linregress(X, y)
y_linear_pred = slope * X + intercept
r2_linear = r_value**2  # R² value for linear regression

# Quadratic Regression (fitting a polynomial of degree 2)
quadratic_model = np.poly1d(np.polyfit(X, y, 2))
y_quadratic_pred = quadratic_model(X)

# Calculate R² for quadratic regression
y_mean = np.mean(y)
ss_tot = np.sum((y - y_mean) ** 2)
ss_res = np.sum((y - y_quadratic_pred) ** 2)
r2_quadratic = 1 - (ss_res / ss_tot)

### FIGURE 3 - Systems approach regression

# Plotting the data and regression lines
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(X, y, color='blue', label='Data', zorder=5)

# Plot the quadratic regression
ax.plot(X, y_quadratic_pred, color='green', label=f'Quadratic regression fit (R²={r2_quadratic:.2f})', linewidth=2)

# Adding titles and labels
ax.set_xlabel('Year')
ax.set_ylabel('Systems approach 5-year moving average')
ax.set_xticks(range(1980,2030,5))
ax.set_xticklabels(range(1980,2030,5))#, rotation=90)

# Adding a legend
ax.legend()

# Add grid
ax.grid(True)

# Add regression equations as text
quad_coeffs = quadratic_model.coefficients
quadratic_eq = f"y = {quad_coeffs[0]:.2f}x² + {quad_coeffs[1]:.2f}x + {quad_coeffs[2]:.2f}"

# Position the texts
ax.text(0.61, 0.13, quadratic_eq, transform=ax.transAxes, fontsize=10, color='green', ha='left')

# Save the figure
out_file = os.path.join(root,'figures','highres', 'systems_approach_quadratic_fit.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.show()



## Run the Mann Whitney U test for significant diference between the pair of groups

# Test can be done on the scores or sum of scores
input_df = {
    'scores': df_all[df_all.columns[1:]], # drop 'Year' columns
    'sum of scores': rank_sum}

# Select the input
input_type = 'scores'
df = input_df[input_type]
# Select only years after 2010 (index=19)
# df = df[df_all.Year>2010]
# Initialize an empty list to store the p-values
p_values = []

# Loop through all possible pairs of columns using itertools.combinations
columns = df.columns
for group1, group2 in itertools.combinations(columns, 2):
    # Extract the data for the two groups
    data1 = df[group1]
    data2 = df[group2]
    
    # Remove NaN values by dropping rows where either of the groups have NaN
    data1_clean = data1.dropna()
    data2_clean = data2.dropna()

    # If after cleaning, both groups still have data, perform the Kruskal-Wallis test
    if len(data1_clean) > 0 and len(data2_clean) > 0:
        stat, p_value = mannwhitneyu(data1_clean, data2_clean)
        
        # Check if the p-value is greater than the threshold (no significant difference)
        if p_value > 0.05:
            # Print the results if no significant difference
            print(f"No significant difference between columns: {group1} vs {group2}")
            print(f"Mann Whitney U Test Statistic: {stat:.4f}")
            print(f"P-value: {p_value:.4f}\n")
        
        # Append the p-value to the list
        p_values.append((group1, group2, p_value))
    else:
        print(f"Warning: Not enough data for comparison between {group1} and {group2} due to NaN values.\n")
        # If not enough data for comparison, we append NaN for that pair
        p_values.append((group1, group2, np.nan))

# Convert the list of results to a dataframe for easy plotting
p_values_df = pd.DataFrame(p_values, columns=['Group1', 'Group2', 'P-value'])

# Create a matrix of p-values for plotting
p_matrix = pd.DataFrame(np.nan, index=columns, columns=columns)

# Fill in the p-values for the matrix
for row in p_values_df.itertuples():
    p_matrix.loc[row.Group1, row.Group2] = row._3
    p_matrix.loc[row.Group2, row.Group1] = row._3  # Fill both upper and lower triangles

# Define a custom function for formatting labels
def custom_format(x):
    if x < 0.001:
        return "<0.001"
    else:
        return f"{x:.3f}"
   
# Plot the heatmap of p-values
plt.figure(figsize=(10, 8))
ax = sns.heatmap(
    p_matrix.astype(float),
    annot=False,
    fmt='',
    cmap='coolwarm',
    vmin=0,
    vmax=0.1,
    cbar_kws={'label': 'Mann-Whitney U Test P-value'},
    annot_kws={"size": 8},  # optional: control font size
)

# Manually add custom text annotations
for i in range(p_matrix.shape[0]):
    for j in range(p_matrix.shape[1]):
        if i != j:  # Skip the diagonal
            value = p_matrix.iloc[i, j]
            text = custom_format(value)
            ax.text(j + 0.5, i + 0.5, text, 
                    ha='center', va='center', 
                    color='white')

# Manualy change the colorbar labels. First get the colorbar object
cbar = ax.collections[0].colorbar
# Define ticks
ticks = np.arange(0, 0.11, 0.01)  # 0, 0.01, ..., 0.1
cbar.set_ticks(ticks)
# Replace the last tick label
ticklabels = [f"{t:g}" for t in ticks]
ticklabels[-1] = '>0.1'
ticklabels[0] = '<0.001'
# cbar.set_ticks(ticks)
cbar.set_ticklabels(ticklabels)
            
# plt.title('Heatmap of Mann-Whitney U Test P-values between %s assigned to studies'%input_type)
plt.xlabel('Thematic group')
plt.ylabel('Thematic group')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=45)
out_file = os.path.join(root,'figures','highres', 'mann-whitney-u-test_by_thematic_group.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.show()


## Run the Kruskal test for significant diference inside the clusters of groups
cluster1=["Systems approach", 'Planning and policies','Land use change', 'Infrastructure']
cluster2=['Resilience', 'Climate change', 'Global scale models']

# Create a dataframe to store results
kruskal_df = pd.DataFrame()
for i, cluster in enumerate([cluster1, cluster2]):
    print(cluster)
    data = df_all[cluster].dropna()
    if i==0: 
        stat, p_value = kruskal(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2], data.iloc[:,3])
    else: stat, p_value = kruskal(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2])
        
    # Check if the p-value is greater than the threshold (no significant difference)
    if p_value > 0.05:
        # Print the results if no significant difference
        print("No significant difference")
    else:
        print("Significant difference")
        
    print(f"Kruskal Test Statistic: {stat:.4f}")
    print(f"P-value: {p_value:.4f}\n")
    
    kruskal_df.loc[i, 'Thematic groups'] = str(cluster)
    kruskal_df.loc[i, 'Kruskal Test Statistic'] = stat
    kruskal_df.loc[i, 'Kruskal Test P-value'] = p_value
    
kruskal_df.to_clipboard()






# ###############################################################################
# ## Interdisciplanirity of studies - the UPSET plot
# all_gt0 = df_all.drop('Year',axis=1).select_dtypes(np.number).gt(0)
# main_inter = all_gt0.sum(axis=1)
# main_inter.index = df_all['Year']

# # Create upset plot of main groups of studies (all combinations)
# input_dict = {}
# # For each group assign the articles, Index of each article will be the id
# for acol in all_gt0.columns: input_dict[acol] = all_gt0.index[all_gt0[acol]].to_list()
# upset_data = from_contents(input_dict)
# # Add the year of publication
# upset_data['Year'] = df_all['Year'].loc[upset_data.id].values
# # Plot
# # fig, ax = plt.subplots(dpi=300)
# upset = UpSet(upset_data, subset_size="count", facecolor="#E24A33", shading_color="lightgray",
#               show_counts=True, intersection_plot_elements=4, 
#               element_size=25, totals_plot_elements=6)
# upset.add_catplot(value="Year", kind="swarm", elements=5, color="#E24A33")#,saturation=0.75)#, width = 0.5, elements=5)
# plot_result = upset.plot()
# plot_result["intersections"].set_ylabel("Number of studies", fontsize=10)
# plot_result["totals"].set_xlabel("Number of studies", fontsize=10)
# # plt.tight_layout()
# out_file = os.path.join(root,'figures','Upset.png')
# plt.savefig(out_file, dpi=fig.dpi)
# plt.show()


###############################################################################
# Hetmap showing cominations of studies

# Get all the group combinationts
all_gt0 = df_all.drop('Year',axis=1).select_dtypes(np.number).gt(0)
group_pairs = [(a, b) for idx, a in enumerate(all_gt0.columns) for b in all_gt0.columns[idx + 1:]]
# Create ouput df
pair_df = pd.DataFrame(index=all_gt0.columns, columns=all_gt0.columns, dtype=np.int16)
# For each pair of groups, count number of studies that included both of them
for pair in group_pairs:
    pair_count = all_gt0.groupby([pair[0],pair[1]]).size().reset_index().rename(columns={0:'count'})
    pair_df.loc[pair[0],pair[1]] = pair_count['count'].iloc[-1]
    pair_df.loc[pair[0],pair[0]] = all_gt0.groupby([pair[0]]).size()[True]
    pair_df.loc[pair[1],pair[1]] = all_gt0.groupby([pair[1]]).size()[True]

# PLot the heatmap
fig, ax = plt.subplots(figsize=(4,3),dpi=300)

# Create a mask for the diagonal
d_mask = np.eye(pair_df.shape[0], dtype=bool)

# Plot the number of studies per pair, without the count per one group
g = sns.heatmap(pair_df, mask = d_mask, 
                norm = mcolors.Normalize(vmin=0, vmax=pair_df.max().max()*1.05),
                annot=False, cmap='Reds',ax=ax)  

# Create a cmap with only one color
single_cmap = mcolors.ListedColormap(['lightgray'])
# Create a diagonal color by plotting another heatmap over it (to layer the color)
sns.heatmap(pair_df, mask=~d_mask, cmap=single_cmap, cbar=False, annot=False, center=0)

# Plot the heatmap
g.figure.axes[-1].yaxis.label.set_size(8)
g.set_xticklabels(g.get_xmajorticklabels(), fontsize = 8)
g.set_yticklabels(g.get_ymajorticklabels(), fontsize = 8)

yticklabels = [ 
    str(x).split('(')[1].split(')')[0].split(',') for x in ax.get_yticklabels() ]
xticklabels = [ 
    str(x).split('(')[1].split(')')[0].split(',') for x in ax.get_xticklabels() ]
ticks = ax.get_yticks()
# Loop over data dimensions and create text annotations.
for i, tick in enumerate(ticks):
    for j, tick in enumerate(ticks):
        label = pair_df.loc[all_gt0.columns[i],all_gt0.columns[j]]
        if np.isnan(label): label=''
        else: label = int(label)
        text = ax.text(j+0.5, i+0.5, 
                       label,
                       ha="center", va="center", color="k", fontsize=8)
# Get the colorbar object
colorbar = g.collections[0].colorbar

# Set the font size for the colorbar ticks and label
colorbar.set_label('Number of studies', fontsize=8)  # Change label font size
colorbar.set_ticks([ i for i in range(0, int(pair_df.max().max()),5)])  # Set the positions of the ticks
colorbar.set_ticklabels([ i for i in range(0, int(pair_df.max().max()),5)])  # Set the labels for the ticks
colorbar.ax.tick_params(labelsize=8)  # Change tick labels font size

# Save
out_file = os.path.join(root,'figures','highres', 'number_of_pairs_by_thematic_group.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.show()   


# Old plots
# # Count the total number of studies
# fig,ax = plt.subplots(figsize=(6.5,2.5), dpi=300)


# # plt.text(39,2820000,'x') # 
# # plt.text(40,2895666.75*1.125*1.125,'x')
# plt.tight_layout()
# # Save
# out_file = os.path.join(root,'figures','Total_no_studies.png')
# plt.savefig(out_file, dpi=fig.dpi)
# plt.show()







###############################################################################
### FIGURE 2 - number of  studies by group
# Count the number of studies by main group (with Global scale models)

# fig,ax = plt.subplots(figsize=(4,4), dpi=300)

# ax = all_count.plot.bar()
# ax.set_ylabel('Number of studies', fontsize=8)
# ax.set_xticks(ticks=range(len(all_count.index)), labels=all_count.index, 
#               rotation=90, fontsize=8)
# ax.set_yticks(np.linspace(0,round(all_count.max(),-1),6), labels=[int(i) for i in np.linspace(0,round(all_count.max(),-1),6)], 
#               fontsize=8)
# plt.text(0,48,'n=%s'%(int(total_count.sum())), weight="bold", fontsize=8,
#          ha='center')

# plt.tight_layout()
# out_file = os.path.join(root,'figures','Thematic_no_studies.png')
# plt.savefig(out_file, dpi=fig.dpi)
# plt.show()


### FIGURE 4 5 6 7

## Ranking of studies
# Get the mean ranking studies by main group
# fig,axs = plt.subplots(1,2, figsize=(6.5,2.5), dpi=300, sharey=True)
# main_rank = df_all.mean().drop('Year')
# main_rank.plot.bar(title='Mean rank of studies', ax=axs[0])
# main_rank_gt0 = df_all[df_all>0].mean().drop('Year')
# main_rank_gt0.plot.bar(title='Mean rank of studies (gt0)', ax=axs[1])
# plt.show()


# ## Temporal trends of ranks by main group of studies
# main_rank_trend_gt0 = df_all[df_all>0].groupby('Year').mean()
# main_rank_trend_gt0 = main_rank_trend_gt0.reindex(time_span, fill_value=np.nan)
# main_rank_trend_gt0.plot.bar(subplots=True, layout=(2,4), title = 'Mean rank of studies (gt0)', 
#                          legend=False, figsize=(16,5), sharey=True, color='r')
# plt.show()

# ## Temporal trends of ranks by main group of studies
# main_rank_trend = df_all.groupby('Year').mean()
# main_rank_trend = main_rank_trend.reindex(time_span, fill_value=np.nan)
# main_rank_trend.plot.bar(subplots=True, layout=(2,4), title = 'Mean rank of studies', 
#                          legend=False, figsize=(16,5), sharey=True, color='r')
# plt.show()

