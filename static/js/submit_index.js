async function initMap() {
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const city = document.getElementById('id_city');
  const map = new Map(document.getElementById("map"), {
    center: { lat: 41.3775, lng: 64.5853 },
    zoom: 7,
    mapId: "4504f8b37365c3d0",
  });
  const draggableMarker = new AdvancedMarkerElement({
    map,
    position: { lat: 41.3775, lng: 64.5853 },
    gmpDraggable: true
  });

  draggableMarker.addListener("dragend", (event) => {
    const position = draggableMarker.position;
    document.getElementById('id_lat').value = position.lat;
    document.getElementById('id_long').value = position.lng;
    map.setCenter(position);
  });
  city.addEventListener('change', () => {
      var latitude = $('#id_city option:selected').data('lat');
      var longitude = $('#id_city option:selected').data('long');
      const newPos = {lat: latitude, lng: longitude};
      draggableMarker.position = newPos;
      map.setCenter(newPos);
      map.setZoom(12)
  });
}

initMap();