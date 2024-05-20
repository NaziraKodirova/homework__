async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  function fetchListings() {
    return fetch('get_listings')  // Replace with your view URL
        .then(response => response.json())
        .then(data => data);  // Return the fetched data
  }
  const listings = fetchListings();

  const locations = [];

  listings.then(data => {
      for (const listing of data) {
            locations.push({lat: listing.lat, lng: listing.lng, address: listing.address, about: listing.about, rooms: listing.rooms,
            price: listing.price, owner: listing.owner, city: listing.city, region: listing.region, urls: listing.urls,
            images: listing.images})
//            labels.push(listing.address)
      } // Log data after it's fetched

      const markers = locations.map((position, i) => {
        const pinGlyph = new google.maps.marker.PinElement({
          glyphColor: "white",
          background: "#416D19",
          borderColor: "#137333",
        });

        const marker = new google.maps.marker.AdvancedMarkerElement({
          position: { lat: position.lat, lng: position.lng},
          content: pinGlyph.element,
        });

        // markers can only be keyboard focusable when they have click listeners
        // open info window when marker is clicked
        const contentString =`
           <div class="carousel">
             ${position.images}
             <button class="previous-button">&#10094;</button>
             <button class="next-button">&#10095;</button>
           </div>
          <div id="info-window">
            <h2>${position.price}</h2>
            <p>${position.address} | ${position.city} | ${position.region}</p>
            <p><a href="${position.urls}">Learn more</a></p>
          </div>
        `;
        marker.addListener("click", () => {
          infoWindow.setContent(contentString);
          infoWindow.open(map, marker);
          google.maps.event.addListener(infoWindow, "domready", function() {
            $("#carousel-container").anythingSlider({
            autoPlay: true,
            buildNavigation: true,
            pauseOnHover: true,
            animationTime: 600,
            theme: "minimalist",
            infiniteScrolling: true,
            });
          });
        });
        return marker;
      });

      // Add a marker clusterer to manage the markers.
      new markerClusterer.MarkerClusterer({ markers, map,});
  });

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 7,
    center: { lat: 41.3775, lng: 64.5853 },
    mapId: "DEMO_MAP_ID",
  });
  const infoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });
}


initMap();