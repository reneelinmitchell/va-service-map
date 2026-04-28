var map = L.map('map').setView([37.5, -78.8], 7);

// Tile layer
L.tileLayer(
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
{
maxZoom: 19
}).addTo(map);

var markers = [];

fetch("/services")
.then(res => res.json())
.then(data => {

data.forEach(service => {

var emojiIcon = L.divIcon({
html: service.emoji,
className: 'emoji-icon',
iconSize: [30,30]
});

var marker = L.marker(
[service.lat, service.lng],
{ icon: emojiIcon }
).addTo(map);

marker.on("click", function(){

document.getElementById("details").innerHTML =
`
<h3>${service.name}</h3>
<p><b>City:</b> ${service.city}</p>
<p>${service.description}</p>
<a href="${service.website}" target="_blank">
Visit Website
</a>
`;

});

markers.push({
marker: marker,
city: service.city,
lat: service.lat,
lng: service.lng
});

});

});

// Load Cities
fetch("/cities")
.then(res => res.json())
.then(cities => {

var dropdown =
document.getElementById("cityDropdown");

cities.forEach(city => {

var option =
document.createElement("option");

option.value = city;
option.text = city;

dropdown.appendChild(option);

});

});

// Zoom on City
document.getElementById("cityDropdown")
.addEventListener("change", function(){

var selected = this.value;

markers.forEach(m => {

if(m.city === selected){

map.setView(
[m.lat, m.lng],
12
);

}

});

});