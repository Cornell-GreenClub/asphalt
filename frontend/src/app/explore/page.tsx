'use client';
import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import PlacesAutocomplete from './PlacesAutocomplete';
import Footer from '../components/Footer';
import Navbar from '../components/Navbar';

// Dynamically import the map component with no Server-Side Rendering
const MapView = dynamic(() => import('./MapView'), {
  ssr: false,
  loading: () => (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-50">
      <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
    </div>
  ),
});

// Add preset route data
const presetRoute = {
  stops: [
    {
      location: 'TST BOCES, 555 Warren Road, Northeast Ithaca, NY 14850',
      coords: { lat: 42.4808, lng: -76.457 },
    },
    {
      location: 'Dewitt Middle School, 560 Warren Road, Ithaca, NY 14850',
      coords: { lat: 42.4803, lng: -76.4566 },
    },
    {
      location:
        'Northeast Elementary School, 425 Winthrop Dr, Ithaca, NY 14850',
      coords: { lat: 42.4775, lng: -76.4647 },
    },
    {
      location:
        'Cayuga Heights Elementary School, 110 E Upland Rd, Ithaca, NY 14850',
      coords: { lat: 42.4697, lng: -76.4791 },
    },
    {
      location:
        'Belle Sherman Elementary School, Valley Road, Ithaca, NY 14853',
      coords: { lat: 42.4478, lng: -76.4766 },
    },
    {
      location:
        'Caroline Elementary School, Slaterville Road, Besemer, NY 14881',
      coords: { lat: 42.3839, lng: -76.4165 },
    },
    {
      location:
        'South Hill Elementary School, 520 Hudson Street, Ithaca, NY 14850',
      coords: { lat: 42.4336, lng: -76.495 },
    },
    {
      location:
        'Beverly J. Martin Elementary School, 302 West Buffalo Street, Ithaca, NY',
      coords: { lat: 42.4422, lng: -76.4976 },
    },
    {
      location: 'Fall Creek School, Linn Street, Ithaca, NY 14850',
      coords: { lat: 42.4527, lng: -76.4869 },
    },
    {
      location:
        'Boynton Middle School, 1601 North Cayuga Street, Ithaca, NY 14850',
      coords: { lat: 42.4624, lng: -76.4921 },
    },
    {
      location: '602 Hancock Street, Ithaca, NY 14850',
      coords: { lat: 42.4808, lng: -76.457 },
    },
    {
      location: '737 Willow Ave, Ithaca, NY 14850',
      coords: { lat: 42.4445, lng: -76.5097 },
    },
    {
      location: 'Enfield School, 20 Enfield Main Road, Ithaca, NY 14850',
      coords: { lat: 42.4436, lng: -76.5491 },
    },
    {
      location:
        'Lehmann Alternative Community School, 111 Chestnut Street, Ithaca, NY',
      coords: { lat: 42.4506, lng: -76.515 },
    },
    {
      location:
        'Recycling and Solid Waste Center, 160 Commercial Avenue, Ithaca, NY',
      coords: { lat: 42.4461, lng: -76.5138 },
    },
  ],
  maintainOrder: true,
  currentFuel: 'Full',
  time: '8h 00m',
  vehicleNumber: 'BUS-001',
};


/**
 * 
 * Renders the explore page, handlilng changes to input. Enables MapView when a route is submitted. 
 * 
 */
