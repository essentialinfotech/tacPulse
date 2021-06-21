function initMap() {
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,

        center: { lat: 23.78182997116147, lng: 90.4199998114322 },
    });
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    document.getElementById("mode").addEventListener("change", () => {
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
}


function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    const selectedMode = document.getElementById("mode").value;
    parent1 = { lat: 23.873916564432367, lng: 90.37966995812839 }
    parent2 = { lat: 23.737317969186893, lng: 90.38705757174523 }
    directionsService.route({
            origin: parent1,
            destination: parent2,
            travelMode: google.maps.TravelMode[selectedMode],
        },
        (response, status) => {
            if (status == "OK") {
                directionsRenderer.setDirections(response);

            } else {
                window.alert("Directions request failed due to " + status);
            }
        }
    );

    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix({
        origins: [parent1],
        destinations: [parent2],
        travelMode: google.maps.TravelMode[selectedMode],
        unitSystem: google.maps.UnitSystem.METRIC,
        avoidHighways: false,
        avoidTolls: false
    }, function(response, status) {
        var step = parseFloat(response.rows[0].elements[0].distance.text) / 2;
        if (status == google.maps.DistanceMatrixStatus.OK && response.rows[0].elements[0].status != "ZERO_RESULTS") {
            var distance = response.rows[0].elements[0].distance.text;
            var duration = response.rows[0].elements[0].duration.text;

            x = 'Distance: ' + distance + "<br>" + ' Predicted Time: ' + duration + " "
            $('#dis_dur').append(x)
        } else {
            alert("Unable to find the distance via road.");
        }
    });
}