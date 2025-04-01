<?php
$source = $_FILES["file"]["tmp_name"];
$target = "upload/" . $_FILES["file"]["name"];
if(move_uploaded_file($source, $target)){
    echo "başarılı";
} else {
    echo "Başarısız";
}

?>