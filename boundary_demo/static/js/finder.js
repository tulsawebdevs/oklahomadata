var geolocate_supported = true, // until prove false

    geocoder = new google.maps.Geocoder(),
    southwest_limit = new L.LatLng(32.1342, -95.6219), // @todo Replace coordinates.
    northeast_limit = new L.LatLng(32.6871, -94.9844), // @todo Replace coordinates.
    bounding_box = new L.LatLngBounds(southwest_limit, northeast_limit),
    outside = false, // until prove true

    map = null,

    user_marker = null,
    displayed_boundary_slug = null,
    displayed_polygon = null,
    displayed_point_slug = null,
    displayed_points = [],

    boundaries = new Array(),
    points = new Array(),

    getGlobal = function(v){return (typeof window[v] != 'undefined')?window[v]:null;},
    point_marker_icon = L.Icon.extend({
        iconUrl: '/leaflet/images/marker2.png',
        shadowUrl: '/leaflet/images/marker-shadow.png',
        iconSize: new L.Point(25, 41),
        shadowSize: new L.Point(41, 41),
        iconAnchor: new L.Point(13, 41),
        popupAnchor: new L.Point(0, -33)
    })

function init_map(lat, lng) {
    if (map == null) {
        var ll = new L.LatLng(lat, lng);

        map = new L.Map('map_canvas', {
            zoom: 14,
            center: ll,
        });

        tiles = new L.TileLayer("http://mt1.google.com/vt/lyrs=m@155000000&hl=en&x={x}&y={y}&z={z}&s={s}", {
            maxZoom: 17,
            attribution: "Map data is Copyright Google, 2011"
        });
        
        map.addLayer(tiles);
    }

    var center = new L.LatLng(lat, lng);
    map.panTo(center);

    check_for_locale(center);
    resize_listener(center);
}

function show_user_marker(lat, lng) {
    var ll = new L.LatLng(lat, lng);

    if (user_marker != null) {
        map.removeLayer(user_marker);
        user_marker = null;
    }

    user_marker = new L.Marker(ll, { draggable: true });
    map.addLayer(user_marker);

    user_marker.on('dragend', function() {
        ll = user_marker.getLatLng();
        geocode(ll)
    });
}

function geocode(query) {
    if (typeof(query) == 'string') {
        gr = { 'address': query };
    } else {
        gr = { 'location': new google.maps.LatLng(query.lat, query.lng) };
    }
    geocoder.geocode(gr, handle_geocode);
}

function handle_geocode(results, status) {
    alt_addresses(results);

    lat = results[0].geometry.location.lat();
    lng = results[0].geometry.location.lng();
    
    last_location = [lat, lng];
    
    normalized_address = results[0].formatted_address;
    $('#location-form #address').val(normalized_address);
    
    process_location(lat, lng);
    save_last_location(last_location);
}

function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(geolocation_success, geolocation_error);
    } else {
        use_default_location();

        $('#resultinfo').html("Your browser does not support automatically determining your location so we're showing you Example Place."); // @todo Replace "Example Place"

        geolocate_supported = false;
    }
}

function geolocation_success(position) {
    process_location(position.coords.latitude, position.coords.longitude)
    ll = new L.LatLng(position.coords.latitude, position.coords.longitude);

    geocode(ll);
    check_for_locale(ll);
    hide_search()
}

function geolocation_error() {
    use_default_location();

    $('#resultinfo').html("Your browser does not support automatically determining your location so we're showing you Example Place."); // @todo Replace "Example Place"
}

function process_location(lat, lng) {
    $('#resultinfo').html(
        'Latitude: ' + lat + '<br />' +
        'Longitude: ' + lng + '<br />'
    );

    init_map(lat, lng);
    show_user_marker(lat, lng);
    get_boundaries(lat, lng);
    get_points(lat, lng);
}

function save_last_location(location) {
    store.set('last_location', location);
}

function get_last_location() {
    last_location = store.get('last_location');
    return last_location;
}

function clear_last_location() {
    store.remove('last_location');
}

function check_saved_location() {
    last_location = get_last_location();
    if (last_location) {
        return true;
    } else {
        return false;
    }
}

function check_for_locale(center) {
    var temp = new L.LatLngBounds(center, center);

    if (!bounding_box.contains(temp) && window.location.hash == "#demo") {
        show_outside();
        outside = true;
    } else {
        hide_outside();
        outside = false;
    }
}

