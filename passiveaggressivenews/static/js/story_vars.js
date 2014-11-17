/**
 * Created by nlivni on 11/14/2014.
 */

$(function() {

    function update_preview() {
        var title = document.getElementById("id_title").value;
        var template = document.getElementById("id_template").value;
        var preview = document.getElementById("preview");
        var var_fields = $(".var-field");
        var var_array = [];

        for (i = 0; i < var_fields.length; i++) {
            var_array.push(var_fields[i].value);
        }

        //console.log(var_array);

        for (i=0; i < var_array.length; i++) {
            var v = var_array[i];
            template = template.replace(/%s/i, v);
        }
        //console.log(template);
        preview.innerHTML = "<h2>" + title + "</h2>" + "<p>" + template + "</p>";
        console.log("update_preview")
    };

    $('#id_template').change(update_preview);
    $(document).keyup(update_preview);
    $(document).ready(update_preview);

    var add_var_btn = document.getElementById("add_var_btn");

    function story_harvest() {


        //get an array containing the var_field inputs
        var var_fields = $(".var-field");

        var var_list = "[";
        // add values from var_fields array to a list string
        for (i = 0; i < var_fields.length; i++) {
            if (i) var_list += ",";
            //escape apostrophes to avoid malformed list
            // @todo - currently looks ugly in var_field, fix to make conversation too and from var_field
            var_fields[i].value = var_fields[i].value.replace("'","&#x27");
            var_list += "'" + var_fields[i].value + "'";
        }
        // test to make sure there's variables, otherwise the extra comma will throw python error
        if (var_list === "[,") {
            var_list = "[]"
        }
        else {
            var_list += "]";
        }
        // update bound variables field
        var variables = $("#id_variables");
        variables.val(var_list);


        // print what you did
        console.log("story_harvest ");
    }

    $(document).ready(story_harvest);
    $(document).on('keyup','.var-field',story_harvest);

    $(add_var_btn).click(function() {

        // define last field
        var last_field = $( "#var_fields .form-group" ).last();

        // get count of fields
        var field_count = $('.var_input').length;

        // insert new field after last field
        $(last_field).after('<div class="var_input form-group"><input class="form-control var-field" id="varfield-'+ field_count + '" type="text" value=""></div>');

        // get new field count
        var field_count = $('.var_input').length;

        // print field count (for validation)
        console.log("field count: " + field_count);
        //$(".var-field").trigger("keyup");

    });

    //story_harvest();
    //console.log("harvest called");

    function escape_submit() {
        submit_val =  $('#submit-id-submit').val();
        $('#id_template').val(htmlEscape($('#id_template').value))
        $('#id_variables').val(htmlEscape($('#id_variables').value))

    }

    $('#submit-id-submit').click( {

    }
    )

});