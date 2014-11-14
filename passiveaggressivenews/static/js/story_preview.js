/**
 * Created by nlivni on 11/13/2014.
 */


$(document).keyup(
function updateLoop(){
var storytext = document.getElementById("story-text").value;
var preview = document.getElementById("preview");
preview.innerHTML = "<p>" + storytext + "</p>";
preview.style.display = "block";
}
)
  //  onKeyPress = updateLoop();
