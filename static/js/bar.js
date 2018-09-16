/* pie route */
var url = "/list-count-json";

function buildPlot() {
  d3.json(url, function(response) {
      //console.log(response);
    var myData = Object.values(response); 
    //console.log(myData);
    var data = [{
      y: myData.map(data => data.count),
      x: myData.map(data => data.neighbourhood),
      type: "bar"
    }];

  Plotly.plot("bar_plot", data);
  });
}
buildPlot();