import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

"""
Asks user to specify a city, month, and day to analyze.
Returns:
(str) city - name of the city to analyze
(str) month - name of the month to filter by, or "all" to apply no month filter
(str) day - name of the day of week to filter by, or "all" to apply no day filter
"""

    print('Hello! Let\'s explore some US bikeshare data!')

# Gets user input for city (chicago, new york city, washington)
    while True:
        city=input('Please choose which city you would like information about, Chicago, New York City or Washington: ')
        city=city.lower()
        if city not in ['chicago','new york city','washington']:
            print('You entered',city,'. Data is only available for Chicago, New York City and Washington.')
        else:
            print('Data for {} will be displayed now'.format(city.title()))
            break

# Gets user input for month (all, january, february, ... , june)
    while True:
        month=input('Which of the first 6 months of the year would you like information for? Or if you would like to see information for all available months, type ALL: ')
        month=month.lower()
        if month not in ['january','february','march','april','may','june','all']:
            print('You entered',month,'. Data is only available for the first six months of the year.')
        else:
            print('Data for {} will be displayed now'.format(month.title()))
            break

# Gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('Which of the days of the week would you like information for? Or if you would like to see information for all days, type ALL: ')
        day=day.lower()
        if day not in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
            print('You entered',day,'. That is not a day, please type in one of the 7 days of the week')
        else:
            print('Data for {} will be displayed now'.format(day.title()))
            break
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):

"""
Loads data for the specified city and filters by month and day if applicable.
Args:
(str) city - name of the city to analyze
(str) month - name of the month to filter by, or "all" to apply no month filter
(str) day - name of the day of week to filter by, or "all" to apply no day filter
Returns:
df - Pandas DataFrame containing city data filtered by month and day
"""

# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

# convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    df['hour'] = df['Start Time'].dt.hour

# filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

# filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df
    
def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month_name()
    common_month = df['month'].mode()[0]
    print('Most common month for travel: ', common_month)
    
    df['day'] = df['Start Time'].dt.day_name()
    common_day = df['day'].mode()[0]
    print('Most common day of the week for travel: ', common_day)

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour to start using a bike is: ', common_hour,":00")

    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)


def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station: ', common_start_station)
    
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: ', common_end_station)

    frequent_station_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most Frequent Combination of Start and End Stations: ', frequent_station_combo)

    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = ((df['Trip Duration'].sum())/86400).round(1) 
    print('Total Travel Time: ',total_travel_time,'days')

    mean_travel_time = ((df['Trip Duration'].mean())/60).round(1)
    print('Average Travel Time: ',mean_travel_time,'minutes')

    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)


def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    city = ['chicago', 'new york city', 'washington']
    
    user_counts = df['User Type'].value_counts()
    print("The different User Types are: ")
    print(user_counts)

    try:
        count_gender = df['Gender'].value_counts()
        print('\nThe number of male and female travellers is:\n', count_gender)
    except KeyError:
        print('\nThere is no gender data available for the selected city')
            
    try:
        earliest_birth_year = df['Birth Year'].min()
        print("\nThe oldest user was born in the year: ", int(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print("The youngest user was born in the year: ", int(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("People born in this year are the most common users: ", int(most_common_birth_year))
    except KeyError:
        print('\nThere is no year of birth data available for the selected city')
        
    print("\nThis took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)

def view_raw_data(df):
    viewer_choice = input('\nWould you like to view some of the raw data? Enter Yes or No: \n').lower()
    choices = ['yes']
    view_steps = 0
    while (viewer_choice in choices):
        print(df.iloc[view_steps:view_steps+5])
        view_steps += 5
        viewer_choice = input('Would you like to see more raw data? Enter Yes or No: \n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()