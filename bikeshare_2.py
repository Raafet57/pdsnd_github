import time
import pandas as pd
import numpy as np

# Constants for file paths and valid input options
# Mapping of city names to their respective CSV files
CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        city (str): name of the city to analyze
        month (str): name of the month to filter by, or "all" to apply no month filter
        day (str): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # User input for city
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please choose from Chicago, New York City, or Washington.")

    # User input for month filter
    while True:
        month = input("Would you like to filter the data by month, day, or not at all? Type 'all' for no time filter. ").lower()
        if month in VALID_MONTHS:
            break
        print("Invalid input. Please choose from January, February, March, April, May, June, or 'all'.")

    # User input for day filter
    while True:
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type 'all' for no day filter. ").lower()
        if day in VALID_DAYS:
            break
        print("Invalid input. Please choose from Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = VALID_MONTHS.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    most_common_day = df['day_of_week'].mode()[0]
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]

    print("Most Common Month:", VALID_MONTHS[most_common_month - 1].title())
    print("Most Common Day of Week:", most_common_day)
    print("Most Common Start Hour:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



# Statistical functions (time_stats, station_stats, trip_duration_stats, user_stats) 
def enhanced_station_stats(df):
    """
    Enhanced function to calculate statistics on stations using numpy.
    
    Args:
        df (DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating Enhanced Station Stats...\n')
    start_time = time.time()

    # Using numpy for efficient computation
    most_common_start_station = np.mode(df['Start Station'])[0]
    most_common_end_station = np.mode(df['End Station'])[0]
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print(f"Most Common Start Station: {most_common_start_station}")
    print(f"Most Common End Station: {most_common_end_station}")
    print(f"Most Common Trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def calculate_trip_lengths(df):
    """
    Calculate statistics on trip lengths.
    
    Args:
        df (DataFrame): The DataFrame containing bikeshare data.
    """
    print('\nCalculating Trip Length Stats...\n')
    start_time = time.time()

    # Using numpy to calculate statistics
    average_trip_length = np.mean(df['Trip Duration'])
    trip_length_variance = np.var(df['Trip Duration'])

    print(f"Average Trip Length: {average_trip_length} seconds")
    print(f"Trip Length Variance: {trip_length_variance} seconds^2")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    most_common_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1).idxmax()

    print(f"Most Common Start Station: {most_common_start_station}")
    print(f"Most Common End Station: {most_common_end_station}")
    print(f"Most Common Trip: {most_common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print(f"Total Travel Time: {total_travel_time} seconds")
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print("User Types:\n", user_types)

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender Counts:\n", gender_counts)

    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\nBirth Year Stats:")
        print(f"Earliest Year: {earliest}, Most Recent Year: {most_recent}, Most Common Year: {most_common}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time upon user request.
    """
    show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()
    start_loc = 0
    while show_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        show_data = input("Do you wish to continue? Enter yes or no: ").lower()
        
def display_raw_data(df):
    """
    Displays 5 rows of raw data at a time upon user request.
    """
    show_data = input("Would you like to see 5 rows of raw data? Enter yes or no: ").lower()
    start_loc = 0
    while show_data == 'yes':
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        show_data = input("Do you wish to continue? Enter yes or no: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()