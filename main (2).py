import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function Code for Data Fetching and conversion
def dataframe(filename):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(filename)
    transposed_data = df.set_index(['Country Name', 'Indicator Name']).stack().unstack(0).reset_index()

    transposed_data.columns.name = None

    return df, transposed_data


file_path = 'Indicators.csv'
original_df, transposed_data = dataframe(file_path)

# Conversion of dataframe to Csv.
transposed_data.to_csv('Transposed.csv')
tran_df = pd.read_csv('Transposed.csv')
tran_df=tran_df.dropna()

# Desciptive Statistics
describe_data=original_df.describe()
print(describe_data)

#Correlation Matrix
selected_data = tran_df[tran_df['Indicator Name'] == 'Nitrous oxide emissions (% change from 1990)'][['Australia', 'Brazil','Nepal']]
correlation_matrix = selected_data.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Nitro Emission')
plt.show()

# Pie Chart
urban = original_df[original_df['Indicator Name'] == 'Urban population']
years_columns = original_df.columns[2:]
urban['Total'] = urban[years_columns].sum(axis=1)
top5_countries = urban.nlargest(5, 'Total')
plt.figure(figsize=(8, 8))
plt.pie(top5_countries['Total'], labels=top5_countries['Country Name'], autopct='%1.1f%%', startangle=90)
plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", title="Country Name", bbox_transform=plt.gcf().transFigure)
plt.title('top 5 Urban Populated Countries')
plt.show()

# Line Chart Code
filter_df =tran_df[(tran_df['Indicator Name'] == 'Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)') &
                   (tran_df['Year'].notna())]  # Ensure there's a valid year

# Select only the relevant columns
filter_df = filter_df[['Year', 'Ethiopia', 'Brazil']]
grouped_data =filter_df.groupby('Year').sum()

# Plot the line chart
plt.figure(figsize=(10, 6))
plt.plot(grouped_data.index, grouped_data['Brazil'], label='Brazil')
plt.plot(grouped_data.index, grouped_data['Ethiopia'], label='Ethopia')
plt.title('Poverty Headcount Ration - Brazil vs Ethopia')
plt.xlabel('Year')
plt.ylabel('Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)')
plt.legend()
plt.grid(True)
plt.show()


#BarChart
indicator_name = 'Foreign direct investment, net inflows (% of GDP)'
selected_data = original_df[original_df['Indicator Name'] == indicator_name]
sum_values = selected_data.groupby('Country Name').sum().iloc[:, 2:]

# Calculate the total sum for each country and select the top 10
top_countries = sum_values.sum(axis=1).sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
top_countries.plot(kind='bar', color='skyblue')
plt.title(f'Top 10 Countries for {indicator_name}')
plt.xlabel('Country')
plt.ylabel('Sum of Values')
plt.show()