function alt_addresses(results) {
    $('#alt-addresses').html('');

    keep = new Array();

    $.each(results, function(i,val) {
        if (i==0) return; // skip the first result

        for (var t in val.types) {
            if (val.types[t] == 'street_address' || val.types[t] == 'intersection') {
                keep.push(val.formatted_address);
                break;
            }
        }
    });

    if (keep.length <= 1) {
        $('#did-you-mean')
            .addClass('disabled-link')
            .unbind();
    } else {
        $('#did-you-mean')
            .removeClass('disabled-link')
            .click(function(e) { 
                    e.stopPropagation(); 
                    toggle_alt_addresses(); 
                    });

        for (var i in keep) {
            $('#alt-addresses').append('<a href="javascript:geocode(\'' + keep[i] + '\');">' + keep[i] + '</a><br />');
        }
    }
}

// Use boundary service to lookup what areas the location falls within
function get_boundaries(lat, lng) {
    var table_html = '<h3>This location is within:</h3><table id="boundaries" border="0" cellpadding="0" cellspacing="0">',
        query_url = '1.0/boundary/?limit=100&contains=' + lat + ',' + lng + '',
        displayed_kind = null,
        for_display = null;

    if (displayed_polygon != null) {
        // Hide old polygon
        displayed_kind = boundaries[displayed_boundary_slug].kind;
        map.removeLayer(displayed_polygon);
        displayed_polygon = null;
        displayed_boundary_slug = null;
    }

    // Clear old boundaries
    boundaries.length = 0;

    $.getJSON(query_url, function(data) {
        $.each(data.objects, function(i, obj) {
            boundaries[obj.slug] = obj;
            table_html += '<tr id="' + obj.slug + '"><td>' + obj.kind + '</td><td><strong><a href="javascript:display_boundary(\'' + obj.slug + '\');">' + obj.name + '</a></strong></td></td>';

            // Try to display a new polygon of the same kind as the last shown
            if (displayed_kind != null && obj.kind == displayed_kind) {
                for_display = obj; 
            }
        });
        table_html += '</table>';
        $('#area-lookup-boundaries').html(table_html);

        if (for_display != null) {
            display_boundary(for_display.slug, true);
        }
    });
}

function get_points(lat, lng) {
    var table_html = '<h3>Points within 1 mile of this:</h3><table id="points" border="0" cellpadding="0" cellspacing="0">',
        query_url = '1.0/point/?limit=100&near=' + lat + ',' + lng + ',1mi',
        displayed_kind = null,
        for_display = null;

    if (displayed_points.length) {
        // Hide old polygon
        displayed_kind = points[displayed_point_slug].kind;
        map.removeLayer(displayed_points);
        displayed_points = [];
        displayed_point_slug = null;
    }

    // Clear old points
    points.length = 0;

    $.getJSON(query_url, function(data) {
        $.each(data.objects, function(i, obj) {
            points[obj.slug] = obj;
            table_html += '<tr id="' + obj.slug + '"><td>' + obj.kind + '</td><td><strong><a href="javascript:display_point(\'' + obj.slug + '\');">' + obj.name + '</a></strong></td></td>';

            // Try to display a new polygon of the same kind as the last shown
            if (displayed_kind != null && obj.kind == displayed_kind) {
                for_display = obj; 
            }
        });
        table_html += '</table>';
        $('#area-lookup-points').html(table_html);

        if (for_display != null) {
            display_point(for_display.slug, true);
        }
    });
}

function display_boundary(slug, no_fit) {
    // Clear old polygons
    if (displayed_polygon != null) {
        map.removeLayer(displayed_polygon);
        displayed_polygon = null;
        displayed_boundary_slug = null;

        $("#boundaries .selected").removeClass("selected");
    }

    // Construct new polygons
    var coords = boundaries[slug]["simple_shape"].coordinates;
    var paths = [];
    var bounds = null;

    $.each(coords, function(i, n){
        $.each(n, function(j, o){
            var path = [];

            $.each(o, function(k,p){
                var ll = new L.LatLng(p[1], p[0]);
                path.push(ll);

                if (bounds === null) {
                    bounds = new L.LatLngBounds(ll, ll);
                } else {
                    bounds.extend(ll);
                }
            });

            paths.push(path);
        });
    });

    displayed_polygon = new L.Polygon(paths, {
        color: "#244f79",
        opacity: 0.8,
        weight: 3,
        fill: true,
        fillColor: "#244f79",
        fillOpacity: 0.2
    });

    displayed_boundary_slug = slug;
    map.addLayer(displayed_polygon);

    $("#boundaries #" + slug).addClass("selected");

    if (!no_fit) {
        map.fitBounds(bounds);
    }
}

