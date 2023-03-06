<?php
require "conexion.php";

    $Nombre = $_POST['Nombre'];
    $email = $_POST['Email'];

    $validar_login = mysql_query($Conexion, "SELECT * FROM Usuarios Where correo='$correo' And Contraseña='$contrasena'");

    if (mysqli_num_row($validar_login) > 0) {
        header("location: ../login.html");
        exit;
    } else {
        echo '
            <script>
                alert("Usuario no existe, por favor verifique los datos introducidos");
                window.location = ../index.html";
            </script>
        ';
    exit;
    }
?>