data = coord_data;

// Once we get a response, send the data.features object to the createFeatures function
//console.log(data);

// console.log(data.features);
var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
    });

var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: API_KEY
});
var featureList = data;
    
//var listingMarkers = [];
var cMarkers = L.markerClusterGroup();
    
featureList.forEach(feature =>{  
    var coords = [feature.latitude,feature.longitude];
    var price = feature.price;
    var image = feature.picture_url;

    cMarkers.addLayer(L.marker(coords)
        .bindPopup("<h2>Price: " + price + "</h2>"));
});


var listingLayer = L.layerGroup(cMarkers);

    // Only one base layer can be shown at a time
    var baseMaps = {
        Light: light,
        Dark: dark
    };

    var overlayMaps = {
        Listings: cMarkers
    };

    var myMap = L.map("map", {
        center: [37.7749, -122.4194],
        zoom: 12,
        layers:[light,listingLayer]
    });
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);

    var url = "/map-geojson";
    d3.json(url, function(data) {
        // Create a new choropleth layer
        L.choropleth(data, {
      
          // Define what  property in the features to use
          valueProperty: "price",
      
          // Set color scale
          scale: ["#ffffb2", "#b10026"],
      
          // Number of breaks in step range
          steps: 10,
      
          // q for quartile, e for equidistant, k for k-means
          mode: "q",
          style: {
            // Border color
            color: "#fff",
            weight: 1,
            fillOpacity: 0.8
          },
          onEachFeature: function(feature, layer) {
            layer.bindPopup(feature.properties.neighbourhood + "<br>" + feature.properties.price );
          }
        }).addTo(myMap);
    });