function trackMap() {
    alert('ok')
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
    lat = parseFloat(document.getElementById('latitude').value)
    long = parseFloat(document.getElementById('longitude').value)
    from_lat = parseFloat(document.getElementById('from_lat').value)
    from_long = parseFloat(document.getElementById('from_long').value)
        // crnt_lat = parseFloat(document.getElementById('crnt_lat').value)
        // crnt_lng = parseFloat(document.getElementById('crnt_lng').value)
    parent1 = { lat: lat, lng: long }
    parent2 = { lat: from_lat, lng: from_long }
    directionsService.route({
            origin: parent1,
            destination: parent2,
            travelMode: google.maps.TravelMode[selectedMode],
        },
        (response, status) => {
            if (status == "OK") {
                directionsRenderer.setDirections(response);

            } else {
                calculateAndDisplayRoute(directionsService, directionsRenderer)
                    // window.alert("Directions request failed due to " + status);
            }
        }
    );

    var service = new google.maps.DistanceMatrixService();
    service.getDistanceMatrix({
        origins: [parent2],
        destinations: [parent1],
        travelMode: google.maps.TravelMode[selectedMode],
        unitSystem: google.maps.UnitSystem.METRIC,
        avoidHighways: false,
        avoidTolls: false
    }, function(response, status) {
        var step = parseFloat(response.rows[0].elements[0].distance.text) / 2;
        if (status == google.maps.DistanceMatrixStatus.OK && response.rows[0].elements[0].status != "ZERO_RESULTS") {
            var distance = response.rows[0].elements[0].distance.text;
            var duration = response.rows[0].elements[0].duration.text;
            $('#dis_dur').empty();
            x = 'Distance: <u>' + distance + "</u><br>" + ' Predicted Time: <u>' + duration + "</u> "
            $('#dis_dur').append(x)
        } else {
            alert("Unable to find the distance via road.");
        }
    });
}