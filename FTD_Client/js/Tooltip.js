function Tooltip(tooltipId, width){
  var tooltipId = tooltipId;
  $("body").append("<div class='tooltip' id='"+tooltipId+"'></div>");

  if(width){
    $("#"+tooltipId).css("width", width);
  }
  // $("#closebtn").on("click", function(e){
  //   e.preventDefault();
  //   console.log("closing ");
  //   // myNetwork.attachButtonListener();
  //   closeSidepage();
  // })
  hideTooltip();

  function showTooltip(content, event) {

    $("#closebtn").empty();

    $("#playerInfo").html(content);
    // $("#closebtn").unbind("click",clickFunc);
    // $(this).addClass("open");
    openSidepage();

    $("#closebtn").on("click", clickFunc);
  }

  function clickFunc(e){
    e.preventDefault();
    console.log("closing ");
    closeSidepage();
    //  $( this ).unbind( e );
  }

  function hideTooltip(){
    $("#"+tooltipId).hide();
  }
  function openSidepage() {
    console.log("here");
   $('#main').animate({
    left: '18%'
  }, 400, 'easeOutSine');
  }
  function closeSidepage(){
    // $("#navigation li a").removeClass("open");
    console.log("Close sidepage");
    $('#main').animate({
    left: '0px'
  }, 400, 'easeOutSine'
    );
  }



  function updatePosition(event){
    var ttid = "#"+tooltipId;
    var xOffset = 20;
    var yOffset = 10;

    var toolTipW = $(ttid).width();
    var toolTipeH = $(ttid).height();
    var windowY = $(window).scrollTop();
    var windowX = $(window).scrollLeft();
    var curX = event.pageX;
    var curY = event.pageY;
    var ttleft = ((curX) < $(window).width() / 2) ? curX - toolTipW - xOffset*2 : curX + xOffset;
    if (ttleft < windowX + xOffset){
      ttleft = windowX + xOffset;
    }
    var tttop = ((curY - windowY + yOffset*2 + toolTipeH) > $(window).height()) ? curY - toolTipeH - yOffset*2 : curY + yOffset;
    if (tttop < windowY + yOffset){
      tttop = curY + yOffset;
    }
    $(ttid).css('top', tttop + 'px').css('left', ttleft + 'px');
  }

  return {
    showTooltip: showTooltip,
    hideTooltip: hideTooltip,
    updatePosition: updatePosition
  }
}