const ExplorePage = () => {

  /*=======================================================
  
    INTERFACES
  
  =========================================================*/

  // define a coordinates interface for standardization
  interface Coords {
    lat: number;
    lng: number;
  }

  // define an interface that defines a place
  interface Place {
    formatted_address: string;
    geometry: {
      location: {
        lat: number;
        lng: number;
      };
    };
  }

  //define an interface for a stop
  interface Stop {
    location: string;
    coords: Coords | null;
  }

  /*=======================================================
  
    STATES
  
  =========================================================*/


  // define a stateful variable formdata holding necessary data to display
  const [formData, setFormData] = useState({
    stops: [
      { location: '', coords: null as Coords | null }, // Start
      { location: '', coords: null as Coords | null }, // End
    ],
    maintainOrder: false,
    currentFuel: '',
    time: '',
    vehicleNumber: '',
  });

  //debug whenever formData.stops updates
  useEffect(() => {
    console.log("Updated stops:", formData.stops);
  }, [formData.stops]); // Runs whenever `stops` changes

  // define stateful variables for the route, and the current view
  const [route, setRoute] = useState(null);
  const [isMapView, setIsMapView] = useState(false);
  const [dropdownVisible, setDropdownVisible] = useState(Array(formData.stops.length).fill(false));

  // Add these computed values
  const startCoords = formData.stops[0]?.coords || null;
  const endCoords = formData.stops[formData.stops.length - 1]?.coords || null;

  // look at later
  interface Place {
    formatted_address: string;
    geometry: {
      location: {
        lat: number;
        lng: number;
      };
    };
  }

  // handle a change to the selection of stops
  const handleStopSelect = (place: Place, index: number) => {
    const newStops = [...formData.stops];
    newStops[index] = {
      location: place.formatted_address,
      coords: place.geometry.location,
    };
    setFormData((prev) => ({ ...prev, stops: newStops }));
  };

  // handle adding a stop
  const addStop = () => {
    setFormData((prev) => ({
      ...prev,
      stops: [
        ...prev.stops.slice(0, -1),
        { location: '', coords: null },
        prev.stops[prev.stops.length - 1],
      ],
    }));
  };

  //handle removing a stop
  const removeStop = (index: number) => {
    if (formData.stops.length <= 2) return; // Keep at least start and end
    setFormData((prev) => ({
      ...prev,
      stops: prev.stops.filter((_, i) => i !== index),
    }));
  };

  // handle a change to the form input
  const handleInputChange = (e: any) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  // look at later
  interface Stop {
    location: string;
    coords: Coords | null;
  }

  // given a list of stops, make an API call to osrm that returns route data that is then formatted
  const getMultiStopRoute = async (stops: Stop[]) => {
    try {
      const coordinates = stops
        .map((stop) =>
          stop.coords ? `${stop.coords.lng},${stop.coords.lat}` : ''
        )
        .join(';');

      const response = await fetch(
        `https://router.project-osrm.org/route/v1/driving/${coordinates}?overview=full&geometries=geojson`
      );
      const data = await response.json();
      if (data.routes && data.routes.length > 0) {
        return data.routes[0].geometry.coordinates.map((coord: any) => [
          coord[1],
          coord[0],
        ]);
      }
      return null;
    } catch (error) {
      console.error('Error getting route:', error);
      return null;
    }
  };

  // Reusable route generation logic, calling the backend
  const generateRouteFromStops = async (stops: any[]) => {
    try {
      // Call the Flask backend to reorder stops
      const response = await fetch('http://localhost:5000/reorder_stops', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stops }),
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("Error reordering stops:", data);
        return;
      }

      // Update the form data with reordered stops
      setFormData((prev) => ({
        ...prev,
        stops: data.stops,
      }));

      // Get route and update map
      const routeData = await getMultiStopRoute(data.stops);
      setRoute(routeData);
      setIsMapView(true);
    } catch (error) {
      console.error("Error calling backend:", error);
    }
  };

  // Form submission handler
  const handleSubmit = async (e: any) => {
    e.preventDefault();
    await generateRouteFromStops(formData.stops);
  };

  // Preset route loader
  const loadPresetRoute = async () => {
    setFormData(presetRoute);
    await generateRouteFromStops(presetRoute.stops);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-50 flex flex-col">
      {/* Only show Navbar if not in MapView */}
      {!isMapView && <Navbar />}
      <div className="mt-16" />
      <div className="relative flex-1 flex flex-col justify-center items-center">
        {/* Decorative Leaves */}
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', left: '5rem', top: '5vh', width: '6rem', transform: 'rotate(-26deg) scaleX(-1)', zIndex: 0 }} className="hidden md:block" />
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', left: '5rem', top: '30vh', width: '5rem', transform: 'rotate(14deg)', zIndex: 0 }} className="hidden md:block" />
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', left: '5rem', top: '55vh', width: '6rem', transform: 'rotate(-21deg) scaleX(-1)', zIndex: 0 }} className="hidden md:block" />
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', right: '5rem', top: '10vh', width: '6rem', transform: 'rotate(24deg)', zIndex: 0 }} className="hidden md:block" />
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', right: '5rem', top: '35vh', width: '5rem', transform: 'rotate(-16deg) scaleX(-1)', zIndex: 0 }} className="hidden md:block" />
        <img src="/images/leaf.png" alt="Leaf" style={{ position: 'absolute', right: '5rem', top: '60vh', width: '6rem', transform: 'rotate(19deg)', zIndex: 0 }} className="hidden md:block" />
        {/* Main Content */}
        <div className="relative z-10 flex flex-col items-center justify-center w-full py-8 pb-24">
          {!isMapView ? (
            <div className="w-full max-w-4xl mx-auto flex flex-col items-center px-2 sm:px-4 md:px-8">
              <h1 className="text-[52px] poppins-bold text-center leading-tight mb-10 text-gray-900 animate-fade-in-down">
                <span className="asphalt-green">Explore</span> <span className="text-black">Your New Route to</span><br />
                <span className="asphalt-green mt-2 inline-block">Sustainability</span>
              </h1>
              <form onSubmit={handleSubmit} className="w-full flex flex-col items-center gap-8">
                {/* Stops Section */}
                <div className="w-full flex flex-col gap-4 relative overflow-visible" style={{minHeight: 60 * formData.stops.length}}>
                  {formData.stops.map((stop, index) => (
                    <div key={index} className="flex items-center gap-2 w-full min-h-14 sm:min-h-16">
                      <div className="flex-grow relative">
                        {/* Timeline inside and between textboxes */}
                        <div className="absolute left-5 top-0 h-full w-8 flex flex-col items-center z-10 pointer-events-none">
                          {/* Vertical line above the circle (not for first) */}
                          {index !== 0 && (
                            <div
                              className="absolute"
                              style={{
                                left: '50%',
                                transform: 'translateX(-50%)',
                                top: '-22px',
                                height: 'calc(50% + 10px)',
                                width: '2px',
                                background: '#034626',
                                borderRadius: 2
                              }}
                            />
                          )}
                          {/* Circle */}
                          <div
                            className={
                              stop.coords
                                ? 'w-4 h-4 rounded-full'
                                : 'w-4 h-4 rounded-full border-2 bg-white'
                            }
                            style={{
                              zIndex: 2,
                              left: '50%',
                              transform: 'translateX(-50%)',
                              position: 'absolute',
                              top: '50%',
                              marginTop: '-8px',
                              background: stop.coords ? '#034626' : 'white',
                              borderColor: !stop.coords ? '#034626' : undefined,
                            }}
                          ></div>
                          {/* Vertical line below the circle (not for last) */}
                          {index !== formData.stops.length - 1 && (
                            <div
                              className="absolute"
                              style={{
                                left: '50%',
                                transform: 'translateX(-50%)',
                                top: 'calc(50% + 14px)',
                                height: 'calc(50% + 10px)',
                                width: '2px',
                                background: '#034626',
                                borderRadius: 2
                              }}
                            />
                          )}
                        </div>
                        <PlacesAutocomplete
                          value={stop.location}
                          onChange={(value) => {
                            const newStops = [...formData.stops];
                            newStops[index].location = value;
                            newStops[index].coords = null;
                            setFormData((prev) => ({ ...prev, stops: newStops }));
                          }}
                          onSelect={(place) => handleStopSelect(place, index)}
                          inputClassName="text-black text-base sm:text-lg md:text-xl pl-16 py-4"
                          placeholder={
                            index === 0
                              ? 'Enter start location'
                              : index === formData.stops.length - 1
                                ? 'Enter end location'
                                : `Stop ${index}`
                          }
                          onDropdownVisibilityChange={(visible) => {
                            setDropdownVisible((prev) => {
                              const arr = [...prev];
                              arr[index] = visible;
                              return arr;
                            });
                          }}
                        />
                      </div>
                      {/* Remove button for intermediate stops */}
                      {index !== 0 && index !== formData.stops.length - 1 && (
                        <button
                          type="button"
                          onClick={() => removeStop(index)}
                          className="ml-2 text-gray-400 hover:text-red-500 text-2xl font-bold focus:outline-none min-w-[32px] min-h-[32px] flex items-center justify-center"
                          aria-label="Remove stop"
                        >
                          ×
                        </button>
                      )}
                    </div>
                  ))}
                </div>
                <div className="flex flex-col sm:flex-row gap-3 -mt-1 w-full">
                  <button
                    type="button"
                    onClick={addStop}
                    className="bg-[#034626] hover:bg-[#023219] text-white poppins-semibold text-xl py-1.5 px-4 rounded-xl transform transition-all hover:scale-105 w-full sm:w-auto"
                  >
                    + Add stop
                  </button>
                  <button
                    type="button"
                    onClick={loadPresetRoute}
                    className="border-2 border-[#034626] asphalt-green poppins-semibold text-xl py-1.5 px-4 rounded-xl transform transition-all hover:scale-105 w-full sm:w-auto"
                  >
                    Load sample schools route
                  </button>
                </div>
                <div className="flex items-center w-full -mt-4 mb-4">
                  <input
                    id="maintainOrder"
                    type="checkbox"
                    name="maintainOrder"
                    checked={formData.maintainOrder}
                    onChange={handleInputChange}
                    className="mr-2 w-4 h-4 accent-[#034626] border-[#034626] rounded focus:ring-2 focus:ring-[#034626] transition-transform duration-150 hover:scale-110 focus:scale-110 cursor-pointer"
                  />
                  <label htmlFor="maintainOrder" className="text-gray-600 text-base text-[16px] cursor-pointer">
                    The stops are in the order they are currently operating
                  </label>
                </div>
                <div className="w-full flex flex-col gap-2 mt-10">
                  <h3 className="text-4xl text-center mb-2 text-gray-800 poppins-bold">
                    Tell Us About Your <span className="asphalt-green">Vehicle</span>
                  </h3>
                  <div className="grid grid-cols-3 gap-4 w-full mt-2">
                    <div className="flex flex-col">
                      <label className="block text-[18px] font-normal text-gray-800 mb-1">Current Fuel Per Trip</label>
                      <input
                        type="text"
                        name="currentFuel"
                        value={formData.currentFuel}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-[#034626] text-gray-700 placeholder-gray-600 text-[18px] poppins-regular"
                        placeholder="gal"
                      />
                    </div>
                    <div className="flex flex-col">
                      <label className="block text-[18px] font-normal text-gray-800 mb-1">Trip Duration</label>
                      <input
                        type="text"
                        name="time"
                        value={formData.time}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-[#034626] text-gray-700 placeholder-gray-600 text-[18px] poppins-regular"
                        placeholder="hh:mm"
                      />
                    </div>
                    <div className="flex flex-col">
                      <label className="block text-[18px] font-normal text-gray-800 mb-1">User Input</label>
                      <input
                        type="text"
                        name="vehicleNumber"
                        value={formData.vehicleNumber}
                        onChange={handleInputChange}
                        className="w-full px-4 py-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-[#034626] text-gray-700 placeholder-gray-600 text-[18px] poppins-regular"
                        placeholder=""
                      />
                    </div>
                  </div>
                </div>
                <button
                  type="submit"
                  className="w-full bg-[#034626] hover:bg-[#023219] text-white poppins-semibold text-xl py-2 px-4 rounded-xl transform transition-all hover:scale-105 -mt-1"
                >
                  Optimize Route
                </button>
              </form>
            </div>
          ) : (
            <MapView
              formData={formData}
              route={route}
              startCoords={startCoords}
              endCoords={endCoords}
              onBack={() => setIsMapView(false)}
            />
          )}
        </div>
      </div>
      <div className="mt-32">
        <Footer />
      </div>
    </main>
  );
};

export default ExplorePage;
