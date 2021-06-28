import time
import pandas as pd
import numpy as np
import matplotlib as plt

#define a dictionary with information
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_choice(message, choices = ['y','n']):
    
    
    while True:
        user_input = input(message).lower().strip()
        
        #convert all inputs into a list after removing all white spaces and converting to small letters
        user_input = user_input.replace(" ","")
        user_input = user_input.split(',')
        
        if user_input == 'end':
           raise SystemExit
                   
        elif 'all' in user_input:
             return ['all']
        
        else:
        #check if all inputs are part of the choices
            for choice in user_input:
                   
                if choice not in choices:
                    print('you have a wrong choice')
                    raise SystemExit
                    
            return user_input              

def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cities = ['chicago', 'new york city', 'washington']
    
    city = get_choice('please choose a city: \n', cities)

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    
    month = get_choice('please choose a month: \n', months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    
    day = get_choice('please choose a day or days: \n', days)

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
    all_cities = ['chicago', 'new york city', 'washington']
    
    if city == ['all']:
        
        num = 1
        
        for cit in all_cities:
        
            df_temp = pd.read_csv(CITY_DATA[cit])
            if num == 1:
                df = df_temp
            else:
                df = pd.concat([df,df_temp], ignore_index = True, sort = True)   
            num  = num + 1
        
    else:
        
        num = 1
        
        for cit in city:
            
            df_temp = pd.read_csv(CITY_DATA[cit])
            if num == 1:
                df = df_temp
            else:
                df = pd.concat([df,df_temp], ignore_index = True, sort = True)
            num = num + 1
            
     
    # filter the df we have right now by month
    # first convert the start time to df and then get the month and the day_pf week from there
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour']  = df['Start Time'].dt.hour
    #filter by selected dates
    
    if month != ['all']:
        
        # we need the months in numbers
         
        months_Series = ['january', 'february', 'march', 'april', 'may', 'june']
         
        month_s = []
    
        for mont in month:
            month_s.append(months_Series.index(mont) + 1)
        
        
        df = df[df['month'].isin(month_s)]
        
    if day != ['all']:
        
        #convert the days selected to a Proper case
        day = list(map(lambda x: x.title(),day))
        
        df = df[df['day'].isin(day)]
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    
    print('The most common month is: ' + str(common_month))
    
    # TO DO: display the most common day of week
    common_day = df['day'].mode()[0]
    
    print('The most common day is: ' + str(common_day))

    # TO DO: display the most common start hour
    
    common_hour = df['hour'].mode()[0]
    
    print('The most common hour is: ' + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    common_start = df['Start Station'].mode()[0]
    
    print('The most common start station is: ' + str(common_start))
    # TO DO: display most commonly used end station

    common_end = df['End Station'].mode()[0]
    
    print('The most common end station is: ' + str(common_end))

    # TO DO: display most frequent combination of start station and end station trip
    df['start end'] = df['Start Station'] + '-' + df['End Station']
    
    common_start_end = df['start end'].mode()[0]
    
    print('The most common start and end combination is: ' + str(common_start_end))
                                            

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['time diff'] = df['End Time'] - df['Start Time']
    
    totaldiff = df['time diff'].sum()
    print('Total time difference is: ' + str(totaldiff))
                          
    # TO DO: display mean travel time
    
    mean_time = df['time diff'].mean()
    print('mean travel time is: ' + str(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()
                          
    print(user_types)
    # TO DO: Display counts of gender
    try:
        
        genders = df['Gender'].value_counts()
        print(genders)
        # TO DO: Display earliest, most recent, and most common year of birth

        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common_age = df['Birth Year'].mode()[0]

        print('the oldest biker was born in:' + str(int(oldest)))
        print('the youngest biker was born in:' + str(int(youngest)))
        print('the most common bikers in age were born in :' + str(int(common_age)))
        
    except:
            print("sorry you can't have gender analysos")

                          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#function to display results
def display(df):
    
    choice = get_choice(' do you want to see the first 5 inputs of the data? ')
    
    if choice == ['y']:
        print(df.iloc[0:5,])
        
    
    pos = 5
    while input('do you want to see next set of 5 \n y or n?') == 'y':
        pos += 5
        print(df.iloc[pos-5:pos,])
        
    

def main():
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print("Note that Washington does not have complete data")
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
