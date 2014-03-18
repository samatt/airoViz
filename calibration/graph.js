

function initGraph () {

  svg = d3.select('body')
    .append('svg:svg')
    .attr('width', calibration.width)
    .attr('height', calibration.height);

  var force = d3.layout.force()
      .nodes(calibration.data.nodes)
      .links(calibration.data.links)
      .linkDistance(function(d){
        return scale(d.power);
      })
      .charge([-100])
      .size([calibration.width, calibration.height])
      .start();

  var edges = svg.selectAll("line")
      .data(calibration.data.links)
      .enter()
      .append("line");
      // .style("stroke", "#ccc")
      // .style("stroke-width", function(d){
      // 		return scale(-d.power);
      // });

    var nodes = svg.selectAll("circle")
      .data(calibration.data.nodes)
      .enter()
      .append("circle")
      .attr("r",4)
      .style("fill", function(d, i) {
              return colors(i);
      })
      .call(force.drag);

    force.on("tick", function() {

        edges.attr("x1", function(d) { return d.source.x; })
             .attr("y1", function(d) { return d.source.y; })
             .attr("x2", function(d) { return d.target.x; })
             .attr("y2", function(d) { return d.target.y; });

        nodes.attr("cx", function(d) { return d.x; })
             .attr("cy", function(d) { return d.y; });

    });
}
