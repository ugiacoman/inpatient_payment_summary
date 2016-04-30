mapboxgl.accessToken = 'pk.eyJ1IjoidWdpYWNvbWFuIiwiYSI6ImNpbW8xdTUwejAwYXF1N2x5dmRydnpuZTIifQ.YF2LyOa-5Ookoi4_kpmCEg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v8',
    center: [-98, 38.88],
    maxZoom: 5,
    minZoom: 1,
    zoom: 3
});

// Holds visible airport features for filtering
var airports = [];

// Create a popup, but don't add it to the map yet.
var popup = new mapboxgl.Popup({
    closeButton: false
});

var filterEl = document.getElementById('feature-filter');
var listingEl = document.getElementById('feature-listing');

function renderListings(features) {
    // Clear any existing listings
    listingEl.innerHTML = '';
    if (features.length) {
        features.forEach(function(feature) {
            var prop = feature.properties;
            var item = document.createElement('a');
            item.href = prop.wikipedia;
            item.target = '_blank';
            item.textContent = prop.name + ' (' + prop.abbrev + ')';
            item.addEventListener('mouseover', function() {
                // Highlight corresponding feature on the map
                popup.setLngLat(feature.geometry.coordinates)
                    .setText(feature.properties.name + ' (' + feature.properties.abbrev + ')')
                    .addTo(map);
            });
            listingEl.appendChild(item);
        });

        // Show the filter input
        filterEl.parentNode.style.display = 'block';
    } else {
        var empty = document.createElement('p');
        empty.textContent = 'Drag the map to populate results';
        listingEl.appendChild(empty);

        // Hide the filter input
        filterEl.parentNode.style.display = 'none';
    }
}

function normalize(string) {
    return string.trim().toLowerCase();
}

map.on('load', function() {

    // Add our vector tile source: World wide
    // airports provided by Natural Earth
    map.addSource('airports', {
        "type": "vector",
        "url": "/test-select"
    });

    map.addLayer({
        "id": "airport",
        "source": "airports",
        "source-layer": "ne_10m_airports",
        "type": "symbol",
        "layout": {
            "icon-image": "airport-15",
            "icon-padding": 0
        },
        "filter": ["in", "abbrev", ""]
    });

    map.on('moveend', function() {
        var features = map.querySourceFeatures('airports', {
            sourceLayer: 'ne_10m_airports'
        });

        if (features) {
            // Populate features for the listing overlay.
            renderListings(features);

            // Clear the input container
            filterEl.value = '';

            // Store the current features in sn `airports` variable to
            // later use for filtering on `keyup`.
            airports = features;

            // Set the filter to populate features into the layer.
            map.setFilter('airport', ['in', 'abbrev'].concat(features.map(function(feature) {
                return feature.properties.abbrev;
            })));
        }
    });

    map.on('mousemove', function(e) {
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['airport']
        });

        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = features.length ? 'pointer' : '';

        if (!features.length) {
            popup.remove();
            return;
        }

        var feature = features[0];

        // Populate the popup and set its coordinates
        // based on the feature found.
        popup.setLngLat(feature.geometry.coordinates)
            .setText(feature.properties.name + ' (' + feature.properties.abbrev + ')')
            .addTo(map);
    });

    filterEl.addEventListener('keyup', function(e) {
        var value = normalize(e.target.value);

        // Filter visible features that don't match the input value.
        var filtered = airports.filter(function(feature) {
            var name = normalize(feature.properties.name);
            var code = normalize(feature.properties.abbrev);
            return name.indexOf(value) > -1 || code.indexOf(value) > -1;
        });

        // Populate the sidebar with filtered results
        renderListings(filtered);

        // Set the filter to populate features into the layer.
        map.setFilter('airport', ['in', 'abbrev'].concat(filtered.map(function(feature) {
            return feature.properties.abbrev;
        })));
    });

    // Call this function on initialization
    // passing an empty array to render an empty state
    renderListings([]);
});