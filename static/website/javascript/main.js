$(document).ready(function () {

//    This Function Prevents more than 5 toppings from being selected
    $('input.topping-checkbox').on('change', function(evt) {
        var limit = 5;
        if($(this).siblings(':checked').length >= limit) {
            this.checked = false;
            alert('You can only choose up to 5 toppings ')
        }
    });

    // Function that runs whenever option is changed to get price
    $(".sub").change(function(){
        // Checks if pizza size is selected
        if ($("input.pizza_size:checked").length > 0) {
            // checks if pizza type is selected
            if ($("input.pizza_type:checked").length > 0) {
                // Gets the selected options
                var pizza_size = document.querySelector('input[name="pizza_size"]:checked').value;
                var pizza_type = document.querySelector('input[name="pizza_type"]:checked').value;
                var topping_count= $('input[name="topping"]:checked').length + 1;
                // Sends an ajax request for data from the server
                $.ajax({
                    url: "pizza_price",
                    data: {
                        'pizza_size':pizza_size,
                        'pizza_type':pizza_type,
                        'topping_count':topping_count
                    },
                    dataType: "json",
                    success: function (data) {
                        // When a succesful response has been received, set the text of h1 = to response
                        $("#pizza_price").text('$' + data.price);
                    }
                });

                
            }
        }
    });
    $(function() {

        $('.cc-num').payment('formatCardNumber');
        $('.cc-exp').payment('formatCardExpiry');
        $('.cc-cvc').payment('formatCardCVC');
      
        var validateDetails = function() {
      
          var expiry = $('.cc-exp').payment('cardExpiryVal');
          var validateExpiry = $.payment.validateCardExpiry(expiry["month"], expiry["year"]);
          var validateCVC = $.payment.validateCardCVC($('.cc-cvc').val());
      
          if (validateExpiry) {
            $('.cc-exp__demo').addClass('identified');
          } else {
            $('.cc-exp__demo').removeClass('identified');
          }
      
          if (validateCVC) {
            $('.cc-cvc__demo').addClass('identified');
          } else {
            $('.cc-cvc__demo').removeClass('identified');
          }
      
        }
      
        $('.paymentInput').bind('change paste keyup', function() {
          validateDetails();
        });
      
      });
 });