function display_point(slug, no_fit) {
    // Clear old points 
    if (displayed_points.length) {
        for(var p = 0; p < displayed_points.length; p++){
            map.removeLayer(displayed_points[p]);
        }
        displayed_points = [];
        displayed_boundary_slug = null;

        $("#points .selected").removeClass("selected");
    }

    // Construct new polygons
    var coords = points[slug]["point"].coordinates,
        bounds = null;

    $.each(coords, function(i, p){
        var ll = new L.LatLng(p[1], p[0]),
            marker = new L.Marker(ll, {icon: new point_marker_icon()});
        displayed_points.push(marker);
        map.addLayer(marker);

        if (bounds === null) {
            bounds = new L.LatLngBounds(ll, ll);
        } else {
            bounds.extend(ll);
        }
    });
    displayed_point_slug = slug;

    $("#points #" + slug).addClass("selected");

    if (!no_fit) {
        map.fitBounds(bounds);
    }
}

function show_search() {
    $('#not-where-i-am').hide();
    if (geolocate_supported) { $('#use-current-location').fadeIn(); }
    $('#did-you-mean').fadeIn();
    $('#location-form').slideDown();
}

function hide_search() {
    $('#not-where-i-am').show();
    $('#use-current-location').hide()
    $('#location-form').slideUp();
}

function switch_page(page_id) {
    $(".page-content").hide()
    $("#" + page_id + "-page").show()
    window.location.hash = page_id

    if (window.location.hash == "#demo") {
        if (outside) {
            show_outside();
        }

        resize_end_trigger(); 

        if (!map) {
            if (check_saved_location()) {
                last_location = store.get('last_location');
                geocode(new L.LatLng(last_location[0], last_location[1]));
            } else {
                geolocate();
            }
        }
    } else {
        hide_outside();
    }
}


function show_outside() {
    $('#outside').fadeIn(500);
}

function hide_outside() {
    $('#outside').fadeOut(250);
}

/* DOM EVENT HANDLERS */
function resize_listener(center) {
    $(this).bind('resize_end', function(){ 
        if (map) {
            map.panTo(center);
        }
    });
}

function resize_end_trigger() {
    $(window).resize(function() {
        if (this.resizeto) { 
            clearTimeout(this.resizeto) 
            };

        this.resizeto = setTimeout(function() { 
            $(this).trigger('resize_end'); 
            }, 500);
    });
}

function not_where_i_am() {
    show_search();
}

function use_current_location() {
    geolocate();
}

function use_default_location() {
    var location = getGlobal('default_location') || ["32.349549", "-95.301829"];
    process_location(parseFloat(location[0]), parseFloat(location[1]));
}

function toggle_alt_addresses() {
    alt_adds_div = $('#alt-addresses');
    if (alt_adds_div.is(':hidden')) {
        show_alt_addresses();
    } else if (alt_adds_div.is(':visible')) {
        hide_alt_addresses();
    }
}

function show_alt_addresses() {
    $('#alt-addresses').slideDown(250);
    $('#did-you-mean').addClass('highlight');
}

function hide_alt_addresses() {
    $('#alt-addresses').hide();
    $('#did-you-mean.highlight').removeClass('highlight');
}

function search_focused() {
    if(this.value == 'Enter an address or drag the pin on the map') {
        $(this).val("");
    }
}

function address_search() {
    geocode($("#location-form #address").val());

    return false;
}

$(document).ready(function() {
    // Setup handlers
    $('body').click(hide_alt_addresses);
    $('#not-where-i-am').click(not_where_i_am);
    $('#use-current-location').click(use_current_location);
    $('#use-default-location').click(use_default_location);
    $('#did-you-mean').click(function(e) { e.stopPropagation(); toggle_alt_addresses(); });
    $('#location-form input[type=text]').focus(search_focused);
    $('#location-form').submit(address_search)

    if (window.location.hash != "") {
        switch_page(window.location.hash.substring(1));
    } else {
        switch_page("demo");
    }
});


