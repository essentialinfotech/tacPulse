
data_lat = parseFloat(document.getElementById('lat').value);
data_lng = parseFloat(document.getElementById('lng').value);

function initMap() {
    const geocoder = new google.maps.Geocoder();
    const service = new google.maps.DistanceMatrixService();
    // my location to panic sender distance duration
    navigator.geolocation.getCurrentPosition((position) => {
        var mylat = position.coords.latitude;
        var mylng = position.coords.longitude

        const origin = {
            lat: mylat,
            lng: mylng
        };
        const destination = {
            lat: data_lat,
            lng: data_lng
        };
        const request = {
            origins: [origin],
            destinations: [destination],
            travelMode: google.maps.TravelMode.DRIVING,
            unitSystem: google.maps.UnitSystem.METRIC,
            avoidHighways: false,
            avoidTolls: false,
        };

        service.getDistanceMatrix(request).then((response) => {
            if (response) {
                var distance = response.rows[0].elements[0].distance.text;
                var duration = response.rows[0].elements[0].duration.text;
                console.log(distance, duration)
                $('#dis_dur').append(
                    "<table className='table table-striped'><thead><th id='th'>Distance</th><th>Duration (A-My Location B-Requested Destination)</th><tbody><tr> <td> " + distance + " </td> <td>" + duration + "</td> </tr></tbody></thead></table>"
                )
            } else {
                console.log('no response found')
            }
        });
    })



    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: {
            lat: data_lat,
            lng: data_lng
        },
    });
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer)
}


function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    // current location to panic location route by zhf
    navigator.geolocation.getCurrentPosition(
        (position) => {
            directionsService.route({
                origin: {
                    // my location
                    query: `${position.coords.latitude}, ${position.coords.longitude}`,
                },
                // requested location
                destination: {
                    query: `${data_lat}, ${data_lng}`,
                },
                travelMode: google.maps.TravelMode.DRIVING,
            },
                (response, status) => {
                    if (status === "OK") {
                        directionsRenderer.setDirections(response);
                    } else {
                        alert("Directions request failed due to " + status);
                    }
                }
            );
        }
    )
}
