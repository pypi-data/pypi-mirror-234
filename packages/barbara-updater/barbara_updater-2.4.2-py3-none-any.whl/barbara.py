
# Work to diminish number of lines
# Work to include user zoom on station plot map

import smbus
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import time
from time import strftime
import datetime as dt
from datetime import datetime
from datetime import timedelta #needed for determining display of 12z or 0z radiosonde
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.animation as animation
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import json
from matplotlib import rcParams
import io
from io import BytesIO
from PIL import Image
import matplotlib.image as mpimg
import traceback
import re
import imageio
from matplotlib.animation import FuncAnimation
import os
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import urllib.parse
from geopy.exc import GeocoderUnavailable
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading #allows to manage hang ups in solenium
import tkinter as tk
from tkinter import IntVar, Checkbutton
import tkinter.font as tkFont
from tkinter import ttk, IntVar
from tkinter import ttk, IntVar, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageTk
import urllib.parse
from collections import deque

global radar_identifier
global day
global hourmin_str, lat, lon

inHg_correction_factor = None
calculation_done = False # Flag to track whether barometer has been calibrated by user input

town_entry = None
town_label = None
state_entry = None
submit_button = None
next_button = None
nearest_radiosonde_station = None
#lightning_town = None
#lightning_state = None
lightning_geolocator = None
station_plot_geolocator = None
lightning_lat = None
station_plot_lat = None
lightning_lon = None
station_plot_lon = None
radar_change_code = None
submit_radar_change = None

alternative_town_1 = ""
alternative_state_1 = ""

alternative_town_2 = ""
alternative_state_2 = ""

alternative_town_3 = ""
alternative_state_3 = ""

confirmed_site_1 = False  # Initialize the confirmation flag
confirmed_site_2 = False
confirmed_site_3 = False

has_submitted_choice = False

global result, town, state, aobs_obs_site, bobs_obs_site, cobs_obs_site, aobs_url, bobs_url, cobs_url


now = datetime.now()
current_year = float(now.strftime("%Y"))

root = tk.Tk()
root.title("Weather Observer")
root.geometry("1050x600")

def get_location():
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        if data['status'] == 'success':
            lat = data['lat']
            lon = data['lon']
            return lat, lon
    except requests.exceptions.RequestException:
        pass
    return None, None

def get_aobs_site(latitude, longitude):
    global baro_input
    aobs_url = generate_aobs_url(latitude, longitude)
    nearest_html = requests.get(aobs_url)
    nearest_soup = BeautifulSoup(nearest_html.content, 'html.parser')
    panel_title = nearest_soup.find('h2', class_='panel-title')
    
    if panel_title:
        aobs_site = panel_title.text.strip()
        current_conditions = nearest_soup.find(id='current_conditions_detail')
        
        if current_conditions and isinstance(current_conditions, Tag):
            tds = current_conditions.find_all('td')
            
            if len(tds) > 5 and tds[5].string is not None:
                baro_input = tds[5].string.strip()

                try:
                    baro_input = float(baro_input[:5])
                    return aobs_site
                except ValueError:
                    print("This site doesn't have a barometric pressure reading we can use.")
                    print("Please choose an alternate site when given the chance.")
        else:
            print("The barometric reading at this site is not available for use.")
    else:
        print("Observation site not found.")
    
    return None

def get_standard_radar_site_url(latitude, longitude):
    
    global radar_site, radar_site_url
    
    aobs_url = generate_aobs_url(latitude, longitude)
    nws_html = requests.get(aobs_url)
    nws_soup = BeautifulSoup(nws_html.content, 'html.parser')
    radar_img = nws_soup.find('img', src=lambda src: src and 'radar.weather.gov/ridge/standard' in src)
    
    if radar_img:
        radar_src = radar_img['src']
        radar_site_url = radar_src.split('"')[0]
        radar_site = radar_src.split("standard/")[1][:4]
        radar_site_url = radar_site_url.replace('_0.gif', '_loop.gif')
        
        return radar_site_url
    return "Standard Radar site URL not found"

def generate_aobs_url(latitude, longitude, aobs_site=''):
    aobs_url = f"https://forecast.weather.gov/MapClick.php?lon={longitude}&lat={latitude}"
    if aobs_site:
        aobs_url += f"&site={aobs_site}"
    return aobs_url

# station_list_url is list of radiosonde sites
station_list_url = "https://www1.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt"

def get_nearest_radiosonde_station(latitude, longitude):
    global sonde_town, sonde_state, nearest_station, sonde_code, nearest_radiosonde_station
    response = requests.get(station_list_url)
    station_data = response.text.splitlines()[2:]  # Skip header lines
    min_distance = float('inf')
    nearest_station = None

    for station in station_data:
        station_info = station.split()

        try:
            station_lat = float(station_info[1])
            station_lon = float(station_info[2])
            sonde_town = " ".join(station_info[5:-3])  # Join town name with spaces
            sonde_state = station_info[4]
            station_year = station_info[-2]  # Second column from the right

            if station_year.isdigit() and int(station_year) in {current_year, current_year - 1}:
                distance = calculate_distance(latitude, longitude, station_lat, station_lon)
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = sonde_town + ", " + sonde_state
                    
        except (ValueError, IndexError):
            continue  # Skip station if there are errors in extracting data
           
    return nearest_station
    
def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [latitude1, longitude1, latitude2, longitude2])

    # Haversine formula for distance calculation
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth radius in kilometers

    return distance

