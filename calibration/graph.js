

app = new Object();
app.server = 'localhost:8080';
app.nodes = [];
app.links = [];
var node = null;
var link = null;

// var force = d3.layout.force()
//   .nodes(app.nodes)
//   .links(app.links)
//   .friction(0.7)
//   .charge([-100])
//   .size([app.width, app.height]);
//
//
// var svg = d3.select('body')
//     .append('svg:svg')
//     .attr('width', app.width)
//     .attr('height', app.height);
//
//
//
// function update () {
//   force.nodes(app.nodes);
//   force.links(app.links);
//   force.linkDistance(function(d){
//     return scale(d.power);
//   }); //.on("tick", tick);
//   if(node !==null)node.remove();
//
//   // link.remove();
//
//   force.start();
//   updateNodes();
//   // updateLinks();
//
// }
//
// function tick(){
//   node.attr("cx", function(d) { return d.x; })
//   .attr("cy", function(d) { return d.y; });
//
//   // console.log(node);
//   link.attr("x1", function(d) { return d.source.x; })
//   .attr("y1", function(d) { return d.source.y; })
//   .attr("x2", function(d) { return d.target.x; })
//   .attr("y2", function(d) { return d.target.y; });
// }
//
// function updateLinks(){
//   link = svg.selectAll("line")
//   .data(app.links, function(d) { return d.source + "-" + d.target; })
//   .enter()
//   .append("line");
// }
//
// function updateNodes(){
  //Data Join method, update already exisitng objects data
  //Using the key method. Name is the unique BSSID for each node.

  // function(d){ console.log(d.name); return d.name;}
  // node = svg.selectAll("circle")
  //   .data(app.nodes)
  //   .attr("attr","update")
  //   .transition()
  //     .duration(750)
  //     .attr("r",function(d){
  //       return scale(d.power)
  //     });

  // node.call(force.drag);

  //Enter
    // var  nodes = svg.selectAll("circle")
    //   .data(app.nodes)
    //   .enter()
    //   .append("circle")
    //   .attr("r",4)
    //   .style("fill", function(d, i) {
    //           return colors(i);
    //   })
    //   .call(force.drag);
    //
    //   var edges = svg.selectAll("line")
    //       .data(app.links)
    //       .enter()
    //       .append("line");
    //   force.on("tick", function() {
    //
    //       edges.attr("x1", function(d) { return d.source.x; })
    //            .attr("y1", function(d) { return d.source.y; })
    //            .attr("x2", function(d) { return d.target.x; })
    //            .attr("y2", function(d) { return d.target.y; });
    //
    //       nodes.attr("cx", function(d) { return d.x; })
    //            .attr("cy", function(d) { return d.y; });
    //
    //   });
  // .attr("r",function(d){
  //   return scale(d.power)
  // })
  // .style("fill", function(d, i) {
  //   if(d.kind == "Listener"){
  //     return colors(1);
  //   }
  //   return (d.kind === "Client")?colors(2):colors(3);
  // })
  // .call(force.drag);

  //Exit
  // node.exit().remove()

//}

//
// function tick() {
//   links.attr("x1", function(d) { return d.source.x; })
//   .attr("y1", function(d) { return d.source.y; })
//   .attr("x2", function(d) { return d.target.x; })
//   .attr("y2", function(d) { return d.target.y; });
//
//   nodes.attr("cx", function(d) { return d.x; })
//   .attr("cy", function(d) { return d.y; });
// }
//
// function initGraphWithChildren(){
//
//   var force = d3.layout.force()
//   .on("tick", tick)
//   .charge(function(d) { return d._children ? -d.size / 100 : -30; })
//   .linkDistance(function(d) { return d.target._children ? 80 : 30; })
//   .size([app.width, app.height - 160]);
//
//   root = app.nodes;
//   console.log(root);
//   root.x0 = app.height / 2;
//   root.y0 = 0;
//
//   function collapse(d) {
//     if (d.children) {
//       d._children = d.children;
//       d._children.forEach(collapse);
//       d.children = null;
//     }
//   }
//
//   root[0].children.forEach(collapse);
//   // update(root);
//
//
//
//   svg = d3.select('body')
//   .append('svg:svg')
//   .attr('width', app.width)
//   .attr('height', app.height);
//
//   var nodes = flatten(root);
//
//   // var nodes = d3./layout.tree.nodes(ns);
//   var links = d3.layout.tree().links(nodes[0]);
//   console.log(links);
//   // Restart the force layout.
//   force
//   .nodes(nodes[0])
//   .links(links)
//   .start();
//
//   // Update the links…
//   link = svg.selectAll("line.link")
//   .data(links, function(d) { return d; });
//
//   // Enter any new links.
//   link.enter().insert("svg:line", ".node")
//   .attr("class", "link")
//   .attr("x1", function(d) { return d.source.x; })
//   .attr("y1", function(d) { return d.source.y; })
//   .attr("x2", function(d) { return d.target.x; })
//   .attr("y2", function(d) { return d.target.y; });
//
//   // Exit any old links.
//   link.exit().remove();
//
//   // Update the nodes…
//   node = svg.selectAll("circle.node")
//   .data(nodes[0], function(d) {console.log(d); return d; })
//   .style("fill", childrenColor);
//
//   node.transition()
//   .attr("r", function(d) { return d.children ? 4.5 : Math.sqrt(d.size) / 10; });
//
//   // Enter any new nodes.
//   node.enter().append("svg:circle")
//   .attr("class", "node")
//   .attr("cx", function(d) { return d.x; })
//   .attr("cy", function(d) { return d.y; })
//   .attr("r", function(d) { return 10 })//return d.children ? 4.5 : Math.sqrt(d.size) / 10;
//   .style("fill", childrenColor)
//   // .on("click", click)
//   .call(force.drag);
//
//   // Exit any old nodes.
//   node.exit().remove();
// }
