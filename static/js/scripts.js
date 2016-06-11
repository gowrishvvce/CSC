function reset_form_data()
{
  $('#question').val('');

  $(".option-item").each(function(index) 
    {
      $(this).find(".option").val('');
      
   });

}

function submit_data()
{

    var question = $('#question').val();
    var options = [];

    $(".option-item").each(function(index) 
    {
      var option = $(this).find(".option").val();
      options.push(option); 
    });

    if(!question.length)
    {
      toastr.error("Invalid form data","Please enter a question");
      return;
    }

    if(options.length < 4)
    {
      toastr.error("Invalid form data","Please enter atleast upto four options");
      return;
    }

    else
    {

        var form_data = {'question' : question,'options' : JSON.stringify(options)};

        $.ajax({  
          url:"/save_options",  
          method:"POST",  
          data:form_data,  
          success:function(data)  
          {  
            var status = data['results']['success'];
            if(status)
            {
             toastr.success("Success","Your options have been successfully recorded");   
             reset_form_data();
            }
           
          }  
        });  

      
    }



}


function add_option()
{

  var item_number = $('.option-item').length;
  item_number += 1;
  if(item_number < 10)
  {
    $(this).closest('#dynamic_field').append('<tr class="option-item" id="row'+item_number+'"><td><input type="text" name="name[]" placeholder="Enter the option" class="form-control option" /></td><td><button type="button" name="remove" id="'+item_number+'" id="btn_remove" class="btn btn-danger">X</button></td></tr>');  
  }
  
}

function remove_option()
{

  var button_id = $(this).attr("id");   
  $(this).closest('#dynamic_field').find('#row'+button_id+'').remove();  

}

$(document).ready(function(){ 

        
      $(document).on('click','#add',add_option);  

      $(document).on('click', '#btn_remove',remove_option);

      $('#add-more-question').click(submit_data);

      $('#submit').click(submit_data); 

 });  

