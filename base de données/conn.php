<?php
// Connexion à la base de données
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "chatbot";

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
    $username = $_POST["nom"];
    $email = $_POST["email"];
    $password = hashPassword($_POST["password"]);

    $sql = "INSERT INTO utilisateurs (nom, email, password) VALUES ('$username', '$email', '$password')";

    if ($conn->query($sql) === TRUE) {
        header("Location: templates/chatbot.html");
        exit();
    } else {
        header("Location: index.html?error=Erreur lors de l'insription");

    }
}

// Connexion
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["login"])) {
    $username = $_POST["nom"];
    $password = $_POST["password"];

    $sql = "SELECT * FROM utilisateurs WHERE nom='$username'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row["password"])) {
            header("Location: templates/chatbot.html");
            exit();
        } else {
            header("Location: index.html?error=Utilisateur non trouvé");
        }
    } else {
        header("Location: index.html?error=Mot de passe incorrect");
    }
}

$conn->close();
?>
