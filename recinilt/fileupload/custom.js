$(document).ready(function(){
    $("#uploadForm").on("submit", function(e){
        console.log("submite basıldı");
        e.preventDefault(); //e yani event, normalde submit deyip,
        //sayfayı filan yeniler. bunu önlemek ve kendi istediğimizi yapmak
        //için, event.preventDefault() deriz.
        console.log($("#file").html())
        $.ajax({
            url:"upload.php", //hangi dosyayı çağırıp upload işlemini yaptırtacaz?
            type:"POST",
            data: new FormData(this),
            contentType:false,
            processData: false,
            success : function(data){

                console.log(data);
            }
        })
    })
});