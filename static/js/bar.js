/* pie route */
var url = "/list-count-json";

function buildPlot() {
  d3.json(url, function(response) {
      //console.log(response);
    var myData = Object.values(response); 
    //console.log(myData);
    var data = [{
      y: myData.map(data => data.value),
      x: myData.map(data => data.neighbourhood),
      type: "bar"
    }];

  Plotly.newPlot("bar_plot", data);
  });
}
buildPlot();

// Submit Button handler
function handleSubmit1() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Build the plot with the new stock
  url = "/list-count-json";
  buildPlot();
}

function handleSubmit2() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Build the plot with the new stock
  url = "/maxprice-json";
  buildPlot();
}

function updatePlotly(newdata) {
  Plotly.restyle("bar", "x", [newdata.x]);
  Plotly.restyle("bar", "y", [newdata.y]);
}
// function buildPlot(url) {

//   // Grab values from the response json object to build the plots
//     d3.json(url, function(response) {
//       //console.log(response);
//       var myData = Object.values(response); 
//       //console.log(myData);
//       var data = [{
//         y: myData.map(data => data.value),
//         x: myData.map(data => data.neighbourhood),
//         type: "bar"
//     }];
//     Plotly.newPlot("bar_plot", data);
//   });
// }

// // Add event listener for submit button
d3.select("#button1").on("click", handleSubmit1);
d3.select("#button2").on("click", handleSubmit2);