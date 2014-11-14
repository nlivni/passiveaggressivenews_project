/**
 * Created by nlivni on 11/13/2014.
 */

$(document).ready(function create_preview(){
        var title = document.getElementById("id_title").value;
        var template = document.getElementById("id_template").value;
        var preview = document.getElementById("preview");

        preview.innerHTML = "<h2>" + title + "</h2>" + "<p>" + template + "</p>";

    }
);

$(document).keyup(function update_preview(){
        var template = document.getElementById("id_template").value;
        var preview = document.getElementById("preview");
        preview.innerHTML = "<p>" + template + "</p>";
    }
);