# Example usage
location = get_location()
if location:
    latitude, longitude = location
    aobs_site = get_aobs_site(latitude, longitude)
    standard_radar_site_url = get_standard_radar_site_url(latitude, longitude)

    #text_widget = None  # Define text_widget as a global variable
            
    # Check if aobs_site is found
    if aobs_site:
        
        def clear_frame(frame1):
            for widget in frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Button, tk.Checkbutton, tk.Entry)):
                    widget.destroy()
        
        def close_GUI():
            root.destroy()
        
        def cobs_input_land():
            global town_entry, alternative_town_3, state_entry, alternative_state_3, result

            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                    widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

            instruction_text = "Please enter the name of the town for the third observation site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5))

            # Create an Entry widget for the user to input the town
            town_entry = tk.Entry(frame1, font=("Helvetica", 14))
            town_entry.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

            state_instruction_text = "Please enter the 2-letter state ID for the third observation site:"
            state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
            state_instructions_label.grid(row=3, column=0, padx=0, pady=(5, 5))
            
            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")

            # Create an Entry widget for the user to input the state
            state_entry = tk.Entry(frame1, font=("Helvetica", 14))
            state_entry.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")

            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_town3_and_state3, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")
            
        def submit_town3_and_state3():
            global town_entry, alternative_town_3, state_entry, alternative_state_3, result, town, state

            #command to close Onboard keyboard
            os.system("pkill onboard") 

            # Get the user's input
            town = town_entry.get()
            state = state_entry.get()

            # Set the global variable alternative_town_1 to the user's input
            alternative_town_3 = town
            alternative_state_3 = state
            
            # Continue with other actions or functions as needed
            cobs_check_land()
                    
        def bobs_input_land():
            global town_entry, alternative_town_2, state_entry, alternative_state_2, result

            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

            instruction_text = "Please enter the name of the town for the second observation site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5))

            # Create an Entry widget for the user to input the town
            town_entry = tk.Entry(frame1, font=("Helvetica", 14))
            town_entry.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

            state_instruction_text = "Please enter the 2-letter state ID for the second observation site:"
            state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
            state_instructions_label.grid(row=3, column=0, padx=0, pady=(5, 5))

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")
 
            # Create an Entry widget for the user to input the state
            state_entry = tk.Entry(frame1, font=("Helvetica", 14))
            state_entry.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")

            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_town2_and_state2, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")
            
        def submit_town2_and_state2():
            global town_entry, alternative_town_2, state_entry, alternative_state_2, result, town, state

            #command to close Onboard keyboard
            os.system("pkill onboard") 
        
            # Get the user's input
            town = town_entry.get()
            state = state_entry.get()

            # Set the global variable alternative_town_1 to the user's input
            alternative_town_2 = town
            alternative_state_2 = state
            
            # Continue with other actions or functions as needed
            bobs_check_land()
            
        def aobs_input_land():
            global town_entry, alternative_town_1, state_entry, alternative_state_1, result

            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

            instruction_text = "Please enter the name of the town for the first observation site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5))

            # Create an Entry widget for the user to input the town
            town_entry = tk.Entry(frame1, font=("Helvetica", 14))
            town_entry.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

            state_instruction_text = "Please enter the 2-letter state ID for the first observation site:"
            state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
            state_instructions_label.grid(row=3, column=0, padx=0, pady=(5, 5))

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")

            # Create an Entry widget for the user to input the state
            state_entry = tk.Entry(frame1, font=("Helvetica", 14))
            state_entry.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")

            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_town1_and_state1, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")
            
        def submit_town1_and_state1():
            global town_entry, alternative_town_1, state_entry, alternative_state_1, result, town, state

            #command to close Onboard keyboard
            os.system("pkill onboard") 

            # Get the user's input
            town = town_entry.get()
            state = state_entry.get()

            # Set the global variable alternative_town_1 to the user's input
            alternative_town_1 = town
            alternative_state_1 = state
         
            # Continue with other actions or functions as needed
            aobs_check_land()
            
        def cobs_input_buoy():
            pass
        
        def bobs_input_buoy():
            global town_entry, alternative_town_2, state_entry, alternative_state_2, result

            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = "Please enter the 5-character code for the buoy for the second site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
            
            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")
             
            # Create an Entry widget for the user to input the town
            town_entry = tk.Entry(frame1, font=("Helvetica", 14))
            town_entry.grid(row=2, column=0, padx=50, pady=(20, 30), sticky="w")
                        
            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=bobs_submit_buoy_code, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(20, 30), sticky="w")
            
        def bobs_submit_buoy_code():
            global town_entry, alternative_town_2, result, town, state

            #command to close Onboard keyboard
            os.system("pkill onboard") 

            # Get the user's input
            town = town_entry.get()

            # Set the global variable alternative_town_1 to the user's input
            alternative_town_2 = town
            
            # Continue with other actions or functions as needed
            bobs_check_buoy()            
        
        def aobs_input_buoy():
            global town_entry, alternative_town_1, state_entry, alternative_state_1, result

            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = "Please enter the 5-character code for the buoy for the first site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")
 
            # Create an Entry widget for the user to input the town
            town_entry = tk.Entry(frame1, font=("Helvetica", 14))
            town_entry.grid(row=2, column=0, padx=50, pady=(20, 30), sticky="w")
                        
            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=aobs_submit_buoy_code, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(20, 30), sticky="w")
            
        def aobs_submit_buoy_code():
            global town_entry, alternative_town_1, result, town, state

            #command to close Onboard keyboard
            os.system("pkill onboard") 

            # Get the user's input
            town = town_entry.get()

            # Set the global variable alternative_town_1 to the user's input
            alternative_town_1 = town
         
            # Continue with other actions or functions as needed
            aobs_check_buoy()
                   
        
        def cobs_check_land():
            global alternative_town_3, alternative_state_3, confirmed_site_3, result, town, state, cobs_site, cobs_obs_site, cobs_url
            
            alternative_town_3 = town
            alternative_state_3 = state
            
            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                    widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 
            
            try:
                # Geocode the alternative town to get the latitude and longitude
                geolocator = Nominatim(user_agent="geocoder_app")
                
                #print(alternative_town_3, alternative_state_3)
                
                location_3 = geolocator.geocode(f"{alternative_town_3}, {alternative_state_3}", country_codes="us")
                
                if location_3 is not None:
                    alternative_latitude_3 = location_3.latitude
                    alternative_longitude_3 = location_3.longitude

                    # trying to stop an error, so just copying what was done for aobs
                    def generate_cobs_url(alternative_latitude_3, alternative_longitude_3, cobs_site=''):
                        cobs_url = f"https://forecast.weather.gov/MapClick.php?lon={alternative_longitude_3}&lat={alternative_latitude_3}"
                        if cobs_site:
                            cobs_url += f"&site={cobs_site}"
                        return cobs_url

                    # Generate the NWS URL for the alternative site
                    cobs_url = generate_cobs_url(alternative_latitude_3, alternative_longitude_3)
                    alternative_html = requests.get(cobs_url)
                    alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

                    extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
                    current_conditions = alternative_soup.find("div", id="current-conditions")
                    if extended_forecast is not None:
                        cobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                        cobs_obs_site = current_conditions.find("h2", class_="panel-title").text.strip()
                        
                        
                        site_1_text = f"The nearest official observation to {alternative_town_3.title()} is {cobs_obs_site}"
                        site_1_label = tk.Label(frame1, text=site_1_text, font=("Helvetica", 16,))
                        site_1_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                        
                        confirm_button = tk.Button(frame1, text="Keep", command=cobs_confirm_land, font=("Helvetica", 16, "bold"))
                        confirm_button.grid(row=2, column=0, padx=(50, 0), pady=5, sticky='w')
                        
                        choose_another_button = tk.Button(frame1, text="Change", command=cobs_land_or_buoy, font=("Helvetica", 16, "bold"))
                        choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')
                        
                    else:
                        print("Failed to retrieve observation site for Observation Site 3.")
                else:
                    print("Failed to retrieve latitude and longitude for the specified town and state for Observation Site 3.")
            except GeocoderUnavailable:
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

                instruction_text = "Geocoding service is unavailable. Please click 'Next' and try again later"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))                 

                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, land_or_buoy)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")     
        
        
        def bobs_check_land():
            global alternative_town_2, alternative_state_2, confirmed_site_2, result, town, state, bobs_site, bobs_obs_site, bobs_url
            
            alternative_town_2 = town
            alternative_state_2 = state 
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 
            
            try:
                # Geocode the alternative town to get the latitude and longitude
                geolocator = Nominatim(user_agent="geocoder_app")
                
                #print(alternative_town_1, alternative_state_1)
                
                location_2 = geolocator.geocode(f"{alternative_town_2}, {alternative_state_2}", country_codes="us")
                
                if location_2 is not None:
                    alternative_latitude_2 = location_2.latitude
                    alternative_longitude_2 = location_2.longitude

                    # trying to stop an error, so just copying what was done for aobs
                    def generate_bobs_url(alternative_latitude_2, alternative_longitude_2, bobs_site=''):
                        bobs_url = f"https://forecast.weather.gov/MapClick.php?lon={alternative_longitude_2}&lat={alternative_latitude_2}"
                        if bobs_site:
                            bobs_url += f"&site={bobs_site}"
                        return bobs_url

                    # Generate the NWS URL for the alternative site
                    bobs_url = generate_bobs_url(alternative_latitude_2, alternative_longitude_2)
                    alternative_html = requests.get(bobs_url)
                    alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

                    extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
                    current_conditions = alternative_soup.find("div", id="current-conditions")
                    if extended_forecast is not None:
                        bobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                        bobs_obs_site = current_conditions.find("h2", class_="panel-title").text.strip()
                        
                        
                        site_1_text = f"The nearest official observation to {alternative_town_2.title()} is {bobs_obs_site}"
                        site_1_label = tk.Label(frame1, text=site_1_text, font=("Helvetica", 16,))
                        site_1_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                        
                        confirm_button = tk.Button(frame1, text="Keep", command=bobs_confirm_land, font=("Helvetica", 16, "bold"))
                        confirm_button.grid(row=2, column=0, padx=(50, 0), pady=5, sticky='w')
                        
                        choose_another_button = tk.Button(frame1, text="Change", command=bobs_land_or_buoy, font=("Helvetica", 16, "bold"))
                        choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')
                        
                    else:
                        print("Failed to retrieve observation site for Observation Site 2.")
                        
                        # Clear the current display
                        for widget in frame1.winfo_children():
                            widget.destroy()
                        
                        # Create and display the updated labels
                        label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                        label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
 
                        
                        instruction_text = "Failed to find that location. Please click 'Next' and try another site."
                        instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                        instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))                 
                        
                        # Create the 'Next' button
                        next_button = create_button(frame1, "Next", button_font, bobs_land_or_buoy)
                        next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")
                        
                else:
                    print("Failed to retrieve latitude and longitude for the specified town and state for Observation Site 2.")
                    
                    # Clear the current display
                    for widget in frame1.winfo_children():
                        widget.destroy()
                    
                    # Create and display the updated labels
                    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                    label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
                    
                    instruction_text = "Failed to find that location. Please click 'Next' and try another site."
                    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))                 
                    
                    # Create the 'Next' button
                    next_button = create_button(frame1, "Next", button_font, bobs_land_or_buoy)
                    next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")      
                    
            except GeocoderUnavailable:
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

                instruction_text = "Geocoding service is unavailable. Please click 'Next' and try again later"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))                 

                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, bobs_land_or_buoy)
                next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")     
         
        def aobs_check_land():
            global alternative_town_1, alternative_state_1, confirmed_site_1, result, town, state, aobs_obs_site, aobs_url
            
            alternative_town_1 = town
            alternative_state_1 = state
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 
            
            try:
                # Geocode the alternative town to get the latitude and longitude
                geolocator = Nominatim(user_agent="geocoder_app")
                
                #print(alternative_town_1, alternative_state_1)
                
                location_1 = geolocator.geocode(f"{alternative_town_1}, {alternative_state_1}", country_codes="us")
                
                if location_1 is not None:
                    alternative_latitude_1 = location_1.latitude
                    alternative_longitude_1 = location_1.longitude

                    # Generate the NWS URL for the alternative site
                    aobs_url = generate_aobs_url(alternative_latitude_1, alternative_longitude_1)
                    alternative_html = requests.get(aobs_url)
                    alternative_soup = BeautifulSoup(alternative_html.content, 'html.parser')

                    extended_forecast = alternative_soup.find("div", id="seven-day-forecast")
                    current_conditions = alternative_soup.find("div", id="current-conditions")
                    if extended_forecast is not None:
                        aobs_town = extended_forecast.find("h2", class_="panel-title").text.strip()
                        aobs_obs_site = current_conditions.find("h2", class_="panel-title").text.strip()
                        
                        
                        site_1_text = f"The nearest official observation to {alternative_town_1.title()} is {aobs_obs_site}"
                        site_1_label = tk.Label(frame1, text=site_1_text, font=("Helvetica", 16,))
                        site_1_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                        
                        confirm_button = tk.Button(frame1, text="Keep", command=aobs_confirm_land, font=("Helvetica", 16, "bold"))
                        confirm_button.grid(row=2, column=0, padx=(50, 0), pady=5, sticky='w')
                        
                        choose_another_button = tk.Button(frame1, text="Change", command=land_or_buoy, font=("Helvetica", 16, "bold"))
                        choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')
                        
                    else:
                        fail_obs_text = f"Failed to retrieve observation from {alternative_town_1}. Please change the site."
                        fail_obs_label = tk.Label(rame1, text=fail_obs_text, font=("Helvetica", 16,))
                        fail_obs_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                        
                        choose_another_button = tk.Button(frame1, text="Change", command=land_or_buoy, font=("Helvetica", 16, "bold"))
                        choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')
                            
                else:
                    fail_obs_text = f"Failed to retrieve latitude and longitude for {alternative_town_1}. Please change the site."
                    fail_obs_label = tk.Label(rame1, text=fail_obs_text, font=("Helvetica", 16,))
                    fail_obs_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                    
                    choose_another_button = tk.Button(frame1, text="Change", command=land_or_buoy, font=("Helvetica", 16, "bold"))
                    choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')

            except GeocoderUnavailable:
                fail_obs_text = f"Geocoding service is unavailable for {alternative_town_1}. Try later, or please change the site."
                fail_obs_label = tk.Label(rame1, text=fail_obs_text, font=("Helvetica", 16,))
                fail_obs_label.grid(row=1, column=0, padx=50, pady=(0, 45))
                
                choose_another_button = tk.Button(frame1, text="Change", command=land_or_buoy, font=("Helvetica", 16, "bold"))
                choose_another_button.grid(row=2, column=0, padx=160, pady=5, sticky='w')

        
        def bobs_check_buoy():
            global alternative_town_2, town_entry, result, bobs_url
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
            
            # Build the URL using the buoy code
            bobs_url = f"https://www.ndbc.noaa.gov/station_page.php?station={alternative_town_2}"
            response = requests.get(bobs_url)
            
            if response.status_code == 200:           
                confirmed_site_2 = True
                
                accept_text = f"Buoy {alternative_town_2} will be used for the second observation site."
                accept_label = tk.Label(frame1, text=accept_text, font=("Helvetica", 16,))
                accept_label.grid(row=1, column=0, padx=50, pady=(20,10))
            else:
                deny_text = f"Not able to find a buoy with that code. Please choose another site."
                deny_label = tk.Label(frame1, text=deny_text, font=("Helvetica", 16,))
                deny_label.grid(row=1, column=0, padx=50, pady=(20,10))
                bobs_land_or_buoy()
            
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, cobs_input_land)
            next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")     
                
        def aobs_check_buoy():
            global alternative_town_1, town_entry, result, aobs_url
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
            
            # Build the URL using the buoy code
            aobs_url = f"https://www.ndbc.noaa.gov/station_page.php?station={alternative_town_1}"
            response = requests.get(aobs_url)
            
            if response.status_code == 200:           
                confirmed_site_1 = True
                
                accept_text = f"Buoy {alternative_town_1} will be used for the first observation site."
                accept_label = tk.Label(frame1, text=accept_text, font=("Helvetica", 16,))
                accept_label.grid(row=1, column=0, padx=50, pady=(20,10))
            else:
                deny_text = f"Not able to find a buoy with that code. Please choose another site."
                deny_label = tk.Label(frame1, text=deny_text, font=("Helvetica", 16,))
                deny_label.grid(row=1, column=0, padx=50, pady=(20,10))
                land_or_buoy()
            
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, bobs_land_or_buoy)
            next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")     
                        
        def cobs_confirm_land():
            global town_entry, alternative_town_3, state_entry, alternative_state_3, result, cobs_site, cobs_obs_site

            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                    widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = f"{cobs_obs_site} will be used for the third observation site."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
            
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, lightning_center_input)
            next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")     
                        
        def bobs_confirm_land():
            global town_entry, alternative_town_2, state_entry, alternative_state_2, result, bobs_site, bobs_obs_site

            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                    widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = f"{bobs_obs_site} will be used for the second observation site."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
            
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, cobs_input_land)
            next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")       
        
        def aobs_confirm_land():
            global town_entry, alternative_town_1, state_entry, alternative_state_1, result, aobs_obs_site

            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                    widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = f"{aobs_obs_site} will be used for the first observation site."
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
            
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, bobs_land_or_buoy)
            next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w")            
            
        
        def create_button(frame1, text, font, command_func):
            button = tk.Button(frame1, text=text, font=font, command=command_func)
            return button
        
        def remove_checkbox():
            choice_check_button.destory()
            
        def choose_reg_sat():
            
            reg_sat_choice_variables = [None] * 12
            
            global box_variables, reg_sat, has_submitted_choice 
            
            if box_variables[5] != 1:
                land_or_buoy()
            elif not has_submitted_choice:
            
                def update_sat_checkboxes(chosen_index):
                    
                    for index, var in enumerate(choice_vars):
                        if index == chosen_index:
                            var.set(1)
                        else:
                            var.set(0)

                def sat_checkbox_clicked(index):
                    def inner():
                        if not has_submitted_choice:  # Check the flag
                            update_sat_checkboxes(index)
                    return inner

                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

                instruction_text = "Please select your regional satellite view:"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 14, "bold"))
                instructions_label.grid(row=1, column=0, padx=50, pady=(0, 25), sticky='w') 

                # Create a custom style for the check buttons
                custom_style = ttk.Style()
                custom_style.configure("Custom.TCheckbutton", font=("Arial", 14, "bold"))  # Set the font properties

                choice_vars = []
                choices = ['Pacific NW', 'Pacific SW', 'Northern Rockies', 'Southern Rockies', 'Upper Miss. Valley',
                           'Southern Miss. Valley', 'Great Lakes', 'Southern Plains', 'Northeast', 'Southeast',
                           'US Pacific Coast', 'US Atlantic Coast']

                column1_frame = tk.Frame(frame1)
                column2_frame = tk.Frame(frame1)
                column3_frame = tk.Frame(frame1)

                v_spacing = 55
                h_spacing = 45

                choice_check_buttons = []

                for index in range(len(choices)):
                    var = tk.IntVar(value=0)
                    choice_vars.append(var)
                    choice_check_button = ttk.Checkbutton(
                        column1_frame if index < 4 else (column2_frame if index < 8 else column3_frame),
                        text=choices[index], variable=var, onvalue=1, offvalue=0,
                        style="Custom.TCheckbutton",
                        command=sat_checkbox_clicked(index)
                    )
                    choice_check_button.grid(row=index % 4, column=index // 4, padx=10, pady=(5, v_spacing), sticky='w')
                    choice_check_buttons.append(choice_check_button)
                                        
                    #if index in {10}:
                        #var.set(2)
                        #choice_check_button.state(["disabled"])

                column1_frame.grid(row=2, column=0, padx=(50, 0), sticky='w')
                column2_frame.grid(row=2, column=0, padx=(310, 0), sticky='w')
                column3_frame.grid(row=2, column=0, padx=(610, 0), pady=(20, 20), sticky='w')

                def submit_sat_choice():
                    global reg_sat_choice_variables, has_submitted_choice
                    reg_sat_choice_variables = [var.get() for var in choice_vars]
                    for index, value in enumerate(reg_sat_choice_variables):
                        if value == 1:
                            # Adjust the values as needed based on your requirements
                            #reg_sat_choice_variables[index] = 2 if index in {10} else 1
                            reg_sat_choice_variables[index] = 1
                            has_submitted_choice = True
                     
                    # Clear the current display                    
                    for widget in frame1.winfo_children():
                        if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):                            
                            widget.destroy()
                            
                    # Clear the current display
                    for widget in frame1.winfo_children():
                        widget.destroy()
                    
                    # Destroy all checkboxes
                    for checkbox in choice_check_buttons:
                        checkbox.destroy()
                    
                    land_or_buoy()

                    # Print the values of the checkbox choices
                    #for i, value in enumerate(reg_sat_choice_variables, start=1):
                        #print(f"reg_sat_choice{i}: {value}")

                submit_frame = tk.Frame(frame1)
                submit_frame.grid(row=4, column=0, padx=0, pady=10, sticky='se')
                submit_button = tk.Button(frame1, text="Submit", command=submit_sat_choice, font=("Arial", 14, "bold"))
                submit_button.grid(row=4, column=3)
                
        
        def page_choose():
            
            box_variables = [None] * 12 
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
            
            instruction_text = "Please select your display choices:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(0, 25), sticky='w')       
            
            # Create a custom style for the check buttons
            custom_style = ttk.Style()
            custom_style.configure("Custom.TCheckbutton", font=("Arial", 14, "bold"))  # Set the font properties
            
            choice_vars = []
            choices = ['Barograph', 'National Radar', 'Local Radar', 'Lightning', 'GOES16 East Satellite',
                       'Regional Satellite', 'National Surface Analysis', 'Local Station Plots', 'Radiosonde', '500mb Vorticity',
                       'GFS 1 Week', 'GFS 2 Week']

            column1_frame = tk.Frame(frame1)
            column2_frame = tk.Frame(frame1)
            column3_frame = tk.Frame(frame1)

            v_spacing = 55
            h_spacing = 45

            # Create the list to store the checkboxes
            choice_check_buttons = []

            for index in range(len(choices)):
                var = tk.IntVar(value=0)
                choice_vars.append(var)
                choice_check_button = ttk.Checkbutton(
                    column1_frame if index < 4 else (column2_frame if index < 8 else column3_frame),
                    text=choices[index], variable=var, onvalue=1, offvalue=0,
                    style="Custom.TCheckbutton"  # Use the custom style
                )
                choice_check_button.grid(row=index % 4, column=index // 4, padx=10, pady=(5, v_spacing), sticky='w')
                choice_check_buttons.append(choice_check_button) 


                if index == 0:
                    var.set(1)
                    choice_check_button.state(["disabled"])
                elif index in {9, 10, 11}:
                    var.set(2)
                    choice_check_button.state(["disabled"])
                        
            column1_frame.grid(row=2, column=0, padx=50, sticky='w')
            column2_frame.grid(row=2, column=0, padx=350, sticky='w')
            column3_frame.grid(row=2, column=0, padx=700, sticky='w')

            def submit_choices():
                global box_variables
                box_variables = [var.get() for var in choice_vars]
                for index, value in enumerate(box_variables):
                    if value == 1:
                        # Adjust the values as needed based on your requirements
                        box_variables[index] = 2 if index in {9, 10, 11} else 1               

                #Print the values of the checkbox choices
                #for c, value in enumerate(box_variables, start=1):
                    #print(f"box{c}: {value}")
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                
                # Destroy all checkboxes
                for checkbox in choice_check_buttons:
                    checkbox.destroy()
                
                choose_reg_sat()

            submit_frame = tk.Frame(frame1)
            submit_frame.grid(row=3, column=0, padx=60, pady=10, sticky='se')
            submit_button = tk.Button(frame1, text="Submit", command=submit_choices, font=("Arial", 14, "bold"))
            submit_button.grid(row=3, column=0)
            
        def submit_lightning_center():
            global submit_lightning_town, submit_lightning_state, lightning_town, lightning_state, lightning_lat, lightning_lon 

            #command to close Onboard keyboard
            os.system("pkill onboard")  

            lightning_geolocator = Nominatim(user_agent="lightning_map")
            
            # Get the user's input
            submit_lightning_town = lightning_town.get()
            submit_lightning_state = lightning_state.get()
            
            # Combine town and state into a search query
            lightning_query = f"{submit_lightning_town}, {submit_lightning_state}"

            # Use geocoder to get coordinates of lightning map center
            lightning_location = lightning_geolocator.geocode(lightning_query)
        
            if lightning_location:
                lightning_lat = lightning_location.latitude
                lightning_lon = lightning_location.longitude
                station_center_input()
                #break
            else:
                # Clear the current display
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                        widget.destroy()
                        
                instruction_text = "Not able to use that location as center."
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
                
                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, lightning_center_input)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")  
                      
        def lightning_center_input():
            
            if box_variables[3] == 1: 
                        
                global lightning_town, lightning_state, submit_lightning_town, submit_lightning_state
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                        widget.destroy()

                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

                instruction_text = "Please enter the name of the town for the center of the lightning map:"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5))

                # Create an Entry widget for the user to input the town
                lightning_town = tk.Entry(frame1, font=("Helvetica", 14))
                lightning_town.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

                state_instruction_text = "Please enter the 2-letter state ID for the center of the lightning map:"
                state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
                state_instructions_label.grid(row=3, column=0, padx=0, pady=(5, 5))

                # Suppress the error message by redirecting standard error output to /dev/null
                os.system("onboard 2>/dev/null &")

                # Create an Entry widget for the user to input the state
                lightning_state = tk.Entry(frame1, font=("Helvetica", 14))
                lightning_state.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")
                
                submit_lightning_town = lightning_town.get()
                submit_lightning_state = lightning_state.get()
                
                # Create a submit button to process the user's input
                submit_button = tk.Button(frame1, text="Submit", command=submit_lightning_center, font=("Helvetica", 16, "bold"))
                submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")            
        
            else:
                station_center_input()
            

        def submit_station_plot_center():
            
            global submit_station_plot_town, submit_station_plot_state, station_plot_town, station_plot_state, station_plot_lat, station_plot_lon, zoom_plot 
            
            #command to close Onboard keyboard
            os.system("pkill onboard") 
            
            station_plot_geolocator = Nominatim(user_agent="station_plot_map")
            
            # Get the user's input
            submit_station_plot_town = station_plot_town.get()
            submit_station_plot_state = station_plot_state.get()
            
            #retrieve user's zoom choice
            zoom_plot = zoom_plot.get()
            
            # Combine town and state into a search query
            station_plot_query = f"{submit_station_plot_town}, {submit_station_plot_state}"
            
            # Use geocoder to get coordinates of lightning map center
            station_plot_location = station_plot_geolocator.geocode(station_plot_query)
        
            if station_plot_location:
                station_plot_lat = station_plot_location.latitude
                station_plot_lon = station_plot_location.longitude
                close_GUI()
                #break
            else:
                # Clear the current display
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button, tk.Entry)):
                        widget.destroy()
                        
                instruction_text = "Not able to use that location as center."
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
                
                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, station_center_input)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")
                
                station_center_input()
                
            
        def station_center_input():
                     
            if box_variables[7] == 1: 
                        
                global station_plot_town, station_plot_state, submit_station_plot_town, submit_station_plot_state, zoom_plot
                
                # Initialize a variable to keep track of the user's choice
                zoom_plot = tk.StringVar(value="9")
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                        widget.destroy()

                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

                instruction_text = "Please enter the name of the town for the center of the station plot map:"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5), sticky='w')

                # Create an Entry widget for the user to input the town
                station_plot_town = tk.Entry(frame1, font=("Helvetica", 14))
                station_plot_town.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

                state_instruction_text = "Please enter the 2-letter state ID for the center of the station plot map:"
                state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
                state_instructions_label.grid(row=3, column=0, padx=50, pady=(5, 5), sticky='w')

                # Create an Entry widget for the user to input the state
                station_plot_state = tk.Entry(frame1, font=("Helvetica", 14))
                station_plot_state.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")

                # Create a label for the radio buttons
                radio_label = tk.Label(frame1, text="How far to zoom in or out?:", font=("Helvetica", 16))
                radio_label.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")

                # Create and place the radio buttons
                radio_buttons = [("Few small\ncounties", "10"), ("Several\ncounties", "9"), ("States", "6"), ("Continents", "4"), ("Almost a\nhemisphere", "3")]
                for p, (text, value) in enumerate(radio_buttons):
                    radio_button = tk.Radiobutton(frame1, text=text, variable=zoom_plot, value=value, font=("Helvetica", 11), justify="left")
                    radio_button.grid(row=6, column=0, padx=(200*p + 50), pady=(5, 5), sticky="w")

                # Suppress the error message by redirecting standard error output to /dev/null
                os.system("onboard 2>/dev/null &")
             
                #submit_station_plot_town = station_plot_town.get()
                #submit_station_plot_state = station_plot_state.get()
                
                # Create a submit button to process the user's input
                submit_button = tk.Button(frame1, text="Submit", command=submit_station_plot_center, font=("Helvetica", 16, "bold"))
                submit_button.grid(row=7, column=0, padx=50, pady=(5, 5), sticky="w")
                
            else:
                close_GUI()
                
             
        def cobs_land_or_buoy():
            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                    widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=20, sticky="w")
            
            instruction_text = "Do you want the third observation site to be on land or a buoy?"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=0)
            
            # Create "Land" button
            land_button = create_button(frame1, "Land", button_font, cobs_input_land)
            land_button.grid(row=2, column=0, padx=50, pady=30, sticky="w")

            # Create "Buoy" button
            buoy_button = create_button(frame1, "Buoy", button_font, cobs_input_buoy)
            buoy_button.grid(row=2, column=0, padx=210, pady=30, sticky="w")
            
        def bobs_land_or_buoy():
            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label, tk.Button)):
                    widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=20, sticky="w")
            
            instruction_text = "Do you want the second observation site to be on land or a buoy?"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=0)
            
            # Create "Land" button
            land_button = create_button(frame1, "Land", button_font, bobs_input_land)
            land_button.grid(row=2, column=0, padx=50, pady=30, sticky="w")

            # Create "Buoy" button
            buoy_button = create_button(frame1, "Buoy", button_font, bobs_input_buoy)
            buoy_button.grid(row=2, column=0, padx=210, pady=30, sticky="w")
                
        def land_or_buoy():
            
            # Clear the current display
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label)):
                    print("destroy widgets in land_or_buoy.")
                    widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=20, sticky="w")
            
            instruction_text = "Do you want the first observation site to be on land or a buoy?"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=0)
            
            # Create "Land" button
            land_button = create_button(frame1, "Land", button_font, aobs_input_land)
            land_button.grid(row=2, column=0, padx=50, pady=30, sticky="w")

            # Create "Buoy" button
            buoy_button = create_button(frame1, "Buoy", button_font, aobs_input_buoy)
            buoy_button.grid(row=2, column=0, padx=210, pady=30, sticky="w")
            

        def confirm_radiosonde_site():
            
            global sonde_letter_identifier
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
            
            # Build the URL for the NWS office based on latitude and longitude
            nws_url = f"https://forecast.weather.gov/MapClick.php?lat={latitude}&lon={longitude}"

            try:
                # Fetch the HTML content of the NWS office page
                response = requests.get(nws_url)
                response.raise_for_status()

                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Find the Local Forecast Office link and extract the 3-letter code
                local_forecast_link = soup.find("a", id="localWFO")            
                        
                if local_forecast_link:
                    local_forecast_url = local_forecast_link["href"]

                    # Extract the NWS 3-letter code from the Local Forecast Office URL
                    code_match = re.search(r"https://www.weather.gov/([A-Za-z]{3})/", local_forecast_url)
                    if code_match:
                        sonde_letter_identifier = code_match.group(1).upper()  # Convert to uppercase
                        #print(f"NWS 3-Letter Code for {sonde_town}, {sonde_state}: {sonde_letter_identifier}")
                    else:
                        print("NWS 3-Letter Code not found in the Local Forecast Office URL.")
                else:
                    print("Could not match site with its 3-letter code.")
                
            except requests.RequestException as e:
                print("Error occurred during API request:", str(e)) 
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
            
            updated_text = f"{nearest_station}"
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=1, column=0, padx=90, pady=(0, 10), sticky='w')
            
            updated_text = f"will be used as the radiosonde site."
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=2, column=0, padx=90, pady=(0, 10), sticky='w') 
             
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, page_choose)
            next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")
        
        def submit_radiosonde_change():
            global radiosonde_change_code, submit_radiosonde_change, test_submit_radiosonde_change, sonde_letter_identifier
            
            #command to close Onboard keyboard
            os.system("pkill onboard")  
            
            # Clear the current display of only Checkbutton and Label
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label)):
                    widget.destroy()         
            
            test_submit_radiosonde_change = radiosonde_change_code.get()
            sonde_letter_identifier = test_submit_radiosonde_change.upper()
       
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
            
            # Get current UTC time and date
            scrape_now = datetime.utcnow()

            if scrape_now.hour >= 1 and scrape_now.hour < 13:
                # Use 00z for current UTC date
                date_str = scrape_now.strftime("%y%m%d00")
                hour_str = "00Z"
            else:
                # Use 12z for current UTC date
                hour_str = "12Z"
                date_str = scrape_now.strftime("%y%m%d12")
                if scrape_now.hour < 1:
                    # Use previous UTC date for 00z images
                    scrape_now -= timedelta(days=1)
                    date_str = scrape_now.strftime("%y%m%d12")
                
            month_str = scrape_now.strftime("%b").capitalize()
            day_str = str(scrape_now.day)
            
            radiosonde_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}_OBS/{sonde_letter_identifier}.gif"
            
            # Send a GET request to the URL
            response = requests.get(radiosonde_url)
            
            # Check if the response status code is 200
            if response.status_code == 200:
                # Clear the current display of only Checkbutton and Label
                for widget in frame1.winfo_children():
                    if isinstance(widget, (tk.Checkbutton, tk.Button, tk.Label, tk.Entry)):
                        widget.destroy()
                
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
                
                updated_text = f"{sonde_letter_identifier}"
                label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
                label2.grid(row=1, column=0, padx=90, pady=(0, 10), sticky='w')
                
                updated_text = f"will be used as the radiosonde site."
                label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
                label2.grid(row=1, column=0, padx=140, pady=(0, 10), sticky='w') 
                 
                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, page_choose)
                next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")     
                
            else:
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                 
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
                        
                instruction_text = "That radiosonde site could not be found. Please click 'Next' to keep or change default radiosonde site"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=0)
                
                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, radiosonde_site_question)
                next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w") 
            
        
        def change_radiosonde_site():
            global radiosonde_change_code, test_submit_radiosonde_change 
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = "Please enter the 3-letter code for the radiosonde site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")
 
            # Create an Entry widget for the user to input the town
            radiosonde_change_code = tk.Entry(frame1, font=("Helvetica", 14))
            radiosonde_change_code.grid(row=2, column=0, padx=50, pady=(20, 30), sticky="w")
            
            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_radiosonde_change, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(20, 30), sticky="w")
        
        def radiosonde_site_question():
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
                
            get_nearest_radiosonde_station(latitude, longitude)

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")

            updated_text = f"The default radiosonde site is: {nearest_station}\n\nDo you want to keep the default radiosonde site, or\nchange to another site?\n"
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=1, column=0, padx=85, pady=(0, 10))
            
            # Recreate 'Keep' and 'Change' buttons
            keep_button = create_button(frame1, "Keep", button_font, confirm_radiosonde_site)
            keep_button.grid(row=2, column=0, padx=(81, 0), pady=5, sticky="w")

            change_button = create_button(frame1, "Change", button_font, change_radiosonde_site)
            change_button.grid(row=2, column=0, padx=200, pady=5, sticky="w") 
            
        
        def confirm_radar_site():
            
            global radar_identifier
            
            radar_identifier = radar_site
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
             
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
            
            updated_text = f"{radar_site}"
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=1, column=0, padx=90, pady=(0, 10), sticky='w')
            
            updated_text = f"will be used as the radar site."
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=1, column=0, padx=160, pady=(0, 10), sticky='w') 
             
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, radiosonde_site_question)
            next_button.grid(row=3, column=0, padx=(90, 0), pady=10, sticky="w")

        def submit_radar_change():
            
            global radar_loop_url, radar_change_code, submit_radar_change, radar_site
            
            #command to close Onboard keyboard
            os.system("pkill onboard")  
            
            # Clear the current display of only Checkbutton and Label
            for widget in frame1.winfo_children():
                if isinstance(widget, (tk.Checkbutton, tk.Label)):
                    widget.destroy()         
            
            test_submit_radar_change = radar_change_code.get()
            test_submit_radar_change = test_submit_radar_change.upper()
            #radar_site = submit_radar_change
            #radar_site = radar_site.upper()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")
            
            radar_loop_url = f"https://radar.weather.gov/ridge/standard/{test_submit_radar_change}_loop.gif"
            
            # Send a GET request to the URL
            response = requests.get(radar_loop_url)

            # Check if the response status code is 200
            if response.status_code == 200:
                
                radar_site = test_submit_radar_change
                confirm_radar_site()
                
            else:
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                 
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
                        
                instruction_text = "That radar site could not be found. Please click 'Next' to keep or change default radar site"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=0)
                
                # Create the 'Next' button
                next_button = create_button(frame1, "Next", button_font, radar_site_question)
                next_button.grid(row=3, column=0, padx=(50, 0), pady=10, sticky="w") 
                
        def change_radar_site():
            
            global radar_change_code, submit_radar_change
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")

            instruction_text = "Please enter the 4-letter code for the radar site:"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
            instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")

            # Create an Entry widget for the user to input the town
            radar_change_code = tk.Entry(frame1, font=("Helvetica", 14))
            radar_change_code.grid(row=2, column=0, padx=50, pady=(20, 30), sticky="w")
            
            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_radar_change, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(20, 30), sticky="w")
        
        def confirm_calibration_site():
            global submit_calibration_town
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            #command to close Onboard keyboard
            os.system("pkill onboard")  
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"))
            label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")
            
            updated_text = f"{aobs_site}"
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16))
            label2.grid(row=1, column=0, padx=90, pady=(0, 10), sticky='w')
            
            updated_text = f"will be used as the calibration site."
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16))
            label2.grid(row=2, column=0, padx=90, pady=(20, 30), sticky='w') 
             
            # Create the 'Next' button
            next_button = create_button(frame1, "Next", button_font, radar_site_question)
            next_button.grid(row=3, column=0, padx=(90, 0), pady=5, sticky="w")
                        
        def radar_site_question():
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer\n", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=90, pady=(10, 0), sticky="w")

            updated_text = f"The default radar site is: {radar_site}\n\nDo you want to keep the default radar site, or\nchange to another site?\n"
            label2 = tk.Label(frame1, text=updated_text, font=("Arial", 16), justify="left")
            label2.grid(row=1, column=0, padx=90, pady=(0, 10))

            # Recreate 'Keep' and 'Change' buttons
            keep_button = create_button(frame1, "Keep", button_font, confirm_radar_site)
            keep_button.grid(row=2, column=0, padx=(90, 0), pady=5, sticky="w")

            change_button = create_button(frame1, "Change", button_font, change_radar_site)
            change_button.grid(row=2, column=0, padx=200, pady=5, sticky="w")
            
        def submit_calibration_input():
            global submit_calibration_town, submit_calibration_state, calibration_town, calibration_state, calibration_lat, calibration_lon, aobs_site 
            
            submit_calibration_town = calibration_town.get()
            submit_calibration_state = calibration_state.get()
            
            # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()
            
            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=10, sticky="w") 
            
            try:
                # Geocode the alternative town to get the latitude and longitude
                geolocator = Nominatim(user_agent="geocoder_app")
                                
                change_calibration = geolocator.geocode(f"{submit_calibration_town}, {submit_calibration_state}", country_codes="us")
                
                if change_calibration is not None:
                    change_calibration_lat = change_calibration.latitude
                    change_calibration_lon = change_calibration.longitude

                    # Generate the NWS URL for the change calibration site
                    change_calibration_url = f"https://forecast.weather.gov/MapClick.php?lon={change_calibration_lon}&lat={change_calibration_lat}"
                    change_calibration_html = requests.get(change_calibration_url)
                    change_calibration_soup = BeautifulSoup(change_calibration_html.content, 'html.parser')
                
                    current_conditions = change_calibration_soup.find(id='current_conditions_detail')
                                        
                    tds = current_conditions.find_all('td')
                    baro_input = tds[5].string.strip()
                    baro_input = float(baro_input[:5])
                    show_baro_input = f'{baro_input:.2f}' #this is a string
                    submit_calibration_town = submit_calibration_town.title()
                    
                    aobs_site = submit_calibration_town
                    
                    instruction_text = f"The barometric pressure at {submit_calibration_town} is {show_baro_input} inches.\nDo you want to keep this as the calibration site,\nchange the site again or,\nenter your own barometric presure?"
                    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), justify="left")
                    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10), sticky="w")
                
                    # Create the 'Keep' button
                    keep_button = create_button(frame1, "Keep", button_font, confirm_calibration_site)
                    keep_button.grid(row=2, column=0, padx=(50,10), pady=5, sticky="w")

                    # Create the 'Change' button
                    change_button = create_button(frame1, "Change", button_font, change_calibration_site)
                    change_button.grid(row=2, column=0, padx=190, pady=5, sticky="w")

                    # Create the 'Enter Your Own' button
                    enter_own_button = create_button(frame1, "Own", button_font, own_calibration_site)
                    enter_own_button.grid(row=2, column=0, padx=355, pady=5, sticky="w")
                
                else:
                    # Clear the current display
                    for widget in frame1.winfo_children():
                        widget.destroy()
                        
                    # Create and display the updated labels
                    label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                    label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")  
                    
                    instruction_text = "Could not match that location with a barometric pressure reading. Please change the site."
                    instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                    instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
                
                    # Create the 'Change' button
                    change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
                    change_button.grid(row=2, column=0, padx=50, pady=5, sticky="w")
                    
            except Exception as e:
                print( "change calibration site:", e)
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()
                    
                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=10, sticky="w")  
                    
                instruction_text = "Something went wrong and that site can't be used. Please change the site."
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(20, 10))
            
                # Create the 'Change' button
                change_button = tk.Button(frame1, text="Change", font=button_font, command=change_calibration_site)
                change_button.grid(row=2, column=0, padx=50, pady=5, sticky="w")
                
                
        def change_calibration_site():
            
                global calibration_town, calibration_state, submit_calibration_town, submit_calibration_state
                
                # Clear the current display
                for widget in frame1.winfo_children():
                    widget.destroy()

                # Create and display the updated labels
                label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
                label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

                instruction_text = "Please enter the name of the town to be used for calibration:"
                instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16,))
                instructions_label.grid(row=1, column=0, padx=50, pady=(5, 5))

                # Create an Entry widget for the user to input the town
                calibration_town = tk.Entry(frame1, font=("Helvetica", 14))
                calibration_town.grid(row=2, column=0, padx=50, pady=(5, 5), sticky="w")

                state_instruction_text = "Please enter the 2-letter state ID for the calibration site:"
                state_instructions_label = tk.Label(frame1, text=state_instruction_text, font=("Helvetica", 16,))
                state_instructions_label.grid(row=3, column=0, padx=0, pady=(5, 5))

                # Suppress the error message by redirecting standard error output to /dev/null
                os.system("onboard 2>/dev/null &")

                # Create an Entry widget for the user to input the state
                calibration_state = tk.Entry(frame1, font=("Helvetica", 14))
                calibration_state.grid(row=4, column=0, padx=50, pady=(5, 5), sticky="w")
                
                # Create a submit button to process the user's input
                submit_button = tk.Button(frame1, text="Submit", command=submit_calibration_input, font=("Helvetica", 16, "bold"))
                submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")
                
                
        def own_calibration_site():
            # Add the action to be performed when 'Enter Your Own' button is clicked
            global baro_input_box
            
                  # Clear the current display
            for widget in frame1.winfo_children():
                widget.destroy()

            # Create and display the updated labels
            label1 = tk.Label(frame1, text="The Weather Observer", font=("Arial", 18, "bold"), justify="left")
            label1.grid(row=0, column=0, padx=50, pady=5, sticky="w")

            instruction_text = "Please enter the current barometric pressurer reading in inches from your own source.\n\nEnter in the form XX.XX"
            instructions_label = tk.Label(frame1, text=instruction_text, font=("Helvetica", 16), justify="left")
            instructions_label.grid(row=1, column=0, padx=(50, 0), pady=(5, 5), sticky="w")

            # Suppress the error message by redirecting standard error output to /dev/null
            os.system("onboard 2>/dev/null &")

            # Create an Entry widget for the user to input the town
            baro_input_box = tk.Entry(frame1, font=("Helvetica", 14), width=5)
            baro_input_box.grid(row=2, column=0, padx=(50, 0), pady=(5, 5), sticky="w")
            
            # Create a label widget for the text to the right of the entry box
            label_text = "inches of mercury"
            label = tk.Label(frame1, text=label_text, font=("Helvetica", 14))
            label.grid(row=2, column=0, padx=120, pady=5, sticky="w")            
            
            # Create a submit button to process the user's input
            submit_button = tk.Button(frame1, text="Submit", command=submit_own_calibration, font=("Helvetica", 16, "bold"))
            submit_button.grid(row=5, column=0, padx=50, pady=(5, 5), sticky="w")
            
        def submit_own_calibration():
            global baro_input

            # Get the user's input
            baro_input = float(baro_input_box.get())

            # check the input
            #print("baro_input from user line 1238: ", baro_input)
         
            # Continue with other actions or functions as needed
            radar_site_question()

        
        frame1 = tk.Frame(root)
        frame1.grid(row=0, column=0)

        # First line (bold)
        label1 = tk.Label(frame1, text="Welcome to The Weather Observer v2.4.2", font=("Arial", 18, "bold"), justify="left")
        label1.grid(row=0, column=0, padx=100, pady=(10, 0), sticky="w")

        # Main block of text including the question
        info_text = f'''
        In order to begin, your new instrument needs to be calibrated,
        and you need to make choices about which weather to observe.

        The nearest NWS Observation site found is:
        {aobs_site}
        
        This site will be used to calibrate the first barometric pressure reading.
        The current barometric pressure reading there is: {baro_input:.2f} inches.

        Do you want to keep the default calibration site,
        change to another site, or
        enter your own barometric pressure?
        '''

        label2 = tk.Label(frame1, text=info_text, font=("Arial", 16), justify="left")
        label2.grid(row=1, column=0, padx=50, pady=(0, 10))

        # Create 'Yes' and 'No' buttons with custom font size (adjust font size as needed)
        button_font = ("Arial", 16, "bold")

        # Define frame_question
        frame_question = tk.Frame(frame1)
        frame_question.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="w")

        # Create the 'Keep' button
        keep_button = create_button(frame_question, "Keep", button_font, confirm_calibration_site)
        keep_button.grid(row=0, column=0, padx=50, pady=5, sticky="w")

        # Create the 'Change' button
        change_button = create_button(frame_question, "Change", button_font, change_calibration_site)
        change_button.grid(row=0, column=1, padx=0, pady=5, sticky="w")

        # Create the 'Enter Your Own' button
        enter_own_button = create_button(frame_question, "Own", button_font, own_calibration_site)
        enter_own_button.grid(row=0, column=2, padx=50, pady=5, sticky="w")

        root.mainloop()

