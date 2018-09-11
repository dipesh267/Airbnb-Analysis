const app = document.getElementById('map');

var request = new XMLHttpRequest();
request.open('GET', 'http://127.0.0.1:5000/coordinates', true);

console.log("before onload");
  
request.onload = function () {
console.log(request.status);
  
  // Begin accessing JSON data here
  var data = JSON.parse(this.response);
  if (request.status >= 200 && request.status < 400) {
    console.log(data);
    // const logo = document.createElement('img');
    // logo.src = data.featured_image_url;

    // const myh1 = document.createElement('h1');
    // myh1.textContent = data.mars_weather;
    // console.log(myh1);
    // app.appendChild(myh1);
    // app.appendChild(logo);

  } else {
    console.log('error');
  }
}

request.send();