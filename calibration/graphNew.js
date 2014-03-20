Network = function(){
  // variables we want to access
  // in multiple places of Network
  var  width = 960
  var  height = 800
  //  allData will store the unfiltered data
  var allData = []
  var  curLinksData = [];
  var  curNodesData = [];
  var  linkedByIndex = {};
  // these will hold the svg groups for
  // accessing the nodes and links display
  var  nodesG = null;
  var  linksG = null;
  // these will point to the circles and lines
  // of the nodes and links
  var  node = null;
  var  link = null;
  // variables to refect the current settings
  // of the visualization
  var  layout = "force";


  // our force directed layout
  var  force = d3.layout.force();
  // color function used to color nodes
  var nodeColors = d3.scale.category20();

  function network(selection, data){
    // format our data
    allData = setupData(data)

    // create our svg and groups
    vis = d3.select(selection).append("svg")
      .attr("width", width)
      .attr("height", height)
    linksG = vis.append("g").attr("id", "links")
    nodesG = vis.append("g").attr("id", "nodes")

    // setup the size of the force environment
    force.size([width, height])

    // setLayout("force")
    // setFilter("all")

    // perform rendering and start force layout
    update()
  }

  force.on("tick", forceTick)
  .charge(-200)


  function update(){
    //  filter data to show based on current filter settings.
    curNodesData = allData.nodes;
    curLinksData = allData.links;


    // reset nodes and links in force layout
    force.nodes(curNodesData)
    .links(curLinksData)
    .linkDistance(function(d){return -d.power});
    // enter / exit for nodes
    updateNodes();
    updateLinks();


    // start me up!
    force.start()
  }

  // enter/exit display for nodes
  function updateNodes(){
    node = nodesG.selectAll("circle.node")
      .data(curNodesData, function(d) { return d.name ;});

    node.enter().append("circle")
      .attr("class", "node")
      .attr("cx", function(d){ return d.x; })
      .attr("cy", function(d){ return d.y; })
      .attr("r", function(d){ return scale(d.power); })
      .style("fill", function(d,i){ return colors(i) })
      .call(force.drag);
      // .style("stroke", function(d){ return strokeFor(d); })
      // .style("stroke-width", 1.0)

    // node.on("mouseover", showDetails)
    //   .on("mouseout", hideDetails)

    node.exit().remove()
  }

  // enter/exit display for links
  function updateLinks(){
    link = linksG.selectAll("line.link")
      .data(curLinksData, function(d){ return "#{d.source.id}_#{d.target.id}"});

    link.enter().append("line")
      .attr("class", "link")
      .attr("stroke", "#ddd")
      .attr("stroke-opacity", 0.8)
      .attr("x1", function(d){ return d.source.x;})
      .attr("y1", function(d){ return d.source.y;})
      .attr("x2", function(d){ return d.target.x;})
      .attr("y2", function(d){ return d.target.y;})

    link.exit().remove()
  }
  network.toggleLayout = function(newLayout){
    // # public function

  }

  // tick function for force directed layout
  function forceTick(e){
    node
      .attr("cx", function(d){ return d.x;})
      .attr("cy", function(d){ return d.y;});

    link
      .attr("x1", function(d){ return d.source.x;})
      .attr("y1", function(d){ return d.source.y;})
      .attr("x2", function(d){ return d.target.x;})
      .attr("y2", function(d){ return d.target.y;});
  }

  network.updateData = function(newData){
      allData = setupData(newData)
      // link.remove()
      // node.remove()
      update()
  }
  // called once to clean up raw data and switch links to
  // point to node instances
  // Returns modified data
  setupData = function(data){
    // initialize circle radius scale

    data.links = new Array();
    data.nodes = new Array();
    data.nodes.push({'name' : "Listener", 'power': -10, 'kind': "Listener", 'weight': 0});
    for (var i = 0; i < data.length; i++) {

      var node = JSON.parse(data[i])

      var n = {'name' : $.trim(node.BSSID), 'power': node.power, 'kind': node.kind};
      var l = {'source' : data.nodes[0].name, 'target': $.trim(node.BSSID), 'power':node.power};
      data.nodes.push(n);
      data.links.push(l);

    }
    countExtent = d3.extent(data.nodes, function(d){ return d.power;});
    circleRadius = d3.scale.sqrt().range([3, 10]).domain(countExtent);
    data.links.forEach( function(n){
      // set initial x/y to values within the width/height
      // of the visualization
      // n.x = randomnumber=Math.floor(Math.random()*width);
      // n.y = randomnumber=Math.floor(Math.random()*height);

      // add radius to the node so we can use it later
      n.radius = circleRadius(n.power);
    });

    // id's -> node objects
    var nodesMap  = mapNodes(data.nodes);
    console.log(nodesMap);
    data.links.forEach( function(l){
      l.source = nodesMap.get(l.source);
      l.target = nodesMap.get(l.target);
      // linkedByIndex is used for link sorting
      linkedByIndex[l.source + " : "+l.target] = 1;
    });



    return data;
  }

  // Helper function to map node id's to node objects.
  // Returns d3.map of ids -> nodes
  mapNodes = function(nodes){
    nodesMap = d3.map();

    nodes.forEach (function(n){
      nodesMap.set(n.name, n);
    });

    return nodesMap;
  }


  return network

}
