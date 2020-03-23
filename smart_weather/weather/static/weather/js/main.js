function getWeatherLocation() {
  function success(position) {
    const latitude  = position.coords.latitude.toPrecision(6);
    const longitude = position.coords.longitude.toPrecision(6);

    document.querySelector('#map').src = `https://cobra.maps.arcgis.com/apps/webappviewer/index.html?id=ee70f4d7437d47bb88cf9de9eb4f8719&find=${longitude},${latitude}`;
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success);
  }
}

function getWeatherLocationByZip() {
  const zip  = document.querySelector('#enterZip').value;
  document.querySelector('#map').src = `https://cobra.maps.arcgis.com/apps/webappviewer/index.html?id=ee70f4d7437d47bb88cf9de9eb4f8719&find=${zip}`;
}

window.onload = function() {
  getWeatherLocation();
};