<?php
class ConexionBaseDatos
  {
    public function Conect()
    {
      $Servidor="127.0.0.1";
      $Port="33060";
      $Usuario="root";
      $Contrasena="";
      $BaseDeDatos="PracticaTaller";
      $DsnCaracteristicas = [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION];
      
      $Conexion = new PDO("mysql:dbname={$BaseDeDatos};host={$Servidor};port={$Port};charsert= utf8mb4_general_ci;",$Usuario ,$Contrasena ,$DsnCaracteristicas);
      
      return $Conexion;
      if (!$this -> Conect)
      {
        echo "Error de conexion";
      }
    }
  }
?>