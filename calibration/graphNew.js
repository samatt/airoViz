Network = function(){
  // variables we want to access
  // in multiple places of Network
  var  width = app.width;
  var  height = app.height;
  //  allData will store the unfiltered data
  var allData = []
  var  curLinksData = [];
  var  curNodesData = [];
  var  linkedByIndex = {};
  // these will hold the svg groups fora
  // accessing the nodes and links display
  var  nodesG = null;
  var  linksG = null;
  // these will point to the circles and lines
  // of the nodes and links
  var  node = null;
  var  link = null;

  var nodesMap = d3.map();
  // variables to refect the current settings
  // of the visualization
  var  layout = "force";



  // our force directed layout
  var  force = d3.layout.force()
      .friction(0.9)
      .charge([-50])
      .size([width, height]);
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
  force.on("end",function(){console.log("Over");});



  function update(){
    //  filter data to show based on current filter settings.
    curNodesData = allData.nodes;
    curLinksData = allData.links;


    // reset nodes and links in force layout
    force.nodes(curNodesData)
    .links(curLinksData)
    .linkDistance(function(d){

      return d.target.linkPower;
    });
    // enter / exit for nodes
    updateNodes();
    updateLinks();

    console.log(force.nodes().length);
    // start me up!
    force.start();
  }


  // enter/exit display for nodes
  function updateNodes(){
    node = nodesG.selectAll("circle.node")
      .data(curNodesData, function(d) { return d.name ;});


    node
      .attr("attr","update")
      .attr("cx", function(d){ return d.x; })
      .attr("cy", function(d){ return d.y; })
      .transition()
        .duration(10000)
        .attr("r",function(d){
          return d.radius;
        });

    node.enter().append("circle")
      .attr("class", "node")
      .attr("cx", function(d){ return d.x; })
      .attr("cy", function(d){ return d.y; })
      .attr("r", function(d){ return d.radius})
      .style("fill", function(d,i){ return d.kind ==="Router"?colors(0):colors(1) })
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
      .data(curLinksData, function(d){ return (d.source.name + " : "+d.target.name) });

    link
      .attr("attr","update")
      .attr("x1", function(d){ return d.source.x;})
      .attr("y1", function(d){ return d.source.y;})
      .attr("x2", function(d){ return d.target.x;})
      .attr("y2", function(d){ return d.target.y;});

    link.enter().append("line")
      .attr("class", "link")
      .attr("stroke", "#ddd")
      .attr("stroke-width", function(d){return scale2(-d.power);})
      .attr("x1", function(d){ return d.source.x;})
      .attr("y1", function(d){ return d.source.y;})
      .attr("x2", function(d){ return d.target.x;})
      .attr("y2", function(d){ return d.target.y;})

    link.exit().remove()
  }
  network.toggleLayout = function(newLayout){
    // # public function

  }

  network.updateData = function(newData){
      force.stop();
      allData = setupData(newData)
      link.remove()
      node.remove()
      update()
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

  // called once to clean up raw data and switch links to
  // point to node instances
  // Returns modified data
  setupData = function(data){
    // initialize circle radius scale
    data.links = new Array();
    data.nodes = new Array();
    data.nodes.push({'name' : "Listener", 'power': -10, 'kind': "Listener"});
    for (var i = 0; i < data.length; i++) {

      var node = JSON.parse(data[i])

      var n = {'name' : $.trim(node.BSSID), 'power': node.power, 'kind': node.kind};
      if(n.kind == "Client"){
        n.probedESSID = node.probedESSID;
      }
      var l = {'source' : data.nodes[0].name, 'target': $.trim(node.BSSID), 'power':node.power};
      data.nodes.push(n);
      data.links.push(l);

    }
    countExtent = d3.extent(data.nodes, function(d){ return d.power;});
    circleRadius = d3.scale.pow().range([3, 9]).domain(countExtent);
    linkRadius = d3.scale.pow().range([500, 30]).domain(countExtent);

    data.nodes.forEach( function(n){
      // set initial x/y to values within the width/height
      // of the visualization
      if(nodesMap.has(n.name)){
          _n = nodesMap.get(n.name);
          n.x = _n.x;
          n.y = _n.y;
          n.px = _n.px;
          n.py = _n.py;
      }
      else{
        n.x = randomnumber=Math.floor(Math.random()*width);
        n.y = randomnumber=Math.floor(Math.random()*height);
      }


      // add radius to the node so we can use it later
      n.radius = circleRadius(n.power);
      console.log(n.radius);
      n.linkPower = linkRadius(n.power)
    });

    // id's -> node objects
    nodesMap  = mapNodes(data.nodes);

    data.links.forEach( function(l){
      l.source = nodesMap.get(l.source);
      l.target = nodesMap.get(l.target);
      // linkedByIndex is used for link sorting
      linkedByIndex[l.source.name + " : "+l.target.name] = 1;
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
