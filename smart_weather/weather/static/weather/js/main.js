function getWeatherLocation() {
  function success(position) {
    const latitude  = position.coords.latitude.toPrecision(6);
    const longitude = position.coords.longitude.toPrecision(6);

    document.querySelector('#map').src = `//cobra.maps.arcgis.com/apps/Embed/index.html?webmap=c4fcd13aa52e4dcfb24cc6e90a970a59&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light&marker=${longitude},${latitude}&center=${longitude},${latitude}&level=10`;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success);
  }
}

function getWeatherLocationByZip() {
  const zip  = document.querySelector('#enterZip').value;
  document.querySelector('#map').src = `//cobra.maps.arcgis.com/apps/Embed/index.html?webmap=c4fcd13aa52e4dcfb24cc6e90a970a59&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light&center=${zip}&find=${zip}&level=8`;
}

window.onload = function() {
//  getWeatherLocation();
};