// $(document).ready(function() {
//     $(".quantity").keyup(function() {
//       alert($(this).val());
//     });
//   })

    $(".quantity").change(function(){
      var num_of_pro = $(this).val();
      var product = $(".product_code").val();

      $.ajax({
        type : "GET",
        url : "/pro_quantity_check",
        data : {
        prod_quantity : num_of_pro,
        product_code : product
        },
        success : function(data){
            if (data.product_available == false)
            {
                alert("Not that much product on stock")
            }

        },
    })

      });


// $(".quantity").on("keyup",function(){
//     var screenName=$(this).val();
//     alert(screenName);
//   });



$(".plus-cart").click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type : "GET",
        url : "/pluscart",
        data : {
        prod_id : id
        },
        success : function(data){
        eml.innerText = data.quantity;
        document.getElementById("amount").innerText = data.amount;
        document.getElementById("total_amount").innerText = data.total_amount;
        },
    })
});



$(".minus-cart").click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type : "GET",
        url : "/minuscart",
        data : {
        prod_id : id
        },
        success : function(data){
        eml.innerText = data.quantity;
        document.getElementById("amount").innerText = data.amount;
        document.getElementById("total_amount").innerText = data.total_amount;
        },
    })
});


$(".remove_item").click(function(){
    var id = $(this).attr("pid");
    var eml = this
    $.ajax({
        type:"GET",
        url : "/remove_item",
        data : {
            prod_id : id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("total_amount").innerText = data.total_amount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
        }
    })
});