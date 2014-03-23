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
  var ramp = d3.map();

  // variables to refect the current settings
  // of the visualization
  var  layout = "force";
  var tooltip = Tooltip("vis-tooltip", 230)

  var  force = d3.layout.force()
      .friction(.65)
      .charge([-200])
      .size([width, height]);

      force.on("tick", forceTick);
      force.on("end",function(){console.log("Over");});

// color function used to color nodes
  var nodeColors = d3.scale.category20();

  function network(selection, data){
    setLayout("Power");

    // format data
    allData = setupData(data)

    // create svg and groups
    vis = d3.select(selection).append("svg")
      .attr("width", width)
      .attr("height", height);
    vis.append("rect")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("fill", "black");
console.log(vis);
    linksG = vis.append("g").attr("id", "links");
    nodesG = vis.append("g").attr("id", "nodes");

    force.size([width, height]);


    // setFilter("all")

    // perform rendering and start force layout
    update();
  }

  function update(){
    //  filter data to show based on current filter settings.
    curNodesData = allData.nodes;
    curLinksData = allData.links;


    // reset nodes and links in force layout
    force.nodes(curNodesData)
    .links(curLinksData)
    .linkDistance(function(d){ return d.target.linkPower; });


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

    // node
    //   .attr("attr","update")
    //   .transition()
    //     .attr("cx", function(d){ return (d.kind==="Listener"?app.width/2:d.x); })
    //     .attr("cy", function(d){ return (d.kind==="Listener"?app.height/2:d.y); });

    node.enter().append("circle")
      .attr("class", "node")
      .attr("cx", function(d){ return d.x; })
      .attr("cy", function(d){ return d.y; })
      // .attr("stroke-width","0.4")
      // .attr("stroke","white")
      .attr("r", function(d){ return d.radius})
      .style("fill",function(d){return d.color;})// function(d,i){ return d.kind ==="Router"?colors(0):colors(1) })
      .call(force.drag);
      // .style("stroke", function(d){ return strokeFor(d); })
      // .style("stroke-width", 1.0)

    node.on("mouseover", showDetails)
      .on("mouseout", hideDetails)

    node.exit().remove();
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
      // .attr("stroke-width", 2)
      // .attr("stroke", "black");

    link.enter().append("line")
      .attr("class", "link")
      .style("stroke-width","0.3")
      .style("stroke",function(d){return (d.target.kind ==="Router"?"White":"Grey")})
      .attr("stroke-dasharray",function(d){return d.target.kind ==="Router"?"10":"35"})
      .attr("x1", function(d){ return d.source.x;})
      .attr("y1", function(d){ return d.source.y;})
      .attr("x2", function(d){ return d.target.x;})
      .attr("y2", function(d){ return d.target.y;});

    link.exit().remove();
  }
  network.toggleLayout = function(newLayout){
    // # public function
    force.stop()
    setLayout(newLayout)
    setupData(allData);
    update()
  }

  setLayout = function(newLayout){
    layout = newLayout;
  }


  network.updateData = function(newData){
      // force.stop();
      allData = setupData(newData);
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
        n.essid = node.AP;
        n.probedESSID = node.probedESSID;
        // console.log(node.probedESSID);
      }
      else{
        n.essid =  node.ESSID;
      }
      var l = {'source' : data.nodes[0].name, 'target': $.trim(node.BSSID), 'power':node.power};
      data.nodes.push(n);
      data.links.push(l);

    }

    countExtent = d3.extent(data.nodes, function(d){ return d.power;});
    circleRadius = d3.scale.pow().range([3, 13]).domain(countExtent);
    linkRadius = d3.scale.pow().range([300, 30]).domain(countExtent);

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


      if(layout =="Power"){
        ramp = d3.scale.pow().domain(countExtent).range(["#8dbbd8","#acbc43"]);
        n.color = ramp(n.power);
      }
      else {
        ramp = function(d){
          if(d.kind == "Router"){ return "#7241a7";}
          else if(d.kind == "Listener"){ return "White";}
          else{return "#b34244";}
        }

        n.color = ramp(n);
      }
      // add radius to the node so we can use it later
      n.radius = circleRadius(n.power);
      n.linkPower = linkRadius(n.power);;

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
    nodes.forEach (function(n){ nodesMap.set(n.name, n);});
    return nodesMap;
  }

  showDetails = function (d,i){
    content = '<p class="main">' + d.kind.toUpperCase() + " : "+ d.name + '</span></p>';
    content += '<hr class="tooltip-hr">';
    if(d.kind == "Client"){

      var AP = d.essid.split("|");
      //contains
      var networkName = $.trim(AP[0]);
      if(networkName === "(not associated)"){
        networkName =  "AP: "+"unassociated";
      }
      else{
        networkName ="AP: "+ nodesMap.get($.trim(AP[0])).essid;
      }
      content += '<p class="main">' + networkName    + '</span></p>';
      content += '<hr class="tooltip-hr">';
      content += '<p class="main">' +"RSSI: " + d.power  + '</span></p>';

      if(d.probedESSID.length > 0){
        content += '<hr class="tooltip-hr">';
        content += '<p class="main">' + "PROBED NETWORKS:"  + '</span></p>';
        d.probedESSID.forEach(function(n){

          content += '<p class="main">' + n  + '</span></p>';
        });
      }
    }
    else{
      content += '<p class="main">' + "NAME:" + d.essid  + '</span></p>';
      content += '<hr class="tooltip-hr">';
      content += '<p class="main">' +"RSSI: " + d.power  + '</span></p>';
    }

    tooltip.showTooltip(content,d3.event);
  }


  hideDetails = function(d,i){
    tooltip.hideTooltip();
    // # watch out - don't mess with node if search is currently matching
    // node.style("stroke", (n) -> if !n.searched then strokeFor(n) else "#555")
      // .style("stroke-width", (n) -> if !n.searched then 1.0 else 2.0)
    // if link
      // link.attr("stroke", "#ddd")
        // .attr("stroke-opacity", 0.8)
  }

    return network
  }
