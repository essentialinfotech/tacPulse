function initMap() {
    my_lat = []
    my_lng = []
    my_title = []


    const myLatLng = { lat: 23.7808875, lng: 90.2792371 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 8,
        center: myLatLng,
    });
    $.ajax({
        method: "GET",
        url: '/api/dispatch/location/',
        success: function(data) {
            $.each(data, function(key, value) {
                var name = ''
                name = value.first_name + ' ' + value.last_name
                lat_lng = { lat: parseFloat(value.latitude), lng: parseFloat(value.longitude) }
                addMarker(lat_lng, name, map)
            });
        }
    });
}

function addMarker(location, tt, map) {

    // var icon_location = 'http://' + window.location.hostname + ':8000/static/images/Ambulance-icon.png'
    var icon_location = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '') + '/static/images/Ambulance-icon.png'

    const iconBase = {
        url: icon_location,
        // url: 'https://icons.iconarchive.com/icons/icons-land/transport/256/Ambulance-icon.png', // url
        scaledSize: new google.maps.Size(40, 40), // scaled size
        origin: new google.maps.Point(0, 0), // origin
        anchor: new google.maps.Point(0, 0) // anchor
    };
    var marker = new google.maps.Marker({
        position: location,
        icon: iconBase,
        title: tt,
        map: map
    });
}