/* global createCanvas, colorMode, strokeWeight, background, rect, stroke, fill,
HSB, mouseX, mouseY, brushHue, prevX, prevY, mouseIsPressed, brushWeight, line, 
random, pmouseX, pmouseY, keyCode, color, ellipse, width, height, textAlign,
loadImage, rectMode, text, image, CENTER, circle, noStroke
*/

// prints "hi" in the browser's dev tools console
console.log("hi");


let images;

let inn = 1;
let deltaInn = 0.1;
let deltaDeltaInn = 0.01;

let boardDimen;
let lineDist;
let tokenRadius;
let can;
let blackTurn;
function setup()
{
  blackTurn = true;
  boardDimen = 600;//min(windowWidth, windowHeight);
  lineDist = boardDimen/8;
  tokenRadius = boardDimen/20;
  can = createCanvas(boardDimen, boardDimen);
  //can.position(windowWidth/2, windowHeight/2, 'fixed');
  colorMode(HSB, 360, 80, 80);
  background(140, 216, 50);
  drawStart();
  /*document.getElementById("clear").onclick = function(){ //when the button is clicked
    flip(3, 3); //clean the canvas
  }*/
}

function draw()
{
    /*if(inn > 40 || inn < 1)
    {
      deltaInn = -deltaInn;
      deltaDeltaInn -= deltaDeltaInn;
    }

    if(deltaInn > 0)
    {
      drawBoard();
      x = boardToCoord(3);
      y = boardToCoord(3);
      fill(0);
      noStroke();
      ellipse(x+2, y+2, tokenRadius/inn, tokenRadius);
      strokeWeight(2/inn);
      fill(255);
      stroke(0);
      ellipse(x, y, tokenRadius/inn, tokenRadius);
    }
    else
    {
      drawBoard();
      x = boardToCoord(3);
      y = boardToCoord(3);
      fill(255);
      noStroke();
      ellipse(x+2, y+2, tokenRadius/inn, tokenRadius);
      strokeWeight(2/inn);
      fill(0);
      stroke(255);
      ellipse(x, y, tokenRadius/inn, tokenRadius);
    } 
    inn += deltaInn;
    deltaInn += deltaDeltaInn;
    console.log(inn);
    console.log(deltaInn);
    circle (400, 400, 20);*/

  //}
  /*for(i = 5; i <= 1; i-=0.02)
  {
    drawBoard();
    x = boardToCoord(3);
    y = boardToCoord(3);
    fill(0);
    noStroke();
    ellipse(x+2, y+2, tokenRadius/i, tokenRadius);
    strokeWeight(1);
    fill(255);
    stroke(0);
    ellipse(x, y, i, tokenRadius);
  }*/
}

function mousePressed()
{
  let boardX = coordToBoard(mouseX);
  let boardY = coordToBoard(mouseY);
  if(blackTurn)
      drawBlack(boardX, boardY);
  else
      drawWhite(boardX, boardY);
  blackTurn = !blackTurn;


  var server = "http://127.0.0.1:5000";
  var dataToSend = {'move':[0, 0]};

    $(function() {
      var appdir='/move';
      var send_msg = "Mouse was clicked";
      var received_msg = "<p>Result returned</p>";
      dataToSend['move'] = [boardX, boardY];
      console.log(send_msg);
      //document.getElementById('message').html(send_msg);
      $.ajax({
          type: "POST",
          url:server+appdir,
          data: JSON.stringify(dataToSend),
          dataType: 'json'
      }).done(function(data) { 
        console.log(data);
        //document.getElementById('n3').val(data['sum']);
        //document.getElementById('message').html(received_msg+data['msg']);
      });
    });

}

function drawBoard()
{
  background(140, 216, 50);
  strokeWeight(4);
  stroke(255);
  var i;
  for (i = 1; i < 8; i++)
  {
      line(i*lineDist, 0, i*lineDist, boardDimen);
      line(0, i*lineDist, boardDimen, i*lineDist);
  }
}

function drawBlack(x, y)
{
  x = boardToCoord(x);
  y = boardToCoord(y);
  fill(255);
  noStroke();
  circle(x+2, y+2, tokenRadius);
  strokeWeight(1);
  fill(0);
  stroke(255);
  circle(x, y, tokenRadius);
}

function drawWhite(x, y)
{
  x = boardToCoord(x);
  y = boardToCoord(y);
  fill(0);
  noStroke();
  circle(x+2, y+2, tokenRadius);
  strokeWeight(1);
  fill(255);
  stroke(0);
  circle(x, y, tokenRadius);
}

function drawStart()
{
  drawBoard();
  drawWhite(3, 3);
  drawBlack(4, 3);
  drawWhite(4, 4);
  drawBlack(3, 4);
}

function boardToCoord(c) //returns [0, boardDimen) canvas coordinate based on 
{
  return lineDist * c + (lineDist/2);
}

function coordToBoard(b) //returns [0, 8) board coordinate based on [0, boardDimen) canvas coordinate
{
  return round((b - (lineDist/2)) / lineDist);
}

function flip(x, y) //flip coin animation
{

}