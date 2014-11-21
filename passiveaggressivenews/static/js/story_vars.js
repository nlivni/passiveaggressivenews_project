/**
 * Created by nlivni on 11/14/2014.
 */

$(function() {

    function update_preview() {
        var title = document.getElementById("id_title").value;
//        var template = document.getElementById("id_template").value;
        var template = CKEDITOR.instances['id_template'].getData();
        var preview = document.getElementById("preview");
        var var_fields = $(".var-field");
        var var_array = [];

        for (i = 0; i < var_fields.length; i++) {
            var_array.push(var_fields[i].value);
        }

        //console.log(var_array);

        for (i=0; i < var_array.length; i++) {
            var v = var_array[i];
            var v_div = "<mark>" + v + "</mark>";
            template = template.replace(/%s/i, v_div);
        }
        //console.log(template);
        preview.innerHTML = "<h2>" + title + "</h2>" + template;
        console.log("update_preview")
    };
//    @todo id_#template is for textarea not ckeditor. needs to be changed for update to work. seems to work when variables are updated though....
//    $('#id_template').change(update_preview);
    CKEDITOR.instances['id_template'].on('change', update_preview);
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
            if (var_fields[i].value.search("'")) {
                var_fields[i].value = var_fields[i].value.replace("'","&#x27");
            }

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
    $(document).on('change','.var-field',story_harvest);


 //-------------------------------new junk (remove variable) ------sb 11/17/14----------------//
    //when user clicks on anything within the div with id = "var_fields" and with a class of "remove_var" it will trigger this function
    $("#var_fields").on("click", ".remove_var", function(event){
     //  get the index number of the variable that has been clicked on.
      var array_index = $(this).attr("data-var");
      //call the function and pass the array_index value needed to take this variable out of the textarea we are using to submit the "array" of variables
      removeFromVarList(array_index);
    //remove the input and any children elements of the input field
$(this).parent().parent().remove();
        //update view
        story_harvest();
        update_preview();
      });
    //this function modifies the list of variables that will be submitted to match the list that exists in the input fields above.  var_to_remove is just text, not an object.
    function removeFromVarList( array_index)
    {
        //get the existing string with #id-variables
 var variables_string = $("#id_variables").val();
        //remove containing brackets
 variables_string=variables_string.replace("['","")
 variables_string=variables_string.replace("']","")
        //split string into an array object
 var variables_array = variables_string.split(/','/);
        //remove the item in the array with the index number passed into this function
variables_array.splice(array_index, 1);
        //loop through array and add single quotes before and after
        for(i=0;i<variables_array.length;i++)
        {
        variables_array[i] = "'"+ variables_array[i] +"'";
        }

        //convert array back to a string
var updated_text = variables_array.toString();
        //put containing brackets back
updated_text = "[" + updated_text + "]";
        //assign value of #id_variables to updated string
        $("#id_variables").val(updated_text);
        //update the preview


    }

  //-------------------------------end new junk----------------------//




    $(add_var_btn).click(function() {

        // define last field
        var last_field = $( "#var_fields .form-group" ).last();

        // get count of fields
        var field_count = $('.var_input').length;

        // insert new field after last field
        $(last_field).after('<div class="var_input form-group"><div class="input-group"><input class="form-control var-field" id="var-field-'+ field_count + '" type="text" value=""><span class="input-group-btn"><button data-var="'+ field_count + '" class ="remove_var btn btn-default" ><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></div></div>');

        // get new field count
        var field_count = $('.var_input').length;

        // print field count (for validation)
        console.log("field count: " + field_count);
        //$(".var-field").trigger("keyup");

    });

    //story_harvest();
    //console.log("harvest called");


//    @todo: thought about escaping on submit rather than before. see below:
//    function escape_submit() {
//        submit_val =  $('#submit-id-submit').val();
//        $('#id_template').val(htmlEscape($('#id_template').value))
//        $('#id_variables').val(htmlEscape($('#id_variables').value))
//
//    }

    $('#submit-id-submit').click( {

    }
    )

});