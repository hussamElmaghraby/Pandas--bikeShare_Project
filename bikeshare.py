import time
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'wash': 'washington.csv' }

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
    city = ''
    while city not in CITY_DATA.keys():
        print("Available Cities : ")
        print("CH 1 \nNY  2 \nWASH 3")
        city = input("Please Select Your City :").lower()
        # city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nInvalid input. Please try again ")
            print("\nRestarting...")
    print(f"\nYou have chosen **[ {city.title()} ]**  as your city.")


    # get user input for month (all, january, february, ... , june)
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''

    while month not in MONTH_DATA.keys():
         print("Please enter the month, between January to June or type 'all' for all months ")
         print(" 1-January \n2-February \n3-March \n4-April \n5-May \n6-June \n7-All")

         month =  input("\nEnter Your Month :").lower()

         if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please try again ")
            print("\nRestarting...")

    print(f"\nYou have chosen **[ {month.title()} ]**  as your month.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    DAY_LIST = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' , 'all' ]
    day = ''
    while day not in DAY_LIST:
        print("\nPlease enter a day in the week of your choice ")
        print("From monday to sunday Or All")
        day = input("Enter Your Day :").lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please try again")
            print("\nRestarting...")
    print(f"\nYou have chosen **[ {day.title()} ]** as your month.")
    print('-'*100)
    return city, month , day


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

    # extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    
    if month != 'all':
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month 
        df = df[df['month'] == month]

    # filter by day of week 
    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df
# ---------------------------------------------------------------------------
def display_data(df):
    available_responses = ['yes' , 'no']
    view_data = ''
    start_loc = 0
    while view_data not in available_responses:
        view_data = input("Would you like to view 5 rows of individual trip data ? Yes or No !").lower()

        if view_data == 'yes':
            
            print(df.iloc[start_loc:start_loc + 5])
            while view_data == 'yes':
                view_data = input("Would you like to add more 5 rows ? :").lower()
                start_loc += 5
                print(df.iloc[start_loc:start_loc + 5])

        elif view_data not in available_responses:
                print("Please Enter a valid input [Yes Or No]")
    print('-'*100)

# ---------------------------------------------------------------------------
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most Common Month : {}".format(most_common_month ))

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("Most Common Day : {}".format(most_common_day ))
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("Most Common Hour : {}".format(most_common_hour ))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

# ----------------------------------------------------------------------------
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The Most Common Start Station : {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The Most Common End Station : {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'] , sep=' - To - ')
    most_combination = df['Start To End'].mode()[0]
    print("The Most Comination : {}".format(most_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
# -----------------------------------------------------------------------------
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time : {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Of Travel Time : {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)

# -------------------------------------------------------------------------------
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print("User Counts : \n{}".format(counts_of_user_types))

    # Display counts of gender
    if 'Gender'  not in df.columns:
        print("\nThere is not Information about 'Gender' in this database !!")
    else :
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts : \n{}".format(gender_counts))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("\nThere is not Information about 'Birth Year' in this database !!")
    else:
        # earliest
        earliest_birthyear = df['Birth Year'].min()
        print("Earliest Birth Year : {}".format(earliest_birthyear))
        # most recent
        most_recent_birthyear = df['Birth Year'].max()
        print("Most Recent Birth Year : {}".format(most_recent_birthyear))
        # most common
        most_common_birthyear = df['Birth Year'].mode()[0]
        print("Most Common Birth Year : {}".format(most_common_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n : ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()