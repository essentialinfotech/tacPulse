function getDetails() {

    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,

        center: { lat: 23.78182997116147, lng: 90.4199998114322 },
    });
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}


function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    var from_lat = parseFloat(document.getElementById('from_lat').value);
    var from_long = parseFloat(document.getElementById('from_long').value);
    var latitude = parseFloat(document.getElementById('latitude').value);
    var longitude = parseFloat(document.getElementById('longitude').value);

    parent1 = { lat: from_lat, lng: from_long }
    parent2 = { lat: latitude, lng: longitude }
    directionsService.route({
            origin: parent1,
            destination: parent2,
            travelMode: google.maps.TravelMode.DRIVING,
        },
        (response, status) => {
            if (status == "OK") {
                directionsRenderer.setDirections(response);

            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );


}