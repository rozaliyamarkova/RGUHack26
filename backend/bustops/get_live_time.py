import requests
import time
import xml.etree.ElementTree as ET
from datetime import datetime


def fetch_from_traveline_api(stop_id,bus_api_username="",bus_api_password=""):
    """
    Fetch bus departure information from the Traveline NextBuses API
    for a specific stop.
    
    Args:
        stop_id (str): The NaPTAN stop identifier
        
    Returns:
        list: List of dictionaries containing bus departure information
    """

    username = bus_api_username
    password = bus_api_password
    
    # Current timestamp in the format expected by the API
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Prepare SIRI-SM request XML
    xml_request = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <Siri version="1.0" xmlns="http://www.siri.org.uk/">
      <ServiceRequest>
        <RequestTimestamp>{current_time}</RequestTimestamp>
        <RequestorRef>{username}</RequestorRef>
        <StopMonitoringRequest version="1.0">
          <RequestTimestamp>{current_time}</RequestTimestamp>
          <MessageIdentifier>{int(time.time())}</MessageIdentifier>
          <MonitoringRef>{stop_id}</MonitoringRef>
        </StopMonitoringRequest>
      </ServiceRequest>
    </Siri>"""
    
    try:
        response = requests.post(
            f"http://{username}:{password}@nextbus.mxdata.co.uk/nextbuses/1.0/1",
            data=xml_request,
            headers={'Content-Type': 'application/xml'},
            timeout=10
        )

        response.raise_for_status()

        
        # Parse the XML response
        return parse_bus_response(response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Traveline API: {e}")
        return []

def parse_bus_response(xml_string):
    """
    Parse the SIRI-SM XML response from the Traveline API
    
    Args:
        xml_string (str): The XML response string
        
    Returns:
        list: List of dictionaries containing bus departure information
    """
    departures = []
    
    try:
        # Parse XML
        root = ET.fromstring(xml_string)
        namespace = {'siri': 'http://www.siri.org.uk/'}
        
        # Find all stop visits
        for visit in root.findall('.//siri:MonitoredStopVisit', namespace):
            try:
                journey = visit.find('.//siri:MonitoredVehicleJourney', namespace)
                
                # Extract bus line number
                line = journey.find('.//siri:PublishedLineName', namespace).text
                
                # Extract direction
                direction_element = journey.find('.//siri:DirectionName', namespace)
                direction = direction_element.text if direction_element is not None else "Unknown"
                
                # Extract operator (if available)
                operator_element = journey.find('.//siri:OperatorRef', namespace)
                operator = operator_element.text if operator_element is not None else None
                
                # Extract departure times
                call = journey.find('.//siri:MonitoredCall', namespace)
                aimed_time_element = call.find('.//siri:AimedDepartureTime', namespace)
                expected_time_element = call.find('.//siri:ExpectedDepartureTime', namespace)
                
                # Check if elements exist before accessing text
                if aimed_time_element is not None:
                    aimed_time = aimed_time_element.text
                else:
                    continue  # Skip this entry if no time is available
                
                # Check if real-time data is available
                is_realtime = expected_time_element is not None
                departure_time = expected_time_element.text if is_realtime else aimed_time
                
                departures.append({
                    'line': line,
                    'direction': direction,
                    'operator': operator,
                    'scheduled_time': aimed_time,
                    'departure_time': departure_time,
                    'is_realtime': is_realtime
                })
            except Exception as e:
                print(f"Error parsing individual bus visit: {e}")
                continue
        
        # Sort by departure time
        departures.sort(key=lambda x: x['departure_time'])
        
    except Exception as e:
        print(f"Error parsing bus data XML: {e}")
    
    return departures