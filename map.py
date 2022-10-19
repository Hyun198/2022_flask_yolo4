import csv
import folium
import pandas as pd


#path = 'C:/Users/user-pc/Desktop/visual/project/static/csv/route_df.csv'

def read_csv(file):
    df = pd.read_csv(file)
    df.head()

    m = folium.Map([37.6174501,126.703616],zoom_start=13)

    for index, row in df.iterrows():
        folium.Marker([row['GPSlatitude'], row['GPSlongitude']]).add_to(m)

    m.save('templates/map.html') 

if __name__ == '__main__':
    read_csv()