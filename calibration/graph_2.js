Network = function(){
  // variables we want to access
  // in multiple places of Network
  var  width = app.width;
  var  height = app.height;
  //  allData will store the unfiltered data
  var allData = []
  var allRawData = [];
  var  curLinksData = [];
  var  curNodesData = [];
  var  linkedByIndex = {};
  // these will hold the svg groups fora
  // accessing the nodes and links display
  var  nodesG = null;
  var  linksG = null;
  // these will point to the circles and lines
  // of the nodes and links
  var  node = "Power";
  var  link = "Distance";

  var nodesMap = d3.map();
  var routersMap = d3.map();
  var clientsMap = d3.map();
  var ramp = d3.map();

  // variables to refect the current settings
  // of the visualization
  var  nodeColor = null;
  var layout = null;
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
    setNodeColor("Type");
    setLayout("Distance");

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

    linksG = vis.append("g").attr("id", "links");
    nodesG = vis.append("g").attr("id", "nodes");

    force.size([width, height]);

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

    if(layout == "Distance"){
      force
        .friction(.65)
        .charge([-200])
        .size([width, height]);
    }
    else if (layout == "Connections"){
      force
        .friction(.6)
        .charge([-150])
        .size([width, height]);
    }

    force.start();
  }

  function updateNodes(){
    node = nodesG.selectAll("circle.node")
      .data(curNodesData, function(d) { return d.name ;});

    node
      .attr("attr","update")
      .transition()
      .duration(1000)
      .attr("class","node")
      .style("fill",function(d){return d.color;})
      .attr("r",function(d){return d.radius;});

    node.enter().append("circle")
      .attr("class", "node")
      .attr("cx", function(d){ return d.x; })
      .attr("cy", function(d){ return d.y; })
      .attr("r", function(d){ return d.radius})
      .style("fill",function(d){return d.color;})
      .call(force.drag);

    node.on("mouseover", showDetails)
      .on("mouseout", hideDetails)

    node.exit().remove();
  }

  function updateLinks(){
    link = linksG.selectAll("line.link")
      .data(curLinksData, function(d){ return (d.source.name + " : "+d.target.name) });

    link
      .attr("attr","update")
      .attr("class", "link");

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

  setNodeColor = function(newColor){
    nodeColor = newColor;
  }

  setLayout = function(newLayout){
    layout = newLayout;
  }

  network.toggleNodeColor = function(newColor){
    // # public function
    force.stop()
    setNodeColor(newColor);
    allData = setupData(allRawData);
    update();
  }

  network.toggleLayout = function(newLayout){
    force.stop()
    setLayout(newLayout);
    allData = setupData(allRawData);
    update();
  }

  network.updateData = function(newData){
      allRawData = newData;
      allData = setupData(newData);
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
  setupData = function(_data){

    data = new Object();
    data.links = new Array();
    data.nodes = new Array();

    data.nodes.push({'name' : "Listener", 'power': -10, 'kind': "Listener"});
    for (var i = 0; i < _data.length; i++) {

      var node = JSON.parse(_data[i]);
      var n = {'name' : $.trim(node.BSSID), 'power': node.power, 'kind': node.kind};

      if(n.kind == "Client"){
        n.essid = node.AP;
        n.probedESSID = node.probedESSID;

        if(layout=="Distance"){
            var l = {'source' : data.nodes[0].name, 'target': $.trim(node.BSSID), 'power':node.power};
            data.links.push(l);
        }
        else if(layout = "Connections"){

          var AP = n.essid.split("|");
          var networkName = $.trim(AP[0]);

          if(networkName === "(not associated)" || networkName === ""){
            // console.log(networkName);
          }
          else{

            // console.log(networkName);
            // networkName ="AP: "+ nodesMap.get($.trim(AP[0])).essid
            var l = {'source' : networkName, 'target': $.trim(node.BSSID), 'power':node.power};
            data.links.push(l);

          }
        }
      }
      else{

        if(layout=="Distance"){
            var l = {'source' : data.nodes[0].name, 'target': $.trim(node.BSSID), 'power':node.power};
            data.links.push(l);
        }
        n.essid =  node.ESSID;
      }
      data.nodes.push(n);
    }
    return refreshD3Data(data);
  }

  refreshD3Data = function(data){

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

      countExtent = d3.extent(data.nodes, function(d){ return d.power;});

      if(layout === "Distance"){
        linkRadius = d3.scale.pow().range([300, 30]).domain(countExtent);
        circleRadius = d3.scale.pow().range([ 5,10]).domain(countExtent);

        n.radius = circleRadius(n.power);
        n.linkPower = linkRadius(n.power);
      }

      else if(layout === "Connections" ){
        linkRadius = d3.scale.pow().range([10, 30]).domain(countExtent);
        circleRadius = function(d){
          if(d.kind === "Router"){ return 7;}
          else if(d.kind === "Listener"){ return 5;}
          else{return 3;}

        }
        // n.linkPower = 10;
        n.linkPower = linkRadius(n.power);
        n.radius = circleRadius(n);
      }

      if(nodeColor ==="Power"){

        ramp = d3.scale.pow().domain(countExtent).range(["#8dbbd8","#acbc43"]);
        n.color = ramp(n.power);
      }
      else {
        ramp = function(d){
          if(d.kind === "Router"){ return "#4c92c1";}
          else if(d.kind === "Listener"){ return "White";}
          else{return "#bb7646";}
        }

        n.color = ramp(n);
      }
    });

    // id's -> node objects
    mapNodes(data.nodes);

    data.links.forEach( function(l){
      // console.log(l.source + " : "+l.target);
      if(nodesMap.has(l.source) && nodesMap.has(l.target)){
        l.source = nodesMap.get(l.source);
        l.target = nodesMap.get(l.target);
        linkedByIndex[l.source.name + " : " +l.target.name] = 1;
      }
      else{
        delete data.links[l];
        console.log("here");
      }




      if(l.source === null || l.target ===null){

        // l.remove();
        // l =null;
        // linkedByIndex["error" + " : "+"error"] = 1;
      }
      else{


      }

    });

    return data;
  }

  // Helper function to map node id's to node objects.
  // Returns d3.map of ids -> nodes
  mapNodes = function(nodes){
    nodesMap = d3.map();
    nodes.forEach (function(n,i){

      if(typeof(nodesMap.get(n.name)) !=="undefined"){
      }
      else{
        nodesMap.set(n.name, n);
      }

    });
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
        if(typeof(nodesMap.get($.trim(AP[0])).essid) !=="undefined"){
          // networkName ="AP: "+ nodesMap.get($.trim(AP[0])).essid;
        }
        else{
          networkName ="AP: "+ "Error";
        }
        // if(nodesMap.get($.trim(AP[0])).essid== "Happy House"){console.log(d);}
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
  }

    return network
  }
