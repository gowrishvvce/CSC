function submit_data(form_data)
{

       $.ajax({  
                url:"/save_options",  
                method:"POST",  
                data:form_data,  
                success:function(data)  
                {  
                     alert(data);  
                     $('.add_name')[0].reset();  
                }  
           });  

}


function add_option()
{



}

function remove_option()
{


}




$(document).ready(function(){ 

      var i=1;  
     
      $(document).on('click','#add',function()
      {  
           i++;  
           $(this).closest('#dynamic_field').append('<tr id="row'+i+'"><td><input type="text" name="name[]" placeholder="Enter your Name" class="form-control name_list" /></td><td><button type="button" name="remove" id="'+i+'" class="btn btn-danger btn_remove">X</button></td></tr>');  
      });  

      $(document).on('click', '.btn_remove', function(){  
           var button_id = $(this).attr("id");   
           $(this).closest('#dynamic_field').find('#row'+button_id+'').remove();  
      });

      $(document).on('click','#add-more-question',function(){

        $('.add_name').submit();

        });

      $('.add_name').submit(function()
      {            

            var form_data = $(this).serialize();
            console.log(form_data);

            return false;
    
      });  
 });  

