String.prototype.isEmpty = function() 
{
      return (this.length === 0 || !this.trim());
};

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

//User registration actions 
function login_user()
{

    var user_name = $('#user_name').val();
    var user_password = $('#user_password').val();



    if(user_name.isEmpty())
    {
      toastr.error("Invalid form data","User login field cannot be empty");
      return;
    }

    if(user_password.isEmpty())
    {
      toastr.error("Invalid form data","Password field cannot be empty");
      return;
    }
    else
    {

      var form_data = {};

      form_data['user_password'] = user_password;
      form_data['user_name'] = user_name;

      jQuery.ajax({
            type: 'POST',               
            data: form_data,
            url: "/login",
            dataType : 'json',  
            success : function(data)
            {
              data = data['results'];
              var success = parseInt(data['success']);
              
              if(success)
              {
                 window.location.href = '/home';
              }
              else
              {
                var messages = data['message'];
                $.each(messages,function(index,message) 
                {
                  toastr.error("Invalid form data",message);
                });
                
              }
            
            }
           
        });



    }
      
}






function register_user()
    {

    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    var first_name = $('#first_name').val();
    
    var last_name =  $('#last_name').val();
    
    var user_email =  $('#user_email').val();
        
    var user_name = $('#user_name').val();
    
    var user_password = $('#user_password').val();

    var password_confirm  = $('#confirm_password').val();
  

    if(first_name.isEmpty())
    {
      toastr.error("Invalid form data","First Name field can't be empty");
      return;
    }

    if(user_email.isEmpty())
    {
      toastr.error("Invalid form data","Email field can't be empty");
      return;
    }

    if(!re.test(user_email))
    {
      toastr.error("Invalid form data","Please enter a valid Email");
      return;
    }
    
    if(user_name.isEmpty())
    {
      toastr.error("Invalid form data","User login field cannot be empty");
      return;
    }

    if(user_password.isEmpty())
    {
      toastr.error("Invalid form data","Password field cannot be empty");
      return;
    }

    if(user_password !== password_confirm)
    {
      toastr.error("Invalid form data","Passwords dont match");
      return;
    }
  
    else
    {

      var form_data = {};

      form_data['first_name'] = first_name;
      form_data['user_email'] = user_email;
      form_data['user_password'] = user_password;
      form_data['user_name'] = user_name;

      if(last_name)
      {
        form_data['last_name'] = last_name;
      }
      
  
       jQuery.ajax({
            type: 'POST',               
            data: form_data,
            url: "/register",
            dataType : 'json',  
        success: function(data)
            {
              data = data['results'];
              var success = parseInt(data['success']);

              if(success)
              {
                 toastr.success('Success',data['message']);
                 window.location.href='/home';
              }
              else
              {
                var messages = data['message'];
                $.each(messages,function(index,message) 
                {
                  toastr.error("Invalid form data",message);
                });
                
              }
            
            }
           
        });


    }


    }


$(document).ready(function(){ 

        
      $(document).on('click','#add',add_option);  

      $(document).on('click', '#btn_remove',remove_option);

      $('#add-more-question').click(submit_data);

      $('#submit').click(submit_data); 

      // user registration
      $('#register-button').click(register_user);

      $('#login-button').click(login_user);

 });  

