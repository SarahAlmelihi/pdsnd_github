import calendar
import time
import pprint
import pandas as pd
import numpy as np


CITY_DATA = { 'ch': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'wa': 'washington.csv' }

months = [ 'january' , 'february' , 'march' , 'april' , 'may' , 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
            city = input("\nWould you like to see data for Chicago, New York City, or Washington?\nEnter 'ch' for Chicago, 'nyc' for New York, 'wa' for Washington.\n").lower()
            if city in ('ch', 'nyc', 'wa'):
                break
            else:
                print('invalid input, choose from the given city.\n')


    while(True):
        filter_choice = input("\nWould you like to filter the data by month, day, both, or not at all?\nEnter 'm' for month, 'd' for day, 'b' for both, 'n' for no filter.\n").lower()
        if filter_choice in ('m','d','b','n'):
            break
        else:
            print('invalid input, choose from the given letter.\n')

    # in case if the user choice was no filter
    month = 0
    day = 0

    # get user input for month (all, january, february, ... , june)
    if filter_choice in ('m','b'):
            while(True):
                    month = input('\nWhich month? January, February, March, April, May, or June.\n').lower()
                    if month in months:
                        break
                    else:
                        print('invalid input, choose from the given months.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_choice in ('d','b'):
            while(True):
                    day = input('\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.\n').lower()
                    if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
                        break
                    else:
                        print('invalid input, choose your day correctly.\n')

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    # filter by month to create the new dataframe
    if month != 0:
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of the week to create the new dataframe
    if day != 0:
        df = df[df['day'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, only if the user chose to not filter by month
    if month == 0:
        common_month = df["month"].mode()[0]
        month_name = calendar.month_abbr[common_month]
        print("The most common month is: ", month_name)

    # display the most common day of week, only if the user chose to not filter by day
    if day == 0:
        print("The most common day is: ", df["day"].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: ", df["hour"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common used start station: ", df["Start Station"].mode()[0])

    # display most commonly used end station
    print("\nThe most common used end station: ", df["End Station"].mode()[0])

    # display most frequent combination of start station and end station trip
    # create a new column 'combination of start and end stations'
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    print("\nThe most frequent combination of start station and end station trip is: ", df["trip"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:\n', df['Trip Duration'].sum())

    # display mean travel time
    print('\nAverage Travel Time:\n', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # Display counts of gender, earliest, most recent, and most common year of birth only if the city is Chicago, or New York
    if city in ('ch','nyc'):
        gender = df['Gender'].value_counts()
        print('\nGender:\n', gender)
        print('\nEarliest Birth Year:\n', df['Birth Year'].min())
        print('\nMost recent Birth Year:\n', df['Birth Year'].max())
        print('\nMost Common Birth Year:\n', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)


        while(True):
                raw_data = input("\nWould you like to view individual trip data? Enter 'y' for yes or 'n' for no.\n")
                if raw_data not in ('n','y'):
                    print("invalid input, Enter 'y' for yes or 'n' for no.\n")
                else:
                    break

        if raw_data == 'y':
            start = 0
            while(True):
                pprint.pprint(df[start:start+5].to_dict('records'))
                print('\n')
                print('-'*40)
                start += 5

                more_raw_data = input("\nWould you like to view more individual trip data? Enter 'y' for yes or 'n' for no.\n")
                while(more_raw_data not in ('y','n')):
                    print("invalid input, Enter 'y' for yes or 'n' for no.\n")
                    more_raw_data = input("\nWould you like to view more individual trip data? Enter 'y' for yes or 'n' for no.\n")
                    if more_raw_data in ('n','y'):
                        break

                if more_raw_data == 'n':
                    break

        restart = input("\nWould you like to restart? Enter 'y' for yes or 'n' for no.\n").lower()
        while(restart not in ('y','n')):
            print("invalid input, Enter 'y' for yes or 'n' for no.\n")
            restart = input("Would you like to restart? Enter 'y' for yes or 'n' for no.\n").lower()
            if restart in ('n','y'):
                break

        if restart == 'n':
            break

        print("\n")


if __name__ == "__main__":
	main()
