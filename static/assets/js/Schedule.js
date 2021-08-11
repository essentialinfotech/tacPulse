function my_suggetion() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: { lat: 23.78182997116147, lng: 90.4199998114322 },
    });
    directionsRenderer.setMap(map);
    const input = document.getElementById("from_loc");
    const input2 = document.getElementById("location")
    const options = {
        // componentRestrictions: { country: "us" },
        fields: ["formatted_address", "geometry", "name"],
        origin: map.getCenter(),
        strictBounds: false,
        types: ["establishment"],
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    const autocomplete2 = new google.maps.places.Autocomplete(input2, options);
    autocomplete.bindTo("bounds", map);
    autocomplete2.bindTo("bounds", map);
    const onChangeHandler = function() {
        calculateAndDisplayRoute(directionsService, directionsRenderer, map);
    };
    document.getElementById("from_loc").addEventListener("change", onChangeHandler);
    document.getElementById("location").addEventListener("change", onChangeHandler);

}

function calculateAndDisplayRoute(directionsService, directionsRenderer, map) {
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
        .catch((e) => swal("Directions request failed due to no route" + status));
}