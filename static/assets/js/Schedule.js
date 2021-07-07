﻿function DrirectionalMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: { lat: 41.85, lng: -87.65 },
    });
    directionsRenderer.setMap(map);

    const onChangeHandler = function() {
        calculateAndDisplayRoute(directionsService, directionsRenderer, map);
    };
    document.getElementById("from_loc").addEventListener("change", onChangeHandler);
    document.getElementById("location").addEventListener("change", onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer, map) {
    const geocoder = new google.maps.Geocoder();
    const infowindow = new google.maps.InfoWindow();
    alert(document.getElementById("from_loc").value)
    directionsService
        .route({
            origin: {
                query: document.getElementById("from_loc").value,
            },
            destination: {
                query: document.getElementById("location").value,
            },
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
            directionsRenderer.setDirections(response);
            // x = response.geocoded_waypoints[0].place_id

            document.getElementById('from_lat').value = response.routes[0].legs[0].start_location.lat()
            document.getElementById('from_long').value = response.routes[0].legs[0].start_location.lng()

            document.getElementById('latitude').value = response.routes[0].legs[0].end_location.lat()
            document.getElementById('longitude').value = response.routes[0].legs[0].end_location.lng()

            document.getElementById('distance').value = response.routes[0].legs[0].distance.text
            document.getElementById('duration').value = response.routes[0].legs[0].duration.text

        })
        // .catch((e) => window.alert("Directions request failed due to " + status));
}