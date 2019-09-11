function myFunction(){

    var checkedCheckboxes = [];

    $('button').click(function(){
        $('input').each(function(){
            if ($(this).is(':checked')) {
                checkedCheckboxes.push($(this).val())  
            }
        });
        var a = checkedCheckboxes[0]

        $.ajax({
            type: "GET",
            data: ({a}),
            dataType: 'json',
            url: "http://127.0.0.1:8000/blacklist/",
            success: function(data){
                alert("Hi I am former "+data.name);
            }
        });
    // Now we have an array
    //console.log('JS Array: ');
    console.log(checkedCheckboxes);

    //console.log(checkedCheckBoxes[0]);
    

    // Convert array to standard Javascript Object Literal
   // var checkedCheckboxesObject = $.extend({}, checkedCheckboxes);
   // console.log('JS Object: ');
   // console.log(checkedCheckboxesObject);
//
   // // Convert Object Literal to JSON
   // var checkedCheckboxesJSON = JSON.stringify(checkedCheckboxesObject);
   // console.log('JSON: ');
   // console.log(checkedCheckboxesJSON);

    });
};
