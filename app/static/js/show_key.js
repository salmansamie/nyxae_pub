
$('button#ret_action').click(function(){
    $.ajax({
        url: "/_get_data/",
        type: "POST",
        async: false,
        success: [
                function(resp){
            $('div#response').append(resp)
        }
        ]
    });
});