# Finish setting up graphics display parameters
rcParams['figure.figsize'] = 12, 6

# Create a figure for plotting
light_blue = (0.8, 0.9, 1.0)
fig = plt.figure(facecolor=light_blue)
ax = fig.add_subplot(1, 1, 1)
bx = fig.add_subplot(1, 1, 1, label="unique_label")

#shut off Thonny navigation toolbar
#if fig.canvas.toolbar:
    #fig.canvas.toolbar.pack_forget()

plt.axis('off')
ax.axis('off')
bx.axis('off')        

xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    
    global inHg_correction_factor
        
    # Get I2C bus
    bus = smbus.SMBus(1)
    
    # HP203B address, 0x77(118)
    # Send OSR and channel setting command, 0x44(68)
    bus.write_byte(0x77, 0x44 | 0x00)

    time.sleep(0.5)

    # HP203B address, 0x77(118)
    # Read data back from 0x10(16), 6 bytes
    # cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB
    data = bus.read_i2c_block_data(0x77, 0x10, 6)

    # Convert the data to 20-bits
    # Correct for 160 feet above sea level
    # cpressure is pressure corrected for elevation
    cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
    fTemp = (cTemp * 1.8) + 32
    pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
    cpressure = (pressure * 1.0058)
    inHg = (cpressure * .029529)
    
    if i == 0:
        
        ax.axis('off')
        bx.axis('off')        
        
        # calculate a correction factor only when i == 0
        inHg_correction_factor = (baro_input / inHg)

    # apply correct factor to each reading from sensor
    inHg = (inHg * inHg_correction_factor)
        
    # HP203B address, 0x77(118)
    # Send OSR and channel setting command, 0x44(68)
    bus.write_byte(0x77, 0x44 | 0x01)

    time.sleep(0.5)

    # HP203B address, 0x76(118)
    # Read data back from 0x31(49), 3 bytes
    # altitude MSB, altitude CSB, altitude LSB
    data = bus.read_i2c_block_data(0x77, 0x31, 3)

    # Convert the data to 20-bits
    altitude = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
    
    if i > 1:

        # Save the image using plt.savefig()
        plt.savefig('baro_trace.png')

        ax.clear()
        bx.clear()
        
        now = datetime.now() # current date and time
        day = now.strftime("%A")
        hourmin_str = now.strftime("%H:%M")
        
        # Adjust margins
        
        fig.subplots_adjust(left=0.125, right=0.90, bottom=0, top=0.88)
        
        ax.text(0, 1.09, "The",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
    
        ax.text(0, 1.05, "Weather",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
 
        ax.text(0, 1.01, "Observer",
            transform=ax.transAxes,
            fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.11, 1.01, f'Last Updated\n{now.strftime("%A")}\n{now.strftime("%I:%M %P")}', 
            transform=ax.transAxes,
            fontweight='light', fontstyle='italic', horizontalalignment='left', fontsize=6)   
        
        try:
            global atemp, awtemp, awind, ctemp, cwind
            
            if aobs_url.startswith("https://www.ndbc.noaa.gov/"):
                
                try:
                    
                    buoy_code = "Buoy: " + alternative_town_1
                    
                    ax.text(.2, 1.1, str(buoy_code),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)
            
                    ax.text(.2, 1.07, str(atemp),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)

                    ax.text(.2, 1.04, str(awtemp),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)
        
                    ax.text(.2, 1.01, str(awind),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9) 
            
                except Exception as e:
                    print("2nd print of buoy data", e)
                    pass
    
            else:
            
                ax.text(.20, 1.09, alternative_town_1.title(),
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
    
                ax.text(.20, 1.05, atemp,
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
 
                ax.text(.20, 1.01, awind,
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
    
        except Exception as e:
            print( "a obs error:", e)
            pass
    
        try:
            
            global bwtemp, bwind, btemp, bwind, ctemp, cwind
            
            if bobs_url.startswith("https://www.ndbc.noaa.gov/"):
                
                try:
                    
                    bobs_buoy_code = "Buoy: " + alternative_town_2
                    
                    ax.text(.5, 1.1, str(bobs_buoy_code),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)
            
                    ax.text(.5, 1.07, str(btemp),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)

                    ax.text(.5, 1.04, str(bwtemp),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9)
        
                    ax.text(.5, 1.01, str(bwind),
                        transform=ax.transAxes,
                        fontweight='bold', horizontalalignment='left', fontsize=9) 
            
                except Exception as e:
                    print("2nd print of buoy data", e)
                    pass
    
            else:
                                    
                ax.text(.50, 1.09, alternative_town_2.title(),
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
        
                ax.text(.50, 1.05, btemp,
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
     
                ax.text(.50, 1.01, bwind,
                    transform=ax.transAxes,
                    fontweight='bold', horizontalalignment='left', fontsize=12)
    
        except Exception as e:
            print("b land Obs error:", e)
            pass

        try:
            ax.text(.80, 1.09, alternative_town_3.title(),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
            ax.text(.80, 1.05, ctemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)

            ax.text(.80, 1.01, cwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        except Exception as e:
            print("c obs error:", e)
            pass
    
        # Is this a user choice?
        if box_variables[1] == 1: 
        
            # Display the national composite radar image in the subplot
            try:           
                # Scrape and save the US composite radar image
                radar_url = 'https://radar.weather.gov/ridge/standard/CONUS_0.gif'
                radar_response = requests.get(radar_url)
                radar_content = radar_response.content
                radar_image = Image.open(BytesIO(radar_content))
                radar_image.save('radar.png', 'PNG')            
            
                if radar_response.status_code == 200:
                    radar_image = Image.open('radar.png')
                    bx.imshow(radar_image)
                    ax.axis('off')
                    bx.axis('off')
                    plt.draw()
                    plt.pause(7)            
                else:            
                    pass
            except Exception as e:
                print("Scrape, save and Display regional radar", e)
                pass
        
        # Is this a user choice?
        if box_variables[2] == 1:
        
            # Scrape, Save and Display local radar loop in the subplot
            try:
                global radar_identifier
                radar_loop_url = f"https://radar.weather.gov/ridge/standard/{radar_identifier}_loop.gif"

                # Scrape and save the radar GIF
                radar_loop_response = requests.get(radar_loop_url)
                if radar_loop_response.status_code == 200:
                    with open('radar_loop.gif', 'wb') as f:
                        f.write(radar_loop_response.content)

                # Open the radar GIF and extract frames
                radar_loop_image = Image.open('radar_loop.gif')
                radar_frames = []
                try:
                    while True:
                        radar_frames.append(radar_loop_image.copy())
                        radar_loop_image.seek(len(radar_frames))  # Move to the next frame
                except EOFError:
                    pass

                # Display the frames in a loop, cycling 1 time
                num_cycles = 1

                plt.ion()  # Turn on interactive mode

                # Pre-load the frames into memory before starting the loop
                preloaded_frames = [radar_frame.copy() for radar_frame in radar_frames]

                for cycle in range(num_cycles):
                    for radar_frame in preloaded_frames:
                        bx.imshow(radar_frame)
                        ax.axis('off')
                        bx.axis('off')
                        plt.draw()
                        plt.pause(0.01)  # Pause for a short duration between frames

            except Exception as e:
                print("Scrape, Save and Display local radar", e)
                pass
        
        # Is this a user choice?
        if box_variables[3] == 1:
            #Use Selenium to get lightning data
        
            # URL of the website to capture
            lightning_url = (
                "https://www.lightningmaps.org/?lang=en#m=oss;t=1;s=200;o=0;b=0.00;ts=0;d=2;dl=2;dc=0;y=" +
                str(lightning_lat) + ";x=" + str(lightning_lon) + ";z=6;"
            )
            
            try:
            
                # Configure Chrome options for headless mode
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")

                # Use the system-installed ChromeDriver executable
                driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)

                # Navigate to the URL
                driver.get(lightning_url)

            
                # Wait for the "Got it!" button to be clickable
                wait = WebDriverWait(driver, 30)
                got_it_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='cc-btn cc-dismiss']")))

                # Click the "Got it!" button
                got_it_button.click()

                time.sleep(5)

                # Capture a screenshot of the entire page
                lightning_screenshot = driver.get_screenshot_as_png()

                # Close the WebDriver
                driver.quit()

                # Display the screenshot using PIL
                lightning_screenshot_image = Image.open(io.BytesIO(lightning_screenshot))

                lightning_screenshot_crop = lightning_screenshot_image.crop((0, 0, lightning_screenshot_image.width, lightning_screenshot_image.height - 90))
                bx.imshow(lightning_screenshot_crop, aspect='equal')
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(7)
        
            except TimeoutError:
                print("Selenium & Display lightning image: Timeout occurred (30 seconds). Exiting current attempt.")
                pass
            except Exception as e:
                print("Selenium & Display lightning image:", e)
                pass
        # Is this a user choice?
        if box_variables[4] == 1:
            # Scrape, Save and Display the national satellite image in the subplot
            try:
                satellite_url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/CONUS/GEOCOLOR/1250x750.jpg'
                satellite_response = requests.get(satellite_url)
                satellite_content = satellite_response.content
                satellite_image = Image.open(BytesIO(satellite_content))
                satellite_image.save('satellite.png', 'PNG')
            
                if satellite_response.status_code == 200:                        
                    satellite_image = Image.open('satellite.png')
                    bx.imshow(satellite_image, aspect='equal')
                    ax.axis('off')
                    bx.axis('off')
                    plt.draw()
                    plt.pause(7)
                else:
                    pass
            except Exception as e:
                print("Scrape, Save and Display satellite image", e)
                pass
            
        # Is this a user choice?
        if box_variables[5] == 1:
            
            if reg_sat_choice_variables[0] ==1:
                sat_goes = 18
                sat_reg = 'pnw'
                
            if reg_sat_choice_variables[1] ==1:
                sat_goes = 18
                sat_reg = 'psw'
                
            if reg_sat_choice_variables[2] ==1:
                sat_goes = 16
                sat_reg = 'nr'
                
            if reg_sat_choice_variables[3] ==1:
                sat_goes = 16
                sat_reg = 'sr'
                
            if reg_sat_choice_variables[4] ==1:
                sat_goes = 16
                sat_reg = 'umv'
                
            if reg_sat_choice_variables[5] ==1:
                sat_goes = 16
                sat_reg = 'smv'
                
            if reg_sat_choice_variables[6] ==1:
                sat_goes = 16
                sat_reg = 'cgl'
                
            if reg_sat_choice_variables[7] ==1:
                sat_goes = 16
                sat_reg = 'sp'
                
            if reg_sat_choice_variables[8] ==1:
                sat_goes = 16
                sat_reg = 'ne' 
            
            if reg_sat_choice_variables[9] ==1:
                sat_goes = 16
                sat_reg = 'se'
            
            if reg_sat_choice_variables[10] ==1:
                sat_goes = 18
                sat_reg = 'wus' 
            
            if reg_sat_choice_variables[11] ==1:
                sat_goes = 16
                sat_reg = 'eus'
            
            # The URL of the website to scrape for the satellite GIF URL
            reg_sat_url = f"https://www.star.nesdis.noaa.gov/GOES/sector.php?sat=G{sat_goes}&sector={sat_reg}&refresh=true"

            # Send an HTTP GET request to the URL
            reg_sat_response = requests.get(reg_sat_url)

            try:

                # Check if the request was successful (status code 200)
                if reg_sat_response.status_code == 200:
                    # Parse the HTML content of the page
                    reg_sat_soup = BeautifulSoup(reg_sat_response.text, 'html.parser')

                    # Use the CSS selector to find the <a> element
                    a_element = reg_sat_soup.select("#main > div > div:nth-child(8) > div.Links > ul > li:nth-child(7) > a")
                    
                    if reg_sat_choice_variables[10] == 1 or reg_sat_choice_variables[11] == 1:
              
                        a_element = reg_sat_soup.select("#main > div > div:nth-child(8) > div.Links > ul > li:nth-child(8) > a")
                                        
                    # Check if the <a> element was found
                    if a_element:
                        # Extract the "href" attribute (URL)
                        final_reg_sat_url = a_element[0].get('href')

                        # Scrape and save the satellite GIF
                        final_reg_sat_response = requests.get(final_reg_sat_url)
                        if final_reg_sat_response.status_code == 200:
                            with open('final_reg_sat_loop.gif', 'wb') as f:
                                f.write(final_reg_sat_response.content)

                        # Open the satellite GIF and extract frames
                        reg_sat_loop_image = Image.open('final_reg_sat_loop.gif')

                        # Define the number of most recent frames to display
                        num_frames_to_display = 12

                        # Use a deque to efficiently manage frames
                        recent_frames = deque(maxlen=num_frames_to_display)

                        try:
                            while True:
                                frame = reg_sat_loop_image.copy()
                                recent_frames.append(frame)
                                reg_sat_loop_image.seek(reg_sat_loop_image.tell() + 1)
                        except EOFError:
                            pass

                        # Number of cycles to play the loop
                        num_cycles = 1

                        plt.ion()  # Turn on interactive mode

                        for cycle in range(num_cycles):
                            for frame in recent_frames:
                                bx.imshow(frame)
                                ax.axis('off')
                                bx.axis('off')
                                plt.draw()
                                plt.pause(0.01)  # Pause for a short duration between frames

                    else:
                        print("The <a> element with the specified CSS selector was not found on the page.")
                else:
                    print("Failed to retrieve the web page. Status code:", response.status_code)            

            except Exception as e:
                print ("failed to get and/or build reg sat loop", e)

        # Is this a user choice?
        if box_variables[6] == 1:
            # Scrape, Save and Display the national surface analysis in the subplot
            try:           
                sfc_url = 'https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif'
                sfc_response = requests.get(sfc_url)
                sfc_content = sfc_response.content        
                sfc_image = Image.open(BytesIO(sfc_content))
                sfc_image.save('sfc.png', 'PNG')
        
                if sfc_response.status_code == 200:           
                    sfc_image = Image.open('sfc.png')
                    bx.imshow(sfc_image)
                    ax.axis('off')
                    bx.axis('off')
                    plt.draw()
                    plt.pause(7)
                else:
                    pass
            except Exception as e:
                print("Scrape, Save and Display sfc analysis", e)
                pass
        
        # Is this a user choice?
        if box_variables[7] == 1: 
            #Build, take, and display snapshot of local station models
        
            timeout_seconds = 30
        
            try:
            
                global station_model_url, zoom_plot
            
                # URL of the website to capture map of station model
                #station_model_url = "http://www.wrh.noaa.gov/map/?&zoom=9&scroll_zoom=false&center=43.7568782054261,-70.02367715840926&boundaries=false,false,false,false,false,false,false,false,false,false,false&tab=observation&obs=true&obs_type=weather&elements=temp,dew,wind,gust,slp&temp_filter=-80,130&gust_filter=0,150&rh_filter=0,100&elev_filter=-300,14000&precip_filter=0.01,30&obs_popup=false&fontsize=4&obs_density=60&obs_provider=ALL"
            
                base_url = f"http://www.wrh.noaa.gov/map/?&zoom={zoom_plot}&scroll_zoom=false"
                other_params = "&boundaries=false,false,false,false,false,false,false,false,false,false,false&tab=observation&obs=true&obs_type=weather&elements=temp,dew,wind,gust,slp&temp_filter=-80,130&gust_filter=0,150&rh_filter=0,100&elev_filter=-300,14000&precip_filter=0.01,30&obs_popup=false&fontsize=4&obs_density=60&obs_provider=ALL"
            
                lat_lon_params = "&center=" + str(station_plot_lat) + "," + str(station_plot_lon)
                station_model_url = base_url + lat_lon_params + other_params
            
                # Configure Chrome options for headless mode
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
            
                # Set the desired aspect ratio
                desired_aspect_ratio = 1.8  # Width should be 1.8x the height

                # Calculate the browser window size to achieve the desired aspect ratio
                desired_width = 1200  # Adjust this value as needed
                desired_height = int(desired_width / desired_aspect_ratio)

                # Set the browser window size
                chrome_options.add_argument(f"--window-size={desired_width},{desired_height}")
                        
                # Use the system-installed ChromeDriver executable
                driver = webdriver.Chrome(service=Service("chromedriver"), options=chrome_options)

                # Navigate to the URL
                driver.get(station_model_url)

                # Find and wait for the close button to be clickable, then click it
                close_button_locator = (By.CSS_SELECTOR, "a.panel-close")
                wait = WebDriverWait(driver, timeout_seconds)
                wait.until(EC.element_to_be_clickable(close_button_locator)).click()

                time.sleep(10)

                # Capture a screenshot of the entire page
                station_model_screenshot = driver.get_screenshot_as_png()

                # Close the WebDriver
                driver.quit()

                # Display the screenshot using PIL
                station_model_screenshot_image = Image.open(io.BytesIO(station_model_screenshot))
                station_model_screenshot_crop = station_model_screenshot_image.crop((42, 0, station_model_screenshot_image.width, station_model_screenshot_image.height))
                bx.imshow(station_model_screenshot_crop, aspect='equal')
                ax.axis('off')
                bx.axis('off')
                plt.draw()
                plt.pause(10)
        
            except Exception as e:
                print("Selenium Station models on sfc plot", e)
                pass
        
        # Is this a user choice?
        if box_variables[8] == 1:
            # Scrape, Save and Display the GYX sounding in the subplot
            try:
                
                # Get current UTC time and date
                scrape_now = datetime.utcnow()

                if scrape_now.hour >= 1 and scrape_now.hour < 13:
                    # Use 00z for current UTC date
                    date_str = scrape_now.strftime("%y%m%d00")
                    hour_str = "00Z"
                else:
                    # Use 12z for current UTC date
                    hour_str = "12Z"
                    date_str = scrape_now.strftime("%y%m%d12")
                    if scrape_now.hour < 1:
                        # Use previous UTC date for 00z images
                        scrape_now -= timedelta(days=1)
                        date_str = scrape_now.strftime("%y%m%d12")
                    
                month_str = scrape_now.strftime("%b").capitalize()
                day_str = str(scrape_now.day)

                # Construct image URL
                sound_url = f"https://www.spc.noaa.gov/exper/soundings/{date_str}_OBS/{sonde_letter_identifier}.gif"
            
                # Send a GET request to the image URL to get the image content
                sound_response = requests.get(sound_url)

                # Save the image using Pillow
                sound_img = Image.open(BytesIO(sound_response.content))
                
                # Crop the top 50 pixels from the image
                crop_box = (0, 250, sound_img.width, sound_img.height)
                sound_img = sound_img.crop(crop_box)
                
                ax.axis('off')
                bx.axis('off') 
                
                sound_img.save('sound.png', 'PNG')
        
                if sound_response.status_code == 200:
                    
                    sound_img = Image.open('sound.png')
                
                    # Calculate the aspect ratio of the image               
                    sound_img = sound_img.convert('RGBA')
                    aspect_ratio = sound_img.width / sound_img.height

                    # Set the size of the displayed image to 8 inches by 8 inches
                    display_width = 0.83
                    display_height = 1

                    # Calculate the extent of the displayed image
                    display_extent = [0, display_width, 0, display_height / aspect_ratio]

                    # Create a new image with a white background
                    sound_img_with_white_bg = Image.new('RGBA', (int(sound_img.width), int(sound_img.height)), (255, 255, 255, 255))
                    sound_img_with_white_bg.paste(sound_img, (0, 0), sound_img)

                    sound_img_with_white_bg.save('sound_img.png', 'PNG')

                    # Display the image with the adjusted extent
                    #ax.axis('off')
                    #bx.axis('off') 
                    bx.imshow(sound_img_with_white_bg, extent=display_extent)
           
                    # Add the text to the subplot
                    bx.text(0.28, 0.89, f'{sonde_letter_identifier}\n{month_str} {day_str} {hour_str}', ha='left', va='center', fontweight='bold', transform=bx.transAxes)
                    plt.draw()
                    plt.pause(13)
                else:
                    pass
            except Exception as e:
                print("Scrape, Save and Display sounding", e)
                pass
                   
        bx.clear()
        bx.axis('off')
        
        # Set custom margins
        fig.subplots_adjust(left=0.125, right=0.9, bottom=0.11, top=0.88)

    else:
        ax.axis('off')
        bx.axis('off')        
        pass
    
    if ".ndbc." in aobs_url:
        try:
            
            #Scrape for buoy data
            aurl = aobs_url        
            ahtml = requests.get(aurl)# requests instance    
            time.sleep(5)    
            asoup = BeautifulSoup(ahtml.text,'html.parser')   
        
            awd = asoup.find(class_="dataTable").find_all('td')[0]
            awd = awd.string.split()[0]
        
            aws = asoup.find(class_="dataTable").find_all('td')[1]
            aws = float(aws.string) * 1.15078
            aws = round(aws)
            aws = " at {} mph".format(aws)

            awg = asoup.find(class_="dataTable").find_all('td')[2]
            awg = round(float(awg.string) * 1.15078)
            awg = " G{}".format(awg)

            awind = awd + aws + awg
        
            awt = asoup.find(class_="dataTable")
            awt = awt.find_all('td')[10]
            awt = awt.string
        
            if not "-" in awt:
                awtemp = "Water Temp: " + str(round(float(awt.string))) + chr(176)
            
            else:
                awtemp = "Water Temp: -"
                pass
            aat = asoup.find(class_="dataTable")
            aat = aat.find_all('td')[9]
            atemp = "Air Temp: " + str(round(float(aat.string))) + chr(176)
            
        except Exception as e:
            print("Scrape buoy data", e)
            pass
    
    else:
            
        #scrape for land aobs
        a_match = re.search(f'\((.*?)\)', aobs_obs_site)
        a_station = a_match.group(1)
        
        # Define the URL
        a_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(a_station)
        
        # Send a GET request to the URL
        a_response = requests.get(a_station_url)

        # Check if the request was successful
        if a_response.status_code == 200:
            # Parse the JSON response
            a_data = a_response.json()
            
            try:
            
                a_wind_direction = a_data["STATION"][0]["OBSERVATIONS"]["wind_cardinal_direction_set_1d"]
                a_wind_direction = str(a_wind_direction[-1])
                
            except Exception as e:
                print("wind direction station a", e)
                a_wind_direction = "N/A"
            
            try:
                
                a_wind_speed = a_data["STATION"][0]["OBSERVATIONS"]["wind_speed_set_1"]
                a_wind_speed = (a_wind_speed[-1])
                a_wind_speed = str(round(a_wind_speed))
                
            except Exception as e:
                print("wind speed station a", e)
                a_wind_speed = "N/A"
                
            try:
                
                a_wind_gust = a_data["STATION"][0]["OBSERVATIONS"]["wind_gust_set_1"]    
                a_wind_gust = (a_wind_gust[-1])
                
                if a_wind_gust is None or a_wind_gust == "null":
                    a_wind_gust = ""
                        
                else:
                    a_wind_gust = str(round(a_wind_gust))
                    a_wind_gust = "G" + (a_wind_gust)
                
            except Exception as e:
                print("a_wind_gust", e)
                a_wind_gust = ""
                
            awind = a_wind_direction + " at " + a_wind_speed + " mph " + a_wind_gust 
            
            # Extract the last value from "air_temp_set_1"
            atemp = a_data["STATION"][0]["OBSERVATIONS"]["air_temp_set_1"]
            atemp = str(atemp[-1])
            atemp = atemp + chr(176)
            
        else:
            atemp = "N/A"
            awind = "N/A"
   
    #scrape for bobs
    
    if ".ndbc." in bobs_url:
        try:
                        #Scrape for buoy data
            burl = bobs_url        
            bhtml = requests.get(burl)# requests instance    
            time.sleep(5)    
            bsoup = BeautifulSoup(bhtml.text,'html.parser')   
        
            bwd = bsoup.find(class_="dataTable").find_all('td')[0]
            bwd = bwd.string.split()[0]
            
            bws = bsoup.find(class_="dataTable").find_all('td')[1]
            bws = float(bws.string) * 1.15078
            bws = round(bws)
            bws = " at {} mph".format(bws)

            bwg = bsoup.find(class_="dataTable").find_all('td')[2]
            bwg = round(float(bwg.string) * 1.15078)
            bwg = " G{}".format(bwg)

            bwind = bwd + bws + bwg
        
            bwt = bsoup.find(class_="dataTable")
            bwt = bwt.find_all('td')[10]
            bwt = bwt.string
            
            if not "-" in bwt:
                bwtemp = "Water Temp: " + str(round(float(bwt.string))) + chr(176)
            
            else:
                bwtemp = "Water Temp: -"
                pass
            
            bat = bsoup.find(class_="dataTable")
            bat = bat.find_all('td')[9]
            btemp = "Air Temp: " + str(round(float(bat.string))) + chr(176)
            
        except Exception as e:
            print("Scrape buoy data for burl", e)
            pass
    
    else:    
        
        #scrape for land aobs
        b_match = re.search(f'\((.*?)\)', bobs_obs_site)
        b_station = b_match.group(1)
        
        # Define the URL
        b_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(b_station)
        
        # Send a GET request to the URL
        b_response = requests.get(b_station_url)

        # Check if the request was successful
        if b_response.status_code == 200:
            # Parse the JSON response
            b_data = b_response.json()
            
            try:
            
                b_wind_direction = b_data["STATION"][0]["OBSERVATIONS"]["wind_cardinal_direction_set_1d"]
                b_wind_direction = str(b_wind_direction[-1])
                
            except Exception as e:
                print("b_wind_direction", e)
                b_wind_direction = "N/A"
            
            try:
                
                b_wind_speed = b_data["STATION"][0]["OBSERVATIONS"]["wind_speed_set_1"]
                b_wind_speed = (b_wind_speed[-1])
                b_wind_speed = str(round(b_wind_speed))
                
            except Exception as e:
                print("b_wind_speed", e)
                b_wind_speed = "N/A"
                
            try:
                
                b_wind_gust = b_data["STATION"][0]["OBSERVATIONS"]["wind_gust_set_1"]    
                b_wind_gust = (b_wind_gust[-1])
                
                if b_wind_gust is None or b_wind_gust == "null":
                    b_wind_gust = ""
                        
                else:
                    b_wind_gust = str(round(b_wind_gust))
                    b_wind_gust = "G" + (b_wind_gust)
                
            except Exception as e:
                print("b_wind_gust", e)
                b_wind_gust = ""
                
            bwind = b_wind_direction + " at " + b_wind_speed + " mph " + b_wind_gust 
            
            # Extract the last value from "air_temp_set_1"
            btemp = b_data["STATION"][0]["OBSERVATIONS"]["air_temp_set_1"]
            btemp = str(btemp[-1])
            btemp = btemp + chr(176)
            
        else:
            btemp = "N/A"
            bwind = "N/A"
            
    # scrape for cobs
  
    c_match = re.search(f'\((.*?)\)', cobs_obs_site)
    c_station = c_match.group(1)
    
    # Define the URL
    c_station_url = "https://api.mesowest.net/v2/stations/timeseries?STID={}&showemptystations=1&units=temp|F,speed|mph,english&recent=240&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local".format(c_station)
    
    # Send a GET request to the URL
    c_response = requests.get(c_station_url)

    # Check if the request was successful
    if c_response.status_code == 200:
        # Parse the JSON response
        c_data = c_response.json()
        
        try:
        
            c_wind_direction = c_data["STATION"][0]["OBSERVATIONS"]["wind_cardinal_direction_set_1d"]
            c_wind_direction = str(c_wind_direction[-1])
            
        except Exception as e:
            print("c_wind_direction", e)
            
            c_wind_direction = "N/A"
        
        try:
            
            c_wind_speed = c_data["STATION"][0]["OBSERVATIONS"]["wind_speed_set_1"]
            c_wind_speed = (c_wind_speed[-1])
            c_wind_speed = str(round(c_wind_speed))
            
        except Exception as e:
            print("c_wind_speed", e)
            c_wind_speed = "N/A"
            
        try:
            
            c_wind_gust = c_data["STATION"][0]["OBSERVATIONS"]["wind_gust_set_1"]    
            c_wind_gust = (c_wind_gust[-1])
            
            if c_wind_gust is None or c_wind_gust == "null":
                c_wind_gust = ""
                    
            else:
                c_wind_gust = str(round(c_wind_gust))
                c_wind_gust = "G" + (c_wind_gust)
            
        except Exception as e:
            print("c_wind_gust", e)
            c_wind_gust = ""
            
        cwind = c_wind_direction + " at " + c_wind_speed + " mph " + c_wind_gust 
        
        # Extract the last value from "air_temp_set_1"
        ctemp = c_data["STATION"][0]["OBSERVATIONS"]["air_temp_set_1"]
        ctemp = str(ctemp[-1])
        ctemp = ctemp + chr(176)
        
    else:
        ctemp = "N/A"
        cwind = "N/A"
          
    # Get time stamp
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_str = now.strftime("%H:%M:%S")
    hourmin_str = now.strftime("%H:%M")
    hms = now.strftime("%H:%M:%S")
    day = now.strftime("%A")
           
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time = pd.to_datetime(date_time) #allows us to label x-axis

    now = datetime.now() # current date and time
    time_delta = dt.timedelta(minutes=4200)
    start_time = now - time_delta

    #sec = now.strftime("%S")
    
    # Set axis limits and labels
    ax.set_xlim(start_time, now)
    
    dtext=date_time
    #Build xs and ys arrays
       
    xs.append(date_time)
    ys.append(inHg)
    
    xs = xs[-4200:]
    ys = ys[-4200:]
    
    ax.clear()
    ax.plot(xs, ys, 'r-')

    ax.text(0, 1.09, "The",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
    
    ax.text(0, 1.05, "Weather",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
 
    ax.text(0, 1.01, "Observer",
        transform=ax.transAxes,
        fontweight='bold', horizontalalignment='left', fontsize=12)
    
    ax.text(.11, 1.01, f'Last Updated\n{now.strftime("%A")}\n{now.strftime("%I:%M %P")}', 
        transform=ax.transAxes,
        fontweight='light', fontstyle='italic', horizontalalignment='left', fontsize=7)  
    
    if ".ndbc." in aobs_url:
        try:
            
            buoy_code = "Buoy: " + alternative_town_1
                    
            ax.text(.2, 1.1, str(buoy_code),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)
            
            ax.text(.2, 1.07, str(atemp),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)

            ax.text(.2, 1.04, str(awtemp),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)
        
            ax.text(.2, 1.01, str(awind),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9) 
            
        except Exception as e:
            print("2nd print of buoy data", e)
            pass
    
    else:
                
        try:
            ax.text(.20, 1.09, alternative_town_1.title(),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
    
            ax.text(.20, 1.05, atemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
 
            ax.text(.20, 1.01, awind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
    
        except Exception as e:
            print("2nd aobs error:", e)
            pass

    if ".ndbc." in bobs_url:
        try:
            
            bobs_buoy_code = "Buoy: " + alternative_town_2
                    
            ax.text(.5, 1.1, str(bobs_buoy_code),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)
            
            ax.text(.5, 1.07, str(btemp),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)

            ax.text(.5, 1.04, str(bwtemp),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9)
        
            ax.text(.5, 1.01, str(bwind),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=9) 
            
        except Exception as e:
            print("2nd print of buoy data", e)
            pass

    else:

        try:
            
            ax.text(.50, 1.09, alternative_town_2.title(),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
            ax.text(.50, 1.05, btemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
     
            ax.text(.50, 1.01, bwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
            
        except Exception as e:
            print("2nd bobs error:", e)
            pass

    try:
        ax.text(.80, 1.09, alternative_town_3.title(),
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.80, 1.05, ctemp,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
        ax.text(.80, 1.01, cwind,
                transform=ax.transAxes,
                fontweight='bold', horizontalalignment='left', fontsize=12)
        
    except Exception as e:
        print("2nd cobs error:", e)
        pass
 
    gold = 30.75
    yellow = 30.35
    gainsboro = 29.65
    darkgrey = 29.25
        
    ax.axhline(gold, color='gold', lw=77, alpha=.5)
    ax.axhline(yellow, color='yellow', lw=46, alpha=.2)
    #ax.axhline(white, color='white', lw=40, alpha=.2)
    ax.axhline(gainsboro, color='gainsboro', lw=46, alpha=.5)    
    ax.axhline(darkgrey, color='darkgrey', lw=77, alpha=.5)
    
    #Lines on minor ticks
    for t in np.arange(29, 31, 0.05):
        ax.axhline(t, color='black', lw=.5, alpha=.2)
    for u in np.arange(29, 31, 0.25):
        ax.axhline(u, color='black', lw=.7)
        
    ax.tick_params(axis='x', direction='inout', length=5, width=1, color='black')
    
    ax.set_ylim(29, 31)
    
    ax.plot(xs, ys, 'r-')
    plt.grid(True, color='.01',) #Draws default horiz and vert grid lines
    plt.ylabel("Inches of Mercury")
    #plt.title("Barometric Pressure")
      
    ax.yaxis.set_minor_locator(AutoMinorLocator(5)) #Puts small ticks between labeled ticks
    ax.yaxis.set_major_formatter(FormatStrFormatter('%2.2f'))
    # disable removing overlapping locations
    ax.xaxis.remove_overlapping_locs = False
    print(i)
    
    ax.xaxis.set(
    major_locator=mdates.HourLocator((0,4,8,12,16,20)),
    major_formatter=mdates.DateFormatter('%-I%P'),
    minor_locator=mdates.DayLocator(),
    minor_formatter=mdates.DateFormatter("\n%a,%-m/%-d"),
)
    ax.set_xlim(dt.datetime.now() - dt.timedelta(minutes=4200), dt.datetime.now())
    #this line seems responsible for vertical lines
    ax.grid(which='major', axis='both', linestyle='-', linewidth=1, color='black', alpha=1, zorder=10)
    plt.show(block=False)
    
    #command to close Onboard keyboard
    os.system("pkill onboard") 
    
try:
    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=3000, save_count=len(xs))
    #ani.save('animation.gif', writer='pillow')
    # the above line was from the effort to get images to a web site automatically
    #I had to get rid of this line to get it to work without thonny...I don't know why
    plt.show()
except AttributeError:
    pass
except IndexError:
    pass    

