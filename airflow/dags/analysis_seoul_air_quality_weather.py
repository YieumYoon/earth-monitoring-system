import pandas as pd
from sqlalchemy import create_engine

def analyze_seoul_air_quality_weather():
    engine = create_engine('postgresql+psycopg2://postgres:postgres@postgres:5432/earth_monitoring')
    aq = pd.read_sql('SELECT * FROM processed.daily_seoul_air_quality', engine)
    w = pd.read_sql('SELECT * FROM processed.daily_seoul_weather', engine)
    df = pd.merge(aq, w, on='date', how='inner')

    results = {}

    # 1. Rainfall Reduces Air Pollution
    df['rainy'] = df['precip'] > 0
    rain_stats = df.groupby('rainy')[['avg_pm25', 'avg_pm10']].mean().rename(index={True: 'Rainy', False: 'Non-Rainy'})
    rain_corr = df['precip'].corr(df['avg_pm25']), df['precip'].corr(df['avg_pm10'])
    results['rainfall'] = {'group_stats': rain_stats, 'corr_pm25': rain_corr[0], 'corr_pm10': rain_corr[1]}

    # 2. Temperature Inversion Increases Pollution
    temp_corr = df['tempmin'].corr(df['avg_pm25']), df['tempmin'].corr(df['avg_pm10'])
    coldest_threshold = df['tempmin'].quantile(0.1)  # 10th percentile as 'coldest'
    df['coldest'] = df['tempmin'] < coldest_threshold
    coldest_stats = df.groupby('coldest')[['avg_pm25', 'avg_pm10']].mean().rename(index={True: 'Coldest 10%', False: 'Other'})
    results['temp_inversion'] = {'corr_pm25': temp_corr[0], 'corr_pm10': temp_corr[1], 'coldest_stats': coldest_stats}

    # 3. Humidity Affects Ozone Levels
    hum_corr = df['humidity'].corr(df['avg_o3'])
    results['humidity_ozone'] = {'corr_humidity_o3': hum_corr}

    # 4. Wind Speed Reduces Pollution
    wind_corr = df['windspeed'].corr(df['avg_pm25']), df['windspeed'].corr(df['avg_pm10'])
    results['wind'] = {'corr_pm25': wind_corr[0], 'corr_pm10': wind_corr[1]}

    # 5. Seasonal Trends in Air Quality
    df['month'] = pd.to_datetime(df['date']).dt.month
    month_stats = df.groupby('month')[['avg_pm25', 'avg_pm10']].mean()
    df['season'] = pd.to_datetime(df['date']).dt.month.map(lambda m: 'Winter' if m in [12,1,2] else 'Spring' if m in [3,4,5] else 'Summer' if m in [6,7,8] else 'Fall')
    season_stats = df.groupby('season')[['avg_pm25', 'avg_pm10']].mean().reindex(['Winter','Spring','Summer','Fall'])
    results['seasonal'] = {'month_stats': month_stats, 'season_stats': season_stats}

    # Print results (or you can log/save them)
    for key, value in results.items():
        print(f'\n==== {key.upper()} ====' )
        if isinstance(value, dict):
            for k, v in value.items():
                print(f'{k}:\n{v}\n')
        else:
            print(value)

    return results

if __name__ == '__main__':
    analyze_seoul_air_quality_weather()
