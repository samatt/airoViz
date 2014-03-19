

function initGraph () {


  svg = d3.select('body')
    .append('svg:svg')
    .attr('width', calibration.width)
    .attr('height', calibration.height);

  var force = d3.layout.force()
      .nodes(calibration.data.nodes)
      .links(calibration.data.links)
      .friction(0.7)
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

    var nodes = svg.selectAll("circle")
      .data(calibration.data.nodes)
      .enter()
      .append("circle")
      .attr("r",function(d){
            if(d.kind == "Listener"){
              return 10;
            }
            return (d.kind === "Client") ? 4:6;
        }
      )
      .style("fill", function(d, i) {
              if(d.kind == "Listener"){
                return colors(1);
              }
              return (d.kind === "Client")?colors(2):colors(3);
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

function tick() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

function initGraphWithChildren(){

  var force = d3.layout.force()
      .on("tick", tick)
      .charge(function(d) { return d._children ? -d.size / 100 : -30; })
      .linkDistance(function(d) { return d.target._children ? 80 : 30; })
      .size([calibration.width, calibration.height - 160]);

  root = calibration.data.nodes;
  console.log(root);
  root.x0 = calibration.height / 2;
  root.y0 = 0;

  function collapse(d) {
    if (d.children) {
      d._children = d.children;
      d._children.forEach(collapse);
      d.children = null;
    }
  }

  root[0].children.forEach(collapse);
  // update(root);



  svg = d3.select('body')
    .append('svg:svg')
    .attr('width', calibration.width)
    .attr('height', calibration.height);

    var nodes = flatten(root);

    // var nodes = d3./layout.tree.nodes(ns);
    var links = d3.layout.tree().links(nodes[0]);
console.log(links);
    // Restart the force layout.
    force
        .nodes(nodes[0])
        .links(links)
        .start();

    // Update the links…
    link = svg.selectAll("line.link")
        .data(links, function(d) { return d; });

    // Enter any new links.
    link.enter().insert("svg:line", ".node")
        .attr("class", "link")
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    // Exit any old links.
    link.exit().remove();

    // Update the nodes…
    node = svg.selectAll("circle.node")
        .data(nodes[0], function(d) {console.log(d); return d; })
        .style("fill", childrenColor);

    node.transition()
        .attr("r", function(d) { return d.children ? 4.5 : Math.sqrt(d.size) / 10; });

    // Enter any new nodes.
    node.enter().append("svg:circle")
        .attr("class", "node")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", function(d) { return 10 })//return d.children ? 4.5 : Math.sqrt(d.size) / 10;
        .style("fill", childrenColor)
        // .on("click", click)
        .call(force.drag);

    // Exit any old nodes.
    node.exit().remove();
}
