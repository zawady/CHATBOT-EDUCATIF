<?php
// Connexion à la base de données
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "chat";

$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

// Fonction de hachage du mot de passe
function hashPassword($password) {
    return password_hash($password, PASSWORD_DEFAULT);
}

// Inscription
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["register"])) {
    $nom = $_POST["nom"];
    $email = $_POST["email"];
    $password = hashPassword($_POST["password"]);

    $sql = "INSERT INTO utilisateurs (nom, email, password) VALUES ('$nom', '$email', '$password')";

    if ($conn->query($sql) === TRUE) {
        header("Location: templates/index.html");
        exit();
    } else {
        echo "Erreur d'inscription : " . $conn->error;
    }
}

// Connexion
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["login"])) {
    $username = $_POST["username"];
    $password = $_POST["password"];

    $sql = "SELECT * FROM utilisateurs WHERE nom='$username'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row["password"])) {
            header("Location: templates/index.html");
            exit();
        } else {
            echo "Mot de passe incorrect.";
        }
    } else {
        echo "Utilisateur non trouvé.";
    }
}

$conn->close();
